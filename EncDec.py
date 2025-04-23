import os
import random

def xor_encrypt_decrypt(data, key):
    return bytes([b ^ key[i % len(key)] for i, b in enumerate(data)])

def generate_random_key(length):
    return bytes([random.randint(0, 255) for _ in range(length)])

def generate_pseudo_random_key(seed, length):
    random.seed(seed)
    return bytes([random.randint(0, 255) for _ in range(length)])

def read_file(filename):
    with open(filename, 'rb') as file:
        return file.read()

def write_text_file(filename, text):
    with open(filename, 'w') as file:
        file.write(text)

def read_text_file(filename):
    with open(filename, 'r') as file:
        return file.read()

def encrypt_file(method):
    input_file = input("Enter the path to the input text file: ").strip()
    if not os.path.exists(input_file):
        print("File not found 🚫")
        return

    data = read_file(input_file)

    if method == "random":
        key = generate_random_key(len(data))
        print("Random key generated (hex):", key.hex())
    else:
        seed = input("Enter a pseudo-random seed (e.g., a number or phrase): ")
        key = generate_pseudo_random_key(seed, len(data))
        print("Pseudo-random key generated using seed. (hex):", key.hex())

    encrypted = xor_encrypt_decrypt(data, key)
    encrypted_hex = encrypted.hex()

    output_file = input_file + ".enc.txt"
    write_text_file(output_file, encrypted_hex)

    print(f"File encrypted and saved as {output_file} ✅")

def decrypt_file():
    enc_file = input("Enter the path to the encrypted .enc.txt file: ").strip()
    if not os.path.exists(enc_file):
        print("File not found 🚫")
        return

    key_hex = input("Enter the key in hex (from encryption step): ").strip()
    try:
        key = bytes.fromhex(key_hex)
    except ValueError:
        print("Invalid key format 😵")
        return

    encrypted_hex = read_text_file(enc_file)
    try:
        encrypted = bytes.fromhex(encrypted_hex)
    except ValueError:
        print("Encrypted file format is corrupted or not in hex 😬")
        return

    decrypted = xor_encrypt_decrypt(encrypted, key)
    
    output_file = enc_file.replace(".enc.txt", ".dec.txt")
    with open(output_file, 'wb') as file:
        file.write(decrypted)

    print(f"File decrypted and saved as {output_file} ✅")

def menu():
    while True:
        print("\n🔐 Encryption Menu:")
        print("1. Encrypt with Random Key")
        print("2. Encrypt with Pseudo-Random Key")
        print("3. Decrypt File")
        print("4. Exit")

        choice = input("Select an option: ").strip()

        if choice == "1":
            encrypt_file("random")
        elif choice == "2":
            encrypt_file("pseudo")
        elif choice == "3":
            decrypt_file()
        elif choice == "4":
            print("Exiting... Peace out 👋")
            break
        else:
            print("Invalid choice, try again 😅")

if __name__ == "__main__":
    menu()
