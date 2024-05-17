class Item:
    def __init__(self, name, description, category, value, markup, tt_cost, full_cost, cost_markup):
        self.name = name
        self.description = description
        self.category = category
        self.value = value
        self.markup = markup
        self.tt_cost = tt_cost
        self.full_cost = full_cost
        self.cost_markup = cost_markup

    def to_dict(self):
        return {
            "name": self.name,
            "description": self.description,
            "category": self.category,
            "value": self.value,
            "markup": self.markup,
            "tt_cost": self.tt_cost,
            "full_cost": self.full_cost,
            "cost_markup": self.cost_markup
        }
