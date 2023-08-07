import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog, filedialog
from tkinter import scrolledtext

class JournalApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Journal")

        self.text = scrolledtext.ScrolledText(root, wrap=tk.WORD)
        self.text.pack(fill="both", expand=True, padx=10, pady=10)

        save_button = ttk.Button(root, text="Save", command=self.save_journal)
        save_button.pack(side="left", padx=10, pady=10)

        load_button = ttk.Button(root, text="Load", command=self.load_journal)
        load_button.pack(side="left", padx=10, pady=10)

    def add_entry(self, category, entry, color):
        formatted_entry = f"[{category}] {entry}\n"
        self.text.config(state=tk.NORMAL)
        self.text.insert(tk.END, formatted_entry, color)
        self.text.config(state=tk.DISABLED)

    def save_journal(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        if file_path:
            with open(file_path, "w") as file:
                file.write(self.text.get("1.0", "end-1c"))

    def load_journal(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if file_path:
            with open(file_path, "r") as file:
                self.text.delete("1.0", "end")
                self.text.insert("insert", file.read())

# ... (character sheet code)

if __name__ == "__main__":
    root = tk.Tk()
    journal_app = JournalApp(root)
    root.mainloop()
