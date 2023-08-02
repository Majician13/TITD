import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog, filedialog
import json
import os

class CharacterSheetApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Character Sheet")

        title_label = ttk.Label(root, text="A Torch in the Dark", font=("Helvetica", 20, "bold"))
        title_label.pack(pady=10)

        subtitle_label = ttk.Label(root, text="Character Sheet", font=("Helvetica", 16))
        subtitle_label.pack()

        self.name_label = ttk.Label(root, text="Name:")
        self.name_label.pack(pady=5)
        self.name_entry = ttk.Entry(root)
        self.name_entry.pack(pady=5)

        stress_frame = ttk.LabelFrame(root, text="Stress")
        stress_frame.pack(padx=10, pady=10)

        self.stress_vars = [tk.IntVar() for _ in range(6)]
        for i, var in enumerate(self.stress_vars):
            ttk.Checkbutton(stress_frame, variable=var).pack(anchor=tk.W)

        corruption_frame = ttk.LabelFrame(root, text="Corruption")
        corruption_frame.pack(padx=10, pady=10)

        self.corruption_vars = [tk.IntVar() for _ in range(6)]
        for i, var in enumerate(self.corruption_vars):
            ttk.Checkbutton(corruption_frame, variable=var).pack(anchor=tk.W)

        # Create the Save button
        self.save_button = ttk.Button(root, text="Save", command=self.save_character_sheet)
        self.save_button.pack(side="left", padx=10, pady=10)

        # Create the Load button
        self.load_button = ttk.Button(root, text="Load", command=self.load_character_sheet)
        self.load_button.pack(side="left", padx=10, pady=10)

    def save_character_sheet(self):
        character_data = {
            "name": self.name_entry.get(),
            "stress": [var.get() for var in self.stress_vars],
            "corruption": [var.get() for var in self.corruption_vars]
            # Add other fields to character_data as needed
        }
        filename = simpledialog.askstring("Save Character Sheet", "Enter a filename:", parent=self.root)
        if filename:
            filename += ".json"
            with open(filename, "w") as f:
                json.dump(character_data, f)
            print(f"Character sheet saved as '{filename}'.")

    def load_character_sheet(self):
        existing_files = [filename for filename in os.listdir() if filename.endswith(".json")]
        if existing_files:
            chosen_file = filedialog.askopenfilename(title="Choose Character Sheet to Load", filetypes=[("JSON Files", "*.json")])
            if chosen_file:
                with open(chosen_file, "r") as f:
                    character_data = json.load(f)

                self.name_entry.delete(0, tk.END)
                self.name_entry.insert(0, character_data["name"])

                for i, var in enumerate(self.stress_vars):
                    var.set(character_data["stress"][i])

                for i, var in enumerate(self.corruption_vars):
                    var.set(character_data["corruption"][i])

                # Add code to update other fields as needed

                print(f"Character sheet loaded from '{chosen_file}'.")

        else:
            print("No saved character sheets found.")

if __name__ == "__main__":
    root = tk.Tk()
    char_app = CharacterSheetApp(root)
    root.mainloop()
