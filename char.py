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

        main_frame = ttk.Frame(root)
        main_frame.pack(padx=10, pady=10, fill="both")

        top_frame = ttk.Frame(main_frame)
        top_frame.pack(fill="x")

        # Name Frame
        name_frame = ttk.Frame(top_frame)
        name_frame.grid(row=0, column=0, padx=5)

        self.name_label = ttk.Label(name_frame, text="Name:")
        self.name_label.pack()
        self.name_entry = ttk.Entry(name_frame)
        self.name_entry.pack(fill="x")

        # Stress Frame
        stress_frame = ttk.LabelFrame(top_frame, text="Stress")
        stress_frame.grid(row=0, column=1, padx=5)

        self.stress_vars = [tk.IntVar(value=0) for _ in range(6)]  # Start as unchecked
        for i, var in enumerate(self.stress_vars):
            ttk.Checkbutton(stress_frame, variable=var).pack(anchor=tk.W)

        # Corruption Frame
        corruption_frame = ttk.LabelFrame(top_frame, text="Corruption")
        corruption_frame.grid(row=0, column=2, padx=5)

        self.corruption_vars = [tk.IntVar(value=0) for _ in range(6)]  # Start as unchecked
        for i, var in enumerate(self.corruption_vars):
            ttk.Checkbutton(corruption_frame, variable=var).pack(anchor=tk.W)

        # Companions Frame
        companions_frame = ttk.LabelFrame(top_frame, text="Companions")
        companions_frame.grid(row=1, column=0, columnspan=3, padx=5, pady=10)

        self.companion_entries = []
        self.companion_vars = []

        for i in range(5):
            companion_frame = ttk.Frame(companions_frame)
            companion_frame.pack(fill="x")

            companion_entry = ttk.Entry(companion_frame)
            companion_entry.pack(side=tk.LEFT, padx=5)
            self.companion_entries.append(companion_entry)

            companion_vars = [tk.IntVar(value=0) for _ in range(4)]  # Start as unchecked
            for var in companion_vars:
                ttk.Checkbutton(companion_frame, variable=var).pack(side=tk.LEFT)
            self.companion_vars.append(companion_vars)

        # Create the Save button
        self.save_button = ttk.Button(root, text="Save", command=self.save_character_sheet)
        self.save_button.pack(side="left", padx=10, pady=10)

        # Create the Load button
        self.load_button = ttk.Button(root, text="Load", command=self.load_character_sheet)
        self.load_button.pack(side="left", padx=10, pady=10)

        # XP Frame
        xp_frame = ttk.LabelFrame(top_frame, text="XP")
        xp_frame.grid(row=0, column=3, padx=5, pady=10, rowspan=2)

        self.xp_vars = [tk.IntVar(value=0) for _ in range(10)]  # Start as unchecked
        for var in self.xp_vars:
            ttk.Checkbutton(xp_frame, text="XP", variable=var).pack(anchor=tk.W)

    def save_character_sheet(self):
        data = {
            "name": self.name_entry.get(),
            "stress": [var.get() for var in self.stress_vars],
            "corruption": [var.get() for var in self.corruption_vars],
            "companions": [{
                "name": entry.get(),
                "checkboxes": [var.get() for var in vars]
            } for entry, vars in zip(self.companion_entries, self.companion_vars)],
            "xp": [var.get() for var in self.xp_vars]
        }

        filename = filedialog.asksaveasfilename(defaultextension=".json", initialdir="./games")
        if filename:
            with open(filename, "w") as file:
                json.dump(data, file)

    def load_character_sheet(self):
        filename = filedialog.askopenfilename(defaultextension=".json", initialdir="./games")
        if filename:
            with open(filename, "r") as file:
                data = json.load(file)

            self.name_entry.delete(0, tk.END)
            self.name_entry.insert(0, data["name"])

            for var, value in zip(self.stress_vars, data["stress"]):
                var.set(value)

            for var, value in zip(self.corruption_vars, data["corruption"]):
                var.set(value)

            for entry, companions_data in zip(self.companion_entries, data["companions"]):
                entry.delete(0, tk.END)
                entry.insert(0, companions_data["name"])

                for var, value in zip(self.companion_vars[0], companions_data["checkboxes"]):
                    var.set(value)

            for var, value in zip(self.xp_vars, data["xp"]):
                var.set(value)

if __name__ == "__main__":
    root = tk.Tk()
    char_app = CharacterSheetApp(root)
    root.mainloop()
