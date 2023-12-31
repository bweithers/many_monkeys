from Property import Property

class BoardSpace:
    def __init__(self, Property: Property, location: int):
        self.property = Property
        self.location = location
        self.players = []
        self.name = self.property.name

    def __init__(self, name: str, location: int):
        self.location = location
        self.players = []
        self.name = name 

    def is_property(self):
        return self.property is None
    
    def is_go(self):
        return self.location == 0

    def __str__(self):
        return f'BS:{self.name}'