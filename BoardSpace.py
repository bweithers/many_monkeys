from Property import Property

class BoardSpace:
    def __init__(self, Property: Property, location: int):
        self.property = Property
        self.location = location
        self.players = []
        self.name = self.property.name if self.property else self.location

    def is_property(self):
        return self.property is None
    
    def is_go(self):
        return self.location == 0

    def __str__(self):
        return f'Space: {self.name}'