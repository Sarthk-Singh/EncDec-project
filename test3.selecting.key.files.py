import os
import random
import tkinter as tk
from tkinter import filedialog, messagebox

# XOR logic
def xor_encrypt_decrypt(data, key):
    return bytes([b ^ key[i % len(key)] for i, b in enumerate(data)])

# Random key generators
def generate_random_key(length):
    return bytes([random.randint(0, 255) for _ in range(length)])

def generate_pseudo_random_key(seed, length):
    random.seed(seed)
    return bytes([random.randint(0, 255) for _ in range(length)])

# File I/O
def read_file(filename):
    with open(filename, 'rb') as file:
        return file.read()

def write_text_file(filename, text):
    with open(filename, 'w') as file:
        file.write(text)

def read_text_file(filename):
    with open(filename, 'r') as file:
        return file.read()

# Encrypt
def encrypt_file(method):
    input_file = filedialog.askopenfilename(title="Select input text file")
    if not input_file or not os.path.exists(input_file):
        messagebox.showerror("Error", "File not found.")
        return

    data = read_file(input_file)

    if method == "random":
        key = generate_random_key(len(data))
    else:
        # Ask the user to select a seed file
        messagebox.showinfo("Seed File", "Please select a text file containing the seed value.")
        seed_file = filedialog.askopenfilename(title="Select seed file")
        if not seed_file or not os.path.exists(seed_file):
            return
        
        try:
            seed = read_text_file(seed_file).strip()
            if not seed:
                messagebox.showerror("Error", "Seed file is empty.")
                return
            key = generate_pseudo_random_key(seed, len(data))
        except Exception as e:
            messagebox.showerror("Error", f"Could not read seed file: {str(e)}")
            return

    encrypted = xor_encrypt_decrypt(data, key)
    encrypted_hex = encrypted.hex()
    output_file = input_file + ".enc.txt"
    write_text_file(output_file, encrypted_hex)
    
    # Save the key to a separate file
    key_file = input_file + ".key.txt"
    write_text_file(key_file, key.hex())

    messagebox.showinfo("Success", f"Encrypted file saved as:\n{output_file}\n\nKey saved to:\n{key_file}")

# Decrypt
def decrypt_file():
    enc_file = filedialog.askopenfilename(title="Select encrypted .enc.txt file")
    if not enc_file or not os.path.exists(enc_file):
        messagebox.showerror("Error", "File not found.")
        return

    # Select key file instead of typing it
    messagebox.showinfo("Key File", "Please select the text file containing the hex key.")
    key_file = filedialog.askopenfilename(title="Select key file")
    if not key_file or not os.path.exists(key_file):
        return
    
    try:
        key_hex = read_text_file(key_file).strip()
        key = bytes.fromhex(key_hex)
    except ValueError:
        messagebox.showerror("Error", "Invalid key format in key file.")
        return
    except Exception as e:
        messagebox.showerror("Error", f"Could not read key file: {str(e)}")
        return

    try:
        encrypted_hex = read_text_file(enc_file)
        encrypted = bytes.fromhex(encrypted_hex)
    except ValueError:
        messagebox.showerror("Error", "Encrypted file is corrupted or not in hex.")
        return
    except Exception as e:
        messagebox.showerror("Error", f"Could not read encrypted file: {str(e)}")
        return

    decrypted = xor_encrypt_decrypt(encrypted, key)
    output_file = enc_file.replace(".enc.txt", ".dec.txt")
    with open(output_file, 'wb') as file:
        file.write(decrypted)

    messagebox.showinfo("Success", f"Decrypted file saved as:\n{output_file}")

# GUI setup
root = tk.Tk()
root.title("🛡 XOR Encrypt/Decrypt Tool")
root.geometry("400x300")
root.configure(bg="#1e1e1e")

title = tk.Label(root, text="Encrypt/Decrypt Files", font=("Segoe UI", 16, "bold"), fg="white", bg="#1e1e1e")
title.pack(pady=20)

btn1 = tk.Button(root, text="Encrypt with Random Key", width=30, command=lambda: encrypt_file("random"))
btn1.pack(pady=5)

btn2 = tk.Button(root, text="Encrypt with Pseudo-Random Key", width=30, command=lambda: encrypt_file("pseudo"))
btn2.pack(pady=5)

btn3 = tk.Button(root, text="Decrypt File", width=30, command=decrypt_file)
btn3.pack(pady=5)

btn4 = tk.Button(root, text="Exit", width=30, command=root.destroy)
btn4.pack(pady=20)

root.mainloop()