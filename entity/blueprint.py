from entity.material import Material


class Blueprint:
    def __init__(self, name, level, type, crafted_item, class_field, materials, is_limited=False, attempts=None):
        self.name = name
        self.level = level
        self.type = type
        self.crafted_item = crafted_item
        self.class_field = class_field
        self.materials = materials
        self.is_limited = is_limited
        self.attempts = attempts

    def to_dict(self):
        # Serialize each material as a dictionary containing quantity and name
        # materials_dict = [{"quantity": material[0], "name": material[1]} for material in self.materials]

        return {
            "name": self.name,
            "level": self.level,
            "type": self.type,
            "crafted_item": self.crafted_item,
            "class_field": self.class_field,
            "materials": self.materials,  # Use the serialized materials dictionary
            "is_limited": self.is_limited,
            "attempts": self.attempts
        }

