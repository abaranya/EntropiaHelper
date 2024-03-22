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
            "materials": self.materials,
            "is_limited": self.is_limited,
            "attempts": self.attempts
        }
