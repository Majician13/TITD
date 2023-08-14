import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext

class JournalApp:
    def __init__(self, root):
        self.root = root
        
        
        # Add a text entry box above the journal text area
        self.entry_box = ttk.Entry(root)
        self.entry_box.pack(fill="x", padx=10, pady=(10, 0))  # Add padding only at the top

        # Add an "Enter" button next to the entry box
        self.enter_button = ttk.Button(root, text="Enter", command=self.move_text_to_journal)
        self.enter_button.pack(side="top", padx=10, pady=5)

        self.text = scrolledtext.ScrolledText(root, wrap=tk.WORD, state=tk.DISABLED)
        self.text.pack(fill="both", expand=True, padx=10, pady=10)

    def show_journal_window(self):
        self.root.deiconify()  # Show the journal window
    
    def move_text_to_journal(self):
        # Get the text from the entry box
        entry_text = self.entry_box.get()

        # Clear the entry box
        self.entry_box.delete(0, "end")

        if entry_text:
            # Append the entered text to the journal text area
            self.text.config(state=tk.NORMAL)
            self.text.insert(tk.END, entry_text + "\n")
            self.text.config(state=tk.DISABLED)
    
    def clear_entries(self, category):
        # Clear previous entries with the specified category tag
        self.text.tag_remove(category, "1.0", tk.END)
    
    def add_entry(self, category, entry, color):
        # Clear previous entries with the specified tag
        self.text.tag_remove("entry", "1.0", tk.END)
        
        formatted_entry = f"[{category}] {entry}\n"
        self.text.config(state=tk.NORMAL)
        self.text.insert(tk.END, formatted_entry, color)
        self.text.config(state=tk.DISABLED)


    def save_journal(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt", filetypes=[("Text Files", "*.txt")], initialdir="./journals"
        )
        if file_path:
            try:
                with open(file_path, "w") as file:
                    file.write(self.text.get("1.0", "end-1c"))
            except Exception as e:
                print("Error saving journal:", e)

    def load_journal(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")], initialdir="./journals")
        if file_path:
            try:
                with open(file_path, "r") as file:
                    self.text.config(state=tk.NORMAL)
                    self.text.delete("1.0", "end")
                    self.text.insert("insert", file.read())
                    self.text.config(state=tk.DISABLED)
            except Exception as e:
                print("Error loading journal:", e)

if __name__ == "__main__":
    root = tk.Tk()
    journal_app = JournalApp(root)
    root.mainloop()
