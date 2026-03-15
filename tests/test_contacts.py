import pytest

import main
import manager
import utils
from utils import WeakPasswordError

BASE_CONTACTS = {
    "adam": "0597365598",
    "rami": "0569876546",
}


def use_inputs(monkeypatch, values):
    answers = iter(values)
    monkeypatch.setattr("builtins.input", lambda _prompt: next(answers))


@pytest.fixture
def isolated_contacts():
    original_contacts = manager.contacts.copy()
    original_reverse_contacts = manager.reverse_contacts.copy()
    manager.contacts = BASE_CONTACTS.copy()
    manager.reverse_contacts = {num: name for name, num in BASE_CONTACTS.items()}
    yield
    manager.contacts = original_contacts
    manager.reverse_contacts = original_reverse_contacts


def test_validate_password_accepts_strong_password():
    assert utils.validate_password("Strong123!") is None


@pytest.mark.parametrize(
    "password",
    ["weak123!", "Aa1", "Aa1" + ("x" * 38)],
)
def test_validate_password_rejects_invalid_passwords(password):
    with pytest.raises(WeakPasswordError):
        utils.validate_password(password)


def test_save_and_load_contacts_round_trip(tmp_path, monkeypatch):
    payload = BASE_CONTACTS.copy()
    monkeypatch.chdir(tmp_path)
    utils.save_contacts(payload)
    contacts, reverse_contacts = utils.load_contacts()

    assert contacts == payload
    assert reverse_contacts == {num: name for name, num in payload.items()}


def test_add_contact_success(isolated_contacts, monkeypatch):
    save_calls = []
    monkeypatch.setattr(
        manager, "save_contacts", lambda data: save_calls.append(data.copy())
    )
    result = manager.add_contact("sara", "0500000000")

    assert "added successfully" in result
    assert manager.contacts["sara"] == "0500000000"
    assert manager.reverse_contacts["0500000000"] == "sara"
    assert save_calls == [manager.contacts.copy()]


def test_add_contact_duplicate_pair(isolated_contacts, monkeypatch):
    save_calls = []
    monkeypatch.setattr(manager, "save_contacts", lambda data: save_calls.append(data))
    result = manager.add_contact("adam", "0597365598")

    assert "contact already added" in result
    assert save_calls == []


@pytest.mark.parametrize(
    ("function", "user_input"),
    [
        (manager.get_by_name, "not-exists"),
        (manager.get_by_num, "000"),
    ],
)
def test_lookup_not_found(function, user_input, isolated_contacts, monkeypatch, capsys):
    use_inputs(monkeypatch, [user_input])
    function()
    assert "contact not found" in capsys.readouterr().out


def test_delete_contact_confirms_yes(isolated_contacts, monkeypatch):
    save_calls = []
    monkeypatch.setattr(manager, "show_all_contacts", lambda: None)
    use_inputs(monkeypatch, ["adam", "Y"])
    monkeypatch.setattr(
        manager, "save_contacts", lambda data: save_calls.append(data.copy())
    )

    manager.delete_contact()

    assert "adam" not in manager.contacts
    assert len(save_calls) == 1


def test_delete_contact_invalid_name(isolated_contacts, monkeypatch, capsys):
    monkeypatch.setattr(manager, "show_all_contacts", lambda: None)
    use_inputs(monkeypatch, ["unknown"])
    save_calls = []
    monkeypatch.setattr(manager, "save_contacts", lambda data: save_calls.append(data))

    manager.delete_contact()

    assert "invalid name" in capsys.readouterr().out
    assert save_calls == []


def test_password_retry_then_exit(monkeypatch, capsys):
    validate_results = iter([WeakPasswordError("weak password"), None])

    def fake_validate(_password):
        result = next(validate_results)
        if isinstance(result, Exception):
            raise result

    monkeypatch.setattr(main, "validate_password", fake_validate)
    monkeypatch.setattr(main, "init", lambda **_kwargs: None)
    use_inputs(monkeypatch, ["weak", "Strong123!", "#"])

    main.main()

    assert "weak password" in capsys.readouterr().out


def test_choice_add_calls_add_contact(monkeypatch):
    calls = []
    monkeypatch.setattr(main, "validate_password", lambda _password: None)
    monkeypatch.setattr(main, "init", lambda **_kwargs: None)
    monkeypatch.setattr(
        main, "add_contact", lambda name, num: calls.append((name, num)) or "added"
    )
    use_inputs(monkeypatch, ["Strong123!", "1", "sara", "0500000000", "#"])

    main.main()

    assert calls == [("sara", "0500000000")]


def test_choice_delete_calls_delete_contact(monkeypatch):
    delete_calls = []
    monkeypatch.setattr(main, "validate_password", lambda _password: None)
    monkeypatch.setattr(main, "init", lambda **_kwargs: None)
    monkeypatch.setattr(main, "delete_contact", lambda: delete_calls.append(True))
    use_inputs(monkeypatch, ["Strong123!", "5", "#"])

    main.main()

    assert delete_calls == [True]
