import random

def load_wordlist(filename):
    try:
        with open(filename, 'r') as file:
            wordlist = file.read().splitlines()
        return wordlist
    except FileNotFoundError:
        raise FileNotFoundError(f"Error: The file '{filename}' was not found.")
    except IOError:
        raise IOError(f"Error: Unable to read the file '{filename}'. Check file permissions.")
    except ValueError as e:
        raise ValueError(f"Error: {str(e)}")

def generate_single_username(include_number):
    try:
        adjective = random.choice(load_wordlist('./dictionary/english-adjectives.txt')).capitalize()
        noun = random.choice(load_wordlist('./dictionary/english-nouns.txt')).capitalize()
    except ValueError as e:
        raise ValueError(f"Error: {str(e)}") from e
    try:
        if include_number in ['yes', 'y']:
            number = random.randint(0, 9999)
            username = f"{adjective}{noun}{number}"
        else:
            username = f"{adjective}{noun}"
    except TypeError as e:
        raise TypeError(f"Error: {str(e)}") from e
    return username

def generate_usernames():
    include_number = input("Do you want to include a number in the usernames? (y/n): ").lower()
    while True:
        usernames = [generate_single_username(include_number) for _ in range(5)]
        print("\nHere are 5 generated usernames:")
        for i, username in enumerate(usernames, 1):
            print(f"{i}. {username}")
        print("6. Reroll for a new set of usernames")
        try:
            choice = int(input("\nSelect an option (1-6): "))
            if 1 <= choice <= 5:
                print(f"\nYou selected: {usernames[choice - 1]}")
                return usernames[choice - 1]
            elif choice == 6:
                print("\nRerolling for a new set of usernames...\n")
            else:
                print("Invalid option. Please select a number between 1 and 6.")
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 6.")

print(generate_usernames())