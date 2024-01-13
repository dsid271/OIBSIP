import tkinter as tk
from tkinter import ttk, messagebox
import random
import string
import pyperclip

class PasswordGeneratorGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Password Generator")
        self.master.geometry("400x300")

        self.label_length = tk.Label(master, text="Password Length:", font=('Segoe UI', 10))
        self.label_length.pack(pady=10)

        self.entry_length = tk.Entry(master, font=('Segoe UI', 10))
        self.entry_length.pack()

        self.check_var_upper = tk.IntVar()
        self.check_upper = tk.Checkbutton(master, text="Include Uppercase", variable=self.check_var_upper, font=('Segoe UI', 10))
        self.check_upper.pack()

        self.check_var_lower = tk.IntVar()
        self.check_lower = tk.Checkbutton(master, text="Include Lowercase", variable=self.check_var_lower, font=('Segoe UI', 10))
        self.check_lower.pack()

        self.check_var_digits = tk.IntVar()
        self.check_digits = tk.Checkbutton(master, text="Include Digits", variable=self.check_var_digits, font=('Segoe UI', 10))
        self.check_digits.pack()

        self.check_var_symbols = tk.IntVar()
        self.check_symbols = tk.Checkbutton(master, text="Include Symbols", variable=self.check_var_symbols, font=('Segoe UI', 10))
        self.check_symbols.pack()

        self.btn_generate = tk.Button(master, text="Generate Password", command=self.generate_password, font=('Segoe UI', 10), bg='#0078D4', fg='white')
        self.btn_generate.pack(pady=20)

        self.btn_copy = tk.Button(master, text="Copy to Clipboard", command=self.copy_to_clipboard, font=('Segoe UI', 10), bg='#0078D4', fg='white')
        self.btn_copy.pack()

    def generate_password(self):
        try:
            length = int(self.entry_length.get())
            if length <= 0:
                raise ValueError("Password length must be a positive integer.")

            character_sets = {
                'upper': string.ascii_uppercase if self.check_var_upper.get() else '',
                'lower': string.ascii_lowercase if self.check_var_lower.get() else '',
                'digits': string.digits if self.check_var_digits.get() else '',
                'symbols': string.punctuation if self.check_var_symbols.get() else ''
             }

            all_characters = ''.join(character_sets.values())

            if not all_characters:
                raise ValueError("Please select at least one character set.")

            password = ''.join(random.choice(all_characters) for _ in range(length))
            self.show_password(password)

        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def copy_to_clipboard(self):
        password = self.btn_generate.cget("text")
        pyperclip.copy(password)
        messagebox.showinfo("Copied", "Password copied to clipboard.")

    def show_password(self, password):
        self.btn_generate.config(text=password)

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGeneratorGUI(root)
    root.mainloop()
