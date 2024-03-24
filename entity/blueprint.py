from entity.material import Material


class Blueprint:
    def __init__(self, name, level, type, class_field, materials, is_limited=False, attempts=None):
        self.name = name
        self.level = level
        self.type = type
        self.class_field = class_field
        self.materials = materials
        self.is_limited = is_limited
        self.attempts = attempts

    def to_dict(self):
        return {
            "name": self.name,
            "level": self.level,
            "type": self.type,
            "class_field": self.class_field,
            "materials": [material.to_dict() for material in self.materials],  # Serialize each material to a dictionary
            "is_limited": self.is_limited,
            "attempts": self.attempts
        }
