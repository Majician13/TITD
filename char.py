import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog, filedialog
import json
import os
import skills
import conditions
import journal

class CharacterSheetApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Character Sheet")
        self.main_app = None  # Add a main_app attribute   
        
        self.journal_window = None  # Define the journal_window attribute
        
        title_label = ttk.Label(root, text="A Torch in the Dark", font=("Helvetica", 20, "bold"))
        title_label.pack(pady=10)

        subtitle_label = ttk.Label(root, text="Character Sheet", font=("Helvetica", 16))
        subtitle_label.pack()

        main_frame = ttk.Frame(root)
        main_frame.pack(padx=10, pady=10, fill="both")

        top_frame = ttk.Frame(main_frame)
        top_frame.pack(fill="x")
        
        # Skills/Meanings Frame
        self.selected_skills = []  # To store selected skills/meanings

        self.skills_frame = ttk.LabelFrame(root, text="Skills/Meanings")
        self.skills_frame.pack(padx=10, pady=10)

        self.skill_dropdown = ttk.Combobox(self.skills_frame, values=list(skills.SKILLS.keys()))
        self.skill_dropdown.bind("<<ComboboxSelected>>", self.add_skill)
        self.skill_dropdown.pack(padx=10, pady=10)

        # Name Frame
        name_frame = ttk.Frame(top_frame)
        name_frame.grid(row=0, column=0, padx=5)

        self.name_label = ttk.Label(name_frame, text="Name:")
        self.name_label.pack()
        self.name_entry = ttk.Entry(name_frame)
        self.name_entry.pack(fill="x") 
        
        # Stash Frame
        stash_frame = ttk.Frame(name_frame)
        stash_frame.pack(fill="x")

        self.stash_label = ttk.Label(stash_frame, text="Stash:")
        self.stash_label.pack(side=tk.LEFT)
        self.stash_values = list(range(21))  # 0 to 20
        self.stash_dropdown = ttk.Combobox(stash_frame, values=self.stash_values, state="readonly")
        self.stash_dropdown.set(0)  # Start stash off at 0
        self.stash_dropdown.pack(side=tk.LEFT)

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
            
        # Conditions/Meanings Frame
        self.selected_conditions = []  # To store selected conditions and meanings

        self.conditions_frame = ttk.LabelFrame(root, text="Conditions/Meanings")
        self.conditions_frame.pack(padx=10, pady=10)

        self.condition_dropdown = ttk.Combobox(self.conditions_frame, values=list(conditions.CONDITIONS.keys()))
        self.condition_dropdown.bind("<<ComboboxSelected>>", self.add_condition)
        self.condition_dropdown.pack(padx=10, pady=10)

        self.selected_conditions_frame = ttk.Frame(self.conditions_frame)
        self.selected_conditions_frame.pack(padx=10, pady=10, fill="both")
        
        # Companions Frame
        companions_frame = ttk.LabelFrame(top_frame, text="Companions/Harm")
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

        # Create the Load Character button
        self.load_button = ttk.Button(root, text="Load Character", command=self.load_character_sheet)
        self.load_button.pack(side="left", padx=10, pady=10)
        
        # Journal Button
        journal_button = ttk.Button(root, text="Journal", command=self.open_journal)
        journal_button.pack(side="right", padx=10, pady=10)

        # XP Frame
        xp_frame = ttk.LabelFrame(top_frame, text="XP")
        xp_frame.grid(row=0, column=3, padx=5, pady=10, rowspan=2)

        self.xp_vars = [tk.IntVar(value=0) for _ in range(10)]  # Start as unchecked
        for var in self.xp_vars:
            ttk.Checkbutton(xp_frame, text="XP", variable=var).pack(anchor=tk.W)
    
    def open_journal(self):
        if self.main_app and self.main_app.journal_app:
            journal_window = tk.Toplevel(self.root)
            journal_window.title("Journal")
            journal_app = journal.JournalApp(journal_window)


    
    # Conditions Functions        
    def add_condition(self, event):
        condition = self.condition_dropdown.get()
        if condition and len(self.selected_conditions) < 3:
            self.selected_conditions.append(condition)
            self.update_selected_conditions()
            if len(self.selected_conditions) == 3:
                self.condition_dropdown.configure(state="disabled")

    def update_selected_conditions(self):
        for widget in self.selected_conditions_frame.winfo_children():
            widget.destroy()

        for i, condition in enumerate(self.selected_conditions):
            label = ttk.Label(self.selected_conditions_frame, text=condition)
            label.grid(row=i, column=0, padx=5, pady=2)

            meaning_label = ttk.Label(self.selected_conditions_frame, text=conditions.CONDITIONS[condition])
            meaning_label.grid(row=i, column=1, padx=5, pady=2)

            delete_button = ttk.Button(self.selected_conditions_frame, text="X", command=lambda c=condition: self.remove_condition(c))
            delete_button.grid(row=i, column=2, padx=5, pady=2)

    def remove_condition(self, condition):
        self.selected_conditions.remove(condition)
        self.update_selected_conditions()
        self.condition_dropdown.configure(state="normal")
    
    # Skill Functions
    def add_skill(self, event):
        """Add a selected skill to the skills frame."""
        selected_skill = self.skill_dropdown.get()
        
        if selected_skill and len(self.selected_skills) < 3 and selected_skill not in self.selected_skills:
            self.selected_skills.append(selected_skill)
            
            skill_frame = ttk.Frame(self.skills_frame)
            skill_frame.pack(fill="x")
            
            skill_label = ttk.Label(skill_frame, text=selected_skill)
            skill_label.pack(side=tk.LEFT, padx=5)
            
            meaning_label = ttk.Label(skill_frame, text=skills.SKILLS[selected_skill])
            meaning_label.pack(side=tk.LEFT)
            
            remove_button = ttk.Button(skill_frame, text="X", command=lambda: self.remove_skill(skill_frame, selected_skill))
            remove_button.pack(side=tk.RIGHT)

            # Disable the skill in the dropdown if all slots are filled
            if len(self.selected_skills) == 3:
                self.skill_dropdown['state'] = 'disabled'
    
    def remove_skill(self, skill_frame, selected_skill):
        """Remove a selected skill from the skills frame."""
        self.selected_skills.remove(selected_skill)
        skill_frame.destroy()

        # Enable the skill dropdown if a slot is available
        if len(self.selected_skills) < 3:
            self.skill_dropdown['state'] = 'normal'
            
    
    
    # Save Function
    def save_character_sheet(self):
        data = {
            "name": self.name_entry.get(),
            "stress": [var.get() for var in self.stress_vars],
            "corruption": [var.get() for var in self.corruption_vars],
            "companions": [{
                "name": entry.get(),
                "checkboxes": [var.get() for var in vars]
            } for entry, vars in zip(self.companion_entries, self.companion_vars)],
            "xp": [var.get() for var in self.xp_vars],
            "skills": self.selected_skills,  # Save selected skills
            "journal": self.journal_app.text.get("1.0", "end-1c")  # Get the journal content
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

            # Load selected skills
            journal_content = data.get("journal", "")  # Get the journal content from the data dictionary
            self.journal_app.text.delete("1.0", "end")  # Clear the current journal content
            self.journal_app.text.insert("insert", journal_content)  # Insert the loaded journal content
            self.selected_skills = data.get("skills", [])
            self.update_skills_frame()
            
        pass

    # Update Skill Function
    def update_skills_frame(self):
        """Update the skills frame based on the selected skills."""
        for widget in self.skills_frame.winfo_children():
            widget.destroy()

        for skill in self.selected_skills:
            skill_frame = ttk.Frame(self.skills_frame)
            skill_frame.pack(fill="x")

            skill_label = ttk.Label(skill_frame, text=skill)
            skill_label.pack(side=tk.LEFT, padx=5)

            meaning_label = ttk.Label(skill_frame, text=skills.SKILLS[skill])
            meaning_label.pack(side=tk.LEFT)

            remove_button = ttk.Button(skill_frame, text="X", command=lambda: self.remove_skill(skill_frame, skill))
            remove_button.pack(side=tk.RIGHT)

        # Disable the skill dropdown if all slots are filled
        if len(self.selected_skills) == 3:
            self.skill_dropdown['state'] = 'disabled'

if __name__ == "__main__":
    root = tk.Tk()
    char_app = CharacterSheetApp(root)
    root.mainloop()
