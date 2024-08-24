import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
from cryptography.fernet import Fernet

def generate_key():
    return Fernet.generate_key()

def save_file(data, file_type, default_ext):
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    file_path = filedialog.asksaveasfilename(
        title=f"Save the {file_type} file",
        defaultextension=default_ext,
        filetypes=[(f"{file_type} files", default_ext)]
    )
    if not file_path:
        messagebox.showerror("Error", f"No {file_type} file path provided!")
        return None
    try:
        with open(file_path, 'wb') as file:
            file.write(data)
        return file_path
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")
        return None

def encrypt_message():
    # Generate key
    key = generate_key()
    cipher_suite = Fernet(key)
    
    # Get message from user
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    secret_message = simpledialog.askstring("Input", "Encrypt text:")
    
    if not secret_message:
        messagebox.showerror("Error", "No message provided!")
        return

    # Encrypt the message
    encrypted_message = cipher_suite.encrypt(secret_message.encode())
    
    # Save key and encrypted message
    key_file_path = save_file(key, "key", ".key")
    if key_file_path:
        encrypted_file_path = save_file(encrypted_message, "encrypted message", ".enc")
        if encrypted_file_path:
            messagebox.showinfo("Success", f"Key saved to {key_file_path}\nEncrypted message saved to {encrypted_file_path}")

if __name__ == "__main__":
    encrypt_message()
