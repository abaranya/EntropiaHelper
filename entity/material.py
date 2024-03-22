class Material:
    def __init__(self, name, tt_value, markup_value, category, entry_date):
        self.name = name
        self.tt_value = tt_value
        self.markup_value = markup_value
        self.category = category
        self.entry_date = entry_date

    def to_dict(self):
        return {
            "name": self.name,
            "tt_value": self.tt_value,
            "markup_value": self.markup_value,
            "category": self.category,
            "entry_date": self.entry_date
        }
