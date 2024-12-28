class Perfume:
    def __init__(self, name):
        self.name = name
        self.notes = {"Top Notes": [], "Middle Notes": [], "Base Notes": []}

    def add_note(self, category, compound, concentration):
        """Add a compound to a specific fragrance note."""
        if category in self.notes:
            self.notes[category].append((compound, concentration))
        else:
            raise ValueError("Invalid category. Choose from: 'Top Notes', 'Middle Notes', 'Base Notes'.")

    def describe(self):
        """Describe the perfume blend."""
        description = f"Perfume: {self.name}\n"
        for category, compounds in self.notes.items():
            description += f"{category}:\n"
            for compound, concentration in compounds:
                description += f"  - {compound} ({concentration}%)\n"
        return description


# Example: Creating a Perfume Blend
perfume = Perfume("Mystic Blossom")
perfume.add_note("Top Notes", "Limonene (Citrus)", 15)
perfume.add_note("Middle Notes", "Linalool (Floral)", 25)
perfume.add_note("Base Notes", "Vanillin (Sweet)", 10)

print(perfume.describe())
