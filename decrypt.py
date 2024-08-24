import tkinter as tk
from tkinter import filedialog, messagebox
from cryptography.fernet import Fernet, InvalidToken

def load_file(file_type):
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    file_path = filedialog.askopenfilename(
        title=f"Select the {file_type} file",
        filetypes=[(f"{file_type} files", f"*.{file_type}")]
    )
    if not file_path:
        messagebox.showerror("Error", f"No {file_type} file selected!")
        return None
    try:
        with open(file_path, 'rb') as file:
            return file.read()
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")
        return None

def save_to_txt(message):
    file_path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text files", "*.txt")],
        title="Save as"
    )
    if file_path:
        try:
            with open(file_path, 'w') as file:
                file.write(message)
            messagebox.showinfo("Success", f"Message saved to {file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

def copy_to_clipboard(message):
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    root.clipboard_clear()
    root.clipboard_append(message)
    root.update()  # Keep the clipboard updated
    root.destroy()

def show_result_window(decrypted_message):
    result_window = tk.Tk()
    result_window.title("Decrypted Message")
    
    # Create a non-editable text widget to display the decrypted message
    text_widget = tk.Text(result_window, wrap='word', width=50, height=10)
    text_widget.insert('1.0', decrypted_message)
    text_widget.config(state='disabled')  # Make the text widget read-only
    text_widget.pack(pady=10, padx=10)
    
    # Add buttons for copying, saving, and exiting
    button_frame = tk.Frame(result_window)
    button_frame.pack(pady=10)
    
    copy_button = tk.Button(button_frame, text="Copy to Clipboard", command=lambda: copy_to_clipboard(decrypted_message))
    copy_button.pack(side='left', padx=5)
    
    save_button = tk.Button(button_frame, text="Save to TXT", command=lambda: save_to_txt(decrypted_message))
    save_button.pack(side='left', padx=5)
    
    exit_button = tk.Button(button_frame, text="Exit", command=result_window.destroy)
    exit_button.pack(side='left', padx=5)
    
    result_window.mainloop()

def decrypt_message():
    # Load key and encrypted message
    key = load_file("key")
    if key is None:
        return
    
    encrypted_message = load_file("enc")
    if encrypted_message is None:
        return
    
    try:
        cipher_suite = Fernet(key)
        decrypted_message = cipher_suite.decrypt(encrypted_message).decode()
        show_result_window(decrypted_message)
    except InvalidToken:
        messagebox.showerror("Error", "Invalid key or corrupted message!")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

if __name__ == "__main__":
    decrypt_message()
