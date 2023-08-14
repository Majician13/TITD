import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import json
import skills
import conditions
import journal

class CharacterSheetApp:
    def __init__(self, root, main_app):
        self.root = root
        self.main_app = main_app
        # self.main_app = None
        self.journal_window = None
        # Initialize selected conditions and selected skills lists
        self.selected_conditions = []
        self.selected_skills = []
        # Create a dictionary to store skill meanings
        self.skill_meanings = {skill: skills.SKILLS[skill] for skill in skills.SKILLS}

        
        # Create a main frame for the entire character sheet
        main_frame = ttk.Frame(root)
        main_frame.pack(padx=10, pady=10, fill="both")

        # Character Sheet Label
        title_label = ttk.Label(main_frame, text="Character Sheet", font=("Helvetica", 16))
        title_label.grid(row=0, column=0, columnspan=5, sticky="w")

        # Top Frame
        top_frame = ttk.Frame(main_frame)
        top_frame.grid(row=1, column=0, columnspan=5, sticky="w")

        # Name Entry
        self.name_label = ttk.Label(top_frame, text="Name:")
        self.name_label.grid(row=0, column=0, sticky="w")
        self.name_entry = ttk.Entry(top_frame)
        self.name_entry.grid(row=0, column=1, columnspan=2, sticky="w")

        # Stress Frame
        stress_frame = ttk.LabelFrame(top_frame, text="Stress")
        stress_frame.grid(row=1, column=0, rowspan=6, padx=5, pady=10, sticky="w")
        self.stress_vars = [tk.IntVar(value=0) for _ in range(6)]  # Start as unchecked
        for i, var in enumerate(self.stress_vars):
            ttk.Checkbutton(stress_frame, text=f"Stress {i+1}", variable=var).pack(anchor=tk.W)

        # Corruption Frame
        corruption_frame = ttk.LabelFrame(top_frame, text="Corruption")
        corruption_frame.grid(row=1, column=1, rowspan=6, padx=5, pady=10, sticky="w")
        self.corruption_vars = [tk.IntVar(value=0) for _ in range(6)]  # Start as unchecked
        for i, var in enumerate(self.corruption_vars):
            ttk.Checkbutton(corruption_frame, text=f"Corruption {i+1}", variable=var).pack(anchor=tk.W)

        # XP Frame
        xp_frame = ttk.LabelFrame(top_frame, text="XP")
        xp_frame.grid(row=0, column=3, padx=5, pady=10, rowspan=2, sticky="w")
        self.xp_vars = [tk.IntVar(value=0) for _ in range(10)]  # Start as unchecked
        for var in self.xp_vars:
            ttk.Checkbutton(xp_frame, text="XP", variable=var).pack(anchor=tk.W)
            
        # Conditions/Meanings Frame
        conditions_meanings_frame = ttk.LabelFrame(top_frame, text="Conditions/Meanings")
        conditions_meanings_frame.grid(row=1, column=4, columnspan=4, padx=5, pady=10, sticky="w")
        
        # Add Condition Button
        self.add_condition_button = ttk.Button(conditions_meanings_frame, text="Add Condition", command=self.add_condition)
        self.add_condition_button.grid(row=0, column=2, padx=5, pady=10, sticky="w")


        conditions_label = ttk.Label(conditions_meanings_frame, text="Conditions:")
        conditions_label.grid(row=0, column=0, sticky="w")
        self.condition_dropdown = ttk.Combobox(conditions_meanings_frame, values=list(conditions.CONDITIONS.keys()))
        self.condition_dropdown.grid(row=0, column=1, sticky="w")

        self.selected_conditions_frame = ttk.Frame(conditions_meanings_frame)
        self.selected_conditions_frame.grid(row=1, column=0, columnspan=2, sticky="w")

        # Skills/Meanings Frame
        skills_meanings_frame = ttk.LabelFrame(top_frame, text="Skills/Meanings")
        skills_meanings_frame.grid(row=2, column=4, columnspan=4, padx=5, pady=10, sticky="w")

        skills_label = ttk.Label(skills_meanings_frame, text="Skills:")
        skills_label.grid(row=0, column=0, sticky="w")
        self.skill_dropdown = ttk.Combobox(skills_meanings_frame, values=list(skills.SKILLS.keys()))
        self.skill_dropdown.grid(row=0, column=1, sticky="w")

        self.selected_skills_frame = ttk.Frame(skills_meanings_frame)
        self.selected_skills_frame.grid(row=1, column=0, columnspan=2, sticky="w")

        # Bind the add_skill function to the <<ComboboxSelected>> event
        self.skill_dropdown.bind("<<ComboboxSelected>>", self.add_skill)


        # Create a frame for Companions/Harm
        companions_frame = ttk.LabelFrame(main_frame, text="Companions/Harm")
        companions_frame.grid(row=5, column=0, columnspan=2, padx=5, pady=10, sticky="w")

        self.companion_entries = []
        self.companion_vars = []

        for i in range(5):
            entry = ttk.Entry(companions_frame)
            entry.grid(row=i, column=0, columnspan=2, sticky="w")
            self.companion_entries.append(entry)

            vars = [tk.IntVar(value=0) for _ in range(4)]  # Start as unchecked
            for j, var in enumerate(vars):
                ttk.Checkbutton(companions_frame, text=f"Harm {j+1}", variable=var).grid(row=i, column=2+j, sticky="w")
            self.companion_vars.append(vars)
            
        

        # # Save Button
        # save_button = ttk.Button(main_frame, text="Save", command=self.save_character_sheet)
        # save_button.grid(row=8, column=0, padx=10, pady=10, sticky="w")

        # # Load Character Button
        # load_button = ttk.Button(main_frame, text="Load Character", command=self.load_character_sheet)
        # load_button.grid(row=8, column=1, padx=10, pady=10, sticky="w")

        # # Journal Button
        # journal_button = ttk.Button(main_frame, text="Journal", command=self.open_journal)
        # journal_button.grid(row=8, column=2, padx=10, pady=10, sticky="w")
       
    def open_journal(self):
        if self.main_app:
            self.main_app.open_journal()

    def add_condition(self):
        condition = self.condition_dropdown.get()

        if condition and len(self.selected_conditions) < len(self.selected_skills):
            self.selected_conditions.append(condition)
            self.update_selected_conditions()
            if len(self.selected_conditions) == len(self.selected_skills):
                self.add_condition_button.configure(state="disabled")
            self.condition_dropdown.set("")  # Clear the dropdown selection

    def remove_condition(self, condition):
        self.selected_conditions.remove(condition)
        self.update_selected_conditions()
        self.add_condition_button.configure(state="normal")

    def update_selected_conditions(self):
        for widget in self.selected_conditions_frame.winfo_children():
            widget.destroy()

        for i, condition in enumerate(self.selected_conditions):
            condition_frame = ttk.Frame(self.selected_conditions_frame)
            condition_frame.grid(row=i, column=0, padx=5, pady=2, sticky="w")

            label = ttk.Label(condition_frame, text=condition)
            label.grid(row=0, column=0, padx=5, pady=2)

            meaning_label = ttk.Label(condition_frame, text=conditions.CONDITIONS[condition])
            meaning_label.grid(row=0, column=1, padx=5, pady=2)

            delete_button = ttk.Button(condition_frame, text="X", command=lambda c=condition: self.remove_condition(c))
            delete_button.grid(row=0, column=2, padx=5, pady=2)

    
    # Skill Functions
    def add_skill(self, event):
        selected_skill = self.skill_dropdown.get()

        if selected_skill and len(self.selected_skills) < 10 and selected_skill not in self.selected_skills:
            self.selected_skills.append(selected_skill)
            self.update_skills_frame()
            self.skill_dropdown.set("")  # Clear the dropdown selection
    
    def remove_skill(self, skill):
        """Remove a selected skill from the selected_skills list and update the skills frame."""
        self.selected_skills.remove(skill)
        self.update_skills_frame()
            
    # Update Skill Function
    def update_skills_frame(self):
        for widget in self.selected_skills_frame.winfo_children():
            widget.destroy()

        for skill in self.selected_skills:
            skill_frame = ttk.Frame(self.selected_skills_frame)
            skill_frame.pack(fill="x")

            skill_label = ttk.Label(skill_frame, text=skill)
            skill_label.pack(side=tk.LEFT, padx=5)

            meaning_label = ttk.Label(skill_frame, text=self.skill_meanings[skill])
            meaning_label.pack(side=tk.LEFT)

            remove_button = ttk.Button(skill_frame, text="X", command=lambda s=skill: self.remove_skill(s))
            remove_button.pack(side=tk.RIGHT)

        # Update the skill dropdown values
        remaining_skills = [s for s in skills.SKILLS.keys() if s not in self.selected_skills]
        self.skill_dropdown['values'] = remaining_skills

        # Disable the skill dropdown if the maximum number of skills is reached
        if len(self.selected_skills) >= 10:
            self.skill_dropdown['state'] = 'disabled'
        else:
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

    

if __name__ == "__main__":
    root = tk.Tk()
    char_app = CharacterSheetApp(root)
    root.mainloop()
