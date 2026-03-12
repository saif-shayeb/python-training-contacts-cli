from colorama import Fore, Style, init

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

#################################################
# because i used 2 dictionaries one with key
# and the other dict use the number as key the
# time complexity of the search for both by name
# and by number is on avg O(1) (trivial) because
# the dictionary uses hash table but if a
# collision happen it can be O(n) in the worst
# case
# the time complexity for the show all contacts is
# O(n) because it iterates over the items of the
# dict so
#                       avg     worst
# --------------------------------------
# find_by_name()->      O(1)    O(n)
# find_by_number(num)-> O(1)    O(n)
# add_new_contact->     O(1)    O(n)
# show_all_contacts()-> O(n)    O(n)
#################################################


def find_by_name(name):
    return contacts[name]


def find_by_number(num):
    return reverse_contacts[num]


def show_all_contacts():
    print("------------------------")
    print(Style.BRIGHT + "  Name        Number")
    print("------------------------")
    for i, (k, v) in enumerate(contacts.items(), start=1):
        print(Fore.BLUE + f"{i}." + Style.BRIGHT + f"{k:<12}{v}")
    print("------------------------")


def add_new_contact(name, num):
    num_res = contacts.setdefault(name, num)
    if num_res != num:
        return Fore.RED + "name already exists!!"
    else:
        name_res = reverse_contacts.setdefault(num, name)
        if name_res != name:
            return Fore.RED + "number already exists!!"
        else:
            return Fore.GREEN + "added successfully!"


def main():
    choice = ""
    print("======================================")
    print("-----welcome to the contacts app------")
    print("======================================")
    init(autoreset=True)
    while choice != "#":
        print("1.add new contact")
        print("2.search by name")
        print("3.search by number")
        print("4.show all contacts")
        print("#.to exit")
        print("======================================")
        choice = input("Enter your choice:")
        match choice:
            case "1":
                name = input("Enter name:")
                num = input("Enter number")
                print(add_new_contact(name, num))
            case "2":
                name = input("Enter name:")
                num = ""
                try:
                    num = find_by_name(name)
                except KeyError:
                    print(Fore.RED + "contact not found!")
                if num != "":
                    print("------------------------")
                    print(
                        Fore.CYAN
                        + "number for name:"
                        + name
                        + " is: "
                        + Style.BRIGHT
                        + num
                    )
                    print("------------------------")

            case "3":
                num = input("Enter number:")
                name = ""
                try:
                    name = find_by_number(num)
                except KeyError:
                    print(Fore.RED + "contact not found!")
                if name != "":
                    print(
                        Fore.CYAN
                        + "name for number :"
                        + num
                        + " is: "
                        + Style.BRIGHT
                        + name
                    )
            case "4":
                show_all_contacts()


if __name__ == "__main__":
    main()
