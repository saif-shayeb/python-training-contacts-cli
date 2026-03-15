import pytest

import main
import manager
import utils
from utils import WeakPasswordError


@pytest.fixture
def isolated_contacts():
    original_contacts = manager.contacts.copy()
    original_reverse_contacts = manager.reverse_contacts.copy()
    manager.contacts = {
        "adam": "0597365598",
        "rami": "0569876546",
    }
    manager.reverse_contacts = {
        "0597365598": "adam",
        "0569876546": "rami",
    }
    yield
    manager.contacts = original_contacts
    manager.reverse_contacts = original_reverse_contacts


def test_validate_password_accepts_strong_password():
    assert utils.validate_password("Strong123") is None


def test_validate_password_rejects_missing_uppercase():
    with pytest.raises(WeakPasswordError):
        utils.validate_password("weak123")


def test_validate_password_rejects_too_short():
    with pytest.raises(WeakPasswordError):
        utils.validate_password("Aa1")


def test_validate_password_rejects_too_long():
    long_password = "Aa1" + ("x" * 38)
    with pytest.raises(WeakPasswordError):
        utils.validate_password(long_password)


def test_save_and_load_contacts_round_trip(tmp_path, monkeypatch):
    payload = {"adam": "0597365598", "rami": "0569876546"}
    monkeypatch.chdir(tmp_path)
    utils.save_contacts(payload)
    contacts, reverse_contacts = utils.load_contacts()

    assert contacts == payload
    assert reverse_contacts == {
        "0597365598": "adam",
        "0569876546": "rami",
    }


def test_add_contact_success(isolated_contacts, monkeypatch):
    save_calls = []

    def fake_save(data):
        save_calls.append(data.copy())

    monkeypatch.setattr(manager, "save_contacts", fake_save)
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


def test_get_by_name_not_found(isolated_contacts, monkeypatch, capsys):
    monkeypatch.setattr("builtins.input", lambda _prompt: "not-exists")
    manager.get_by_name()
    out = capsys.readouterr().out
    assert "contact not found" in out


def test_get_by_num_not_found(isolated_contacts, monkeypatch, capsys):
    monkeypatch.setattr("builtins.input", lambda _prompt: "000")
    manager.get_by_num()
    out = capsys.readouterr().out
    assert "contact not found" in out


def test_delete_contact_confirms_yes(isolated_contacts, monkeypatch):
    inputs = iter(["adam", "Y"])
    save_calls = []
    monkeypatch.setattr(manager, "show_all_contacts", lambda: None)
    monkeypatch.setattr("builtins.input", lambda _prompt: next(inputs))
    monkeypatch.setattr(
        manager, "save_contacts", lambda data: save_calls.append(data.copy())
    )

    manager.delete_contact()

    assert "adam" not in manager.contacts
    assert len(save_calls) == 1


def test_delete_contact_invalid_name(isolated_contacts, monkeypatch, capsys):
    monkeypatch.setattr(manager, "show_all_contacts", lambda: None)
    monkeypatch.setattr("builtins.input", lambda _prompt: "unknown")
    save_calls = []
    monkeypatch.setattr(manager, "save_contacts", lambda data: save_calls.append(data))

    manager.delete_contact()

    out = capsys.readouterr().out
    assert "invalid name" in out
    assert save_calls == []


def test_password_retry_then_exit(monkeypatch, capsys):
    inputs = iter(["weak", "Strong123", "#"])
    validate_states = iter([WeakPasswordError("weak password"), None])

    def fake_validate(_password):
        state = next(validate_states)
        if isinstance(state, Exception):
            raise state
        return state

    monkeypatch.setattr(main, "validate_password", fake_validate)
    monkeypatch.setattr("builtins.input", lambda _prompt: next(inputs))
    monkeypatch.setattr(main, "init", lambda **_kwargs: None)

    main.main()

    out = capsys.readouterr().out
    assert "weak password" in out


def test_choice_add_calls_add_contact(monkeypatch):
    inputs = iter(["Strong123", "1", "sara", "0500000000", "#"])
    calls = []
    monkeypatch.setattr(main, "validate_password", lambda _password: None)
    monkeypatch.setattr("builtins.input", lambda _prompt: next(inputs))
    monkeypatch.setattr(main, "init", lambda **_kwargs: None)
    monkeypatch.setattr(
        main, "add_contact", lambda name, num: calls.append((name, num)) or "added"
    )

    main.main()

    assert calls == [("sara", "0500000000")]


def test_choice_delete_calls_delete_contact(monkeypatch):
    inputs = iter(["Strong123", "5", "#"])
    delete_calls = []
    monkeypatch.setattr(main, "validate_password", lambda _password: None)
    monkeypatch.setattr("builtins.input", lambda _prompt: next(inputs))
    monkeypatch.setattr(main, "init", lambda **_kwargs: None)
    monkeypatch.setattr(main, "delete_contact", lambda: delete_calls.append(True))

    main.main()

    assert delete_calls == [True]
