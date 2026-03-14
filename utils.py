import json


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
