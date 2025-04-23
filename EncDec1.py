import os
import random
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog

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
        seed = simpledialog.askstring("Seed Input", "Enter a pseudo-random seed:", parent=root)
        if seed is None:
            return
        key = generate_pseudo_random_key(seed, len(data))

    encrypted = xor_encrypt_decrypt(data, key)
    encrypted_hex = encrypted.hex()
    output_file = input_file + ".enc.txt"
    write_text_file(output_file, encrypted_hex)

    messagebox.showinfo("Success", f"Encrypted file saved as:\n{output_file}\n\nKey (hex):\n{key.hex()}")
    
def get_key_from_popup():
    popup = tk.Toplevel(root)
    popup.title("Enter Key in Hex")
    popup.geometry("450x180")
    popup.configure(bg="white")

    popup.grab_set()
    popup.focus_force()

    label = tk.Label(
        popup, 
        text="Paste your hex key below:", 
        font=("Segoe UI", 12),
        fg="black", 
        bg="white"
    )
    label.pack(pady=10)

    # Use a Text widget instead of Entry for better visibility
    entry = tk.Text(
        popup,
        width=52,  # Adjusted width for Text widget
        height=3,  # Allow multiple lines
        font=("Courier", 12),
        fg="black",
        bg="#f0f0f0",  # Light gray background for better contrast
        insertbackground="black"
    )
    entry.pack(pady=5)

    key_var = tk.StringVar()

    def submit():
        # Get text from the Text widget
        key_var.set(entry.get("1.0", "end-1c"))
        popup.destroy()

    submit_btn = tk.Button(popup, text="Submit", command=submit, 
                          bg="#4CAF50", fg="white", 
                          font=("Segoe UI", 10))
    submit_btn.pack(pady=15)

    entry.focus_set()
    root.wait_window(popup)
    return key_var.get()

# Decrypt
def decrypt_file():
    enc_file = filedialog.askopenfilename(title="Select encrypted .enc.txt file", parent=root)
    if not enc_file or not os.path.exists(enc_file):
        messagebox.showerror("Error", "File not found.", parent=root)
        return

    key_hex = get_key_from_popup()
    if not key_hex:
        return

    try:
        key = bytes.fromhex(key_hex)
    except ValueError:
        messagebox.showerror("Error", "Invalid key format.", parent=root)
        return

    encrypted_hex = read_text_file(enc_file)
    try:
        encrypted = bytes.fromhex(encrypted_hex)
    except ValueError:
        messagebox.showerror("Error", "Encrypted file is corrupted or not in hex.", parent=root)
        return

    decrypted = xor_encrypt_decrypt(encrypted, key)
    output_file = enc_file.replace(".enc.txt", ".dec.txt")
    with open(output_file, 'wb') as file:
        file.write(decrypted)

    messagebox.showinfo("Success", f"Decrypted file saved as:\n{output_file}", parent=root)

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
