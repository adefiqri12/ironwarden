import hashlib
import random

# Load the BIP39 wordlist
def load_wordlist(filename):
    try:
        with open(filename, 'r') as file:
            wordlist = file.read().splitlines()
        
        # Check if wordlist contains exactly 2048 words
        if len(wordlist) != 2048:
            raise ValueError("The word list must contain exactly 2048 words.")
        
        return wordlist

    except FileNotFoundError:
        raise FileNotFoundError(f"Error: The file '{filename}' was not found.")
    except IOError:
        raise IOError(f"Error: Unable to read the file '{filename}'. Check file permissions.")
    except ValueError as e:
        raise ValueError(f"Error: {str(e)}")

# Convert the entropy (in bytes) to a binary string
def bytes_to_bin(byte_array):
    return ''.join(f'{byte:08b}' for byte in byte_array)

# Generate the checksum
def generate_checksum(entropy_bytes):
    # Calculate the SHA256 hash of the entropy
    hash_bytes = hashlib.sha256(entropy_bytes).digest()
    # Take the first n bits from the hash (n is entropy length / 32)
    checksum_length = len(entropy_bytes) * 8 // 32
    checksum_bin = bytes_to_bin(hash_bytes)[:checksum_length]
    return checksum_bin

# Generate a random 12-word mnemonic
def generate_mnemonic(wordlist):
    # Generate 128 bits of entropy (16 bytes)
    entropy_bytes = random.getrandbits(128).to_bytes(16, byteorder='big')
    
    # Convert entropy to binary
    entropy_bin = bytes_to_bin(entropy_bytes)
    
    # Generate checksum from the entropy
    checksum_bin = generate_checksum(entropy_bytes)
    
    # Append checksum to the entropy
    entropy_bin_with_checksum = entropy_bin + checksum_bin
    
    # Split the binary string into 11-bit chunks
    words_indices = [int(entropy_bin_with_checksum[i:i+11], 2) for i in range(0, len(entropy_bin_with_checksum), 11)]
    
    # Map the 11-bit chunks to words in the wordlist
    mnemonic = [wordlist[index] for index in words_indices]
    
    return ' '.join(mnemonic)

# Main program
try:
    # Load the BIP39 word list from the file
    wordlist = load_wordlist('/dictionary/bip39.txt')
    
    # Generate a valid 12-word seed phrase
    seed_phrase = generate_mnemonic(wordlist)
    print("Generated 12-word seed phrase:", seed_phrase)

except Exception as e:
    print(f"An error occurred: {e}")