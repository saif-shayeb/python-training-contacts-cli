from colorama import Fore, Style
from utils import load_contacts, save_contacts, init_contacts

###########################################################################
# this part is only used for testing and to always have the same contacs on
# startup
contacts = {
    "khalid": "0599131355",
    "adam": "0597365598",
    "rami": "0569876546",
    "ali": "0598754632",
}
reverse_contacts = {
    "0599131355": "khalid",
    "0597365598": "adam",
    "0569876546": "rami",
    "0598754632": "ali",
}


init_contacts(contacts)
##########################################################################
contacts, reverse_contacts = load_contacts()


def add_contact(name, num):
    num_check = contacts.get(name)
    name_check = reverse_contacts.get(num)
    if num_check == num and name_check == name:
        return Fore.RED + "contact already added"
    if num_check == num:
        return Fore.RED + "number already exists!!"
    if name_check == name:
        return Fore.RED + "name already exists!!"
    num_res = contacts.setdefault(name, num)
    name_res = reverse_contacts.setdefault(num, name)
    if name == name_res and num == num_res:
        save_contacts(contacts)
        return Fore.GREEN + "added successfully!"


def get_by_name():
    name = input("Enter name:")
    num = ""
    try:
        num = contacts[name]
    except KeyError:
        print(Fore.RED + "contact not found!")
    if num != "":
        print("------------------------")
        print(Fore.CYAN
              + "number for name:"
              + name + " is: "
              + Style.BRIGHT
              + num)
        print("------------------------")


def get_by_num():
    num = input("Enter number:")
    name = ""
    try:
        name = reverse_contacts[num]
    except KeyError:
        print(Fore.RED + "contact not found!")
    if name != "":
        print("------------------------")
        print(Fore.CYAN
              + "name for number :"
              + num
              + " is: "
              + Style.BRIGHT
              + name)
        print("------------------------")


def show_all_contacts():
    print("------------------------")
    print(Style.BRIGHT + "  Name        Number")
    print("------------------------")
    for i, (k, v) in enumerate(contacts.items(), start=1):
        print(Fore.BLUE + f"{i}." + Style.BRIGHT + f"{k:<12}{v}")
    print("------------------------")


def delete_contact():
    show_all_contacts()
    name = input("please enter the name of the user u want to delete:")
    try:
        confirm = input(
            "confirm the deletion of the contact:"
            + name
            + "\t"
            + contacts[name]
            + "(Y\\N)?"
        )
    except KeyError:
        print(Fore.RED + "invalid name!")
        return
    if confirm.capitalize() == "Y":
        contacts.pop(name)
        save_contacts(contacts)
        print(Fore.GREEN + "deleted successfully")
        return
    elif confirm.capitalize() == "N":
        print(Fore.RED + "canceled deletion")
        return
    print("invalid input")
