from Property import Property
from Player import Player

class BoardSpace:
    def __init__(self, location: int, Property: Property = None, name: str = None):
        self.property = Property
        self.location = location
        self.players = []
        self.name = self.property.name if Property else name
        self.owner = None

    def is_property(self):
        return self.property is not None
    
    def is_owned(self):
        return self.owner is not None
    

    def is_go(self):
        return self.location == 0

    # decide if this is a property, if it is do the propety thing else do the thing thing
    def space_action(self, lander: Player = None):
        if self.is_property() and self.is_owned():
            self.property.pay_rent(lander)
        else:
            match self.name:
                case 'Go':
                    lander.money += 400
                #TODO Community Chest/Chance
                case 'Community Chest':
                    lander.money += 50
                case 'Chance':
                    lander.money -= 100
                case 'Jail':
                    pass
                case 'Go to Jail':
                    lander.location = 10
                    lander.jailed = 1
                #TODO? Free parking in middle
                case 'Free Parking':
                    pass
                case 'Income Tax':
                    lander.money -= min(200,.1*(lander.money + sum([p.value for p in lander.properties])))
                case 'Luxury Tax':
                    lander.money -= 100
                    
    def __str__(self):
        return f'{self.name}'


class UnrecognizedSquareException(Exception):
    pass