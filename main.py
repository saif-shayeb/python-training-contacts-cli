from colorama import init
from manager import (
    add_contact,
    get_by_name,
    get_by_num,
    show_all_contacts,
    delete_contact,
)
from utils import WeakPasswordError, validate_password

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
#################################################
# after adding the json file the time complextity
# changed for those functions:
# add_new_contact() ->
#       O(n) to write to the json file
# delete_contact() ->
#       O(n) also to write to the json
# and an initial O(n) on startup to load from json
##################################################


def main():
    choice = ""
    print("======================================")
    print("-----welcome to the contacts app------")
    print("======================================")
    init(autoreset=True)

    # Require a strong session password before allowing app actions.
    while True:
        app_password = input("Set app password: ")
        try:
            validate_password(app_password)
            break
        except WeakPasswordError as err:
            print(err)

    while choice != "#":
        print("1.add new contact")
        print("2.search by name")
        print("3.search by number")
        print("4.show all contacts")
        print("5.Remove a contact")
        print("#.to exit")
        print("======================================")
        choice = input("Enter your choice:")
        match choice:
            case "1":
                name = input("Enter name:")
                num = input("Enter number:")
                print(add_contact(name, num))
            case "2":
                get_by_name()

            case "3":
                get_by_num()
            case "4":
                show_all_contacts()
            case "5":
                delete_contact()


if __name__ == "__main__":
    main()
