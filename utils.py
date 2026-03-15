import json
import re


class WeakPasswordError(Exception):
    pass


def save_contacts(data):
    with open("contacts.json", "w+") as f:
        json.dump(data, f)


def load_contacts():
    with open("contacts.json", "r") as f:
        contacts = json.load(f)
        reverse_contacts = {}
        for k, v in contacts.items():
            reverse_contacts[v] = k
    return (contacts, reverse_contacts)


def init_contacts(contacts):
    save_contacts(contacts)


def validate_password(password):
    pattern = r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d).{6,40}$"
    if not re.fullmatch(pattern, password):
        raise WeakPasswordError(
            "password must have at least one upper case letter"
            + " and one lowercase letter and one digit and should be "
            + "in range of 6 to 40 letters long"
        )
