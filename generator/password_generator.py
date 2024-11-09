import random
import string
from typing import Optional

class PasswordGenerationError(Exception):
    pass

def validate_length(length: int) -> bool:
    MIN_LENGTH = 4
    MAX_LENGTH = 128
    return MIN_LENGTH <= length <= MAX_LENGTH

def validate_option(option: int) -> bool:
    return 1 <= option <= 5

def generate_password(length: int = 8, option: int = 5) -> str:
    """
    Generate a password based on specified length and complexity option.
    
    Args:
        length: Length of the password (default: 8)
        option: Complexity option 1-5 (default: 5)
        
    Returns:
        str: Generated password
        
    Raises:
        PasswordGenerationError: If invalid parameters are provided
        ValueError: If parameters are of wrong type
    """
    try:
        # Validate input parameters
        if not isinstance(length, int) or not isinstance(option, int):
            raise ValueError("Length and option must be integers")
            
        if not validate_length(length):
            raise PasswordGenerationError(f"Password length must be between 4 and 128 characters")
            
        if not validate_option(option):
            raise PasswordGenerationError("Invalid option. Please choose a number between 1 and 5")

        # Define character sets
        numbers = string.digits
        lowercase = string.ascii_lowercase
        uppercase = string.ascii_uppercase
        special_characters = string.punctuation

        # Choose character set based on option
        char_sets = {
            1: numbers,
            2: lowercase,
            3: lowercase + uppercase,
            4: lowercase + uppercase + numbers,
            5: lowercase + uppercase + numbers + special_characters
        }
        
        char_set = char_sets[option]

        # Ensure minimum complexity requirements for options 3-5
        if option >= 3:
            # Generate password ensuring at least one character from each required set
            password = []
            if option >= 3:
                password.extend([random.choice(lowercase), random.choice(uppercase)])
            if option >= 4:
                password.append(random.choice(numbers))
            if option >= 5:
                password.append(random.choice(special_characters))
                
            # Fill the rest of the length with random characters
            remaining_length = length - len(password)
            password.extend(random.choice(char_set) for _ in range(remaining_length))
            
            # Shuffle the password to make it random
            random.shuffle(password)
            return ''.join(password)
        else:
            # For options 1-2, generate password normally
            return ''.join(random.choice(char_set) for _ in range(length))

    except Exception as e:
        raise PasswordGenerationError(f"Error generating password: {str(e)}")

def password_generator() -> Optional[str]:
    """
    Interactive password generator function.
    
    Returns:
        Optional[str]: Generated password or None if error occurs
    """
    try:
        # Get and validate length input
        while True:
            try:
                length_input = input("Enter the desired password length (4-128): ").strip()
                length = int(length_input)
                if validate_length(length):
                    break
                print("Please enter a length between 4 and 128 characters.")
            except ValueError:
                print("Please enter a valid number.")

        # Display options
        print("\nPassword Options:")
        print("1 - Numbers only (PIN)")
        print("2 - Lowercase only")
        print("3 - Mixed case")
        print("4 - Mixed case with numbers")
        print("5 - Mixed case with numbers and special characters")
        
        # Get and validate option input
        while True:
            try:
                option_input = input("\nChoose a password type (1-5): ").strip()
                option = int(option_input)
                if validate_option(option):
                    break
                print("Please enter a number between 1 and 5.")
            except ValueError:
                print("Please enter a valid number.")

        # Generate and display password
        password = generate_password(length=length, option=option)
        print(f"\nGenerated password: {password}")
        return password

    except KeyboardInterrupt:
        print("\nPassword generation cancelled by user.")
        return None
    except Exception as e:
        print(f"\nError: {str(e)}")
        return None