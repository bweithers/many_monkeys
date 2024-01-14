from Property import Property
from Player import Player
from BoardParameters import prop_set_sizes, house_prices
class BoardSpace:
    def __init__(self, location: int, Property: Property = None, name: str = None):
        self.property = Property
        self.location = location
        self.players = []
        self.name = self.property.name if Property else name
        self.owner = None

    def is_property(self):
        return bool(self.property) 
    
    def is_owned(self):
        return bool(self.owner) 

    def is_go(self):
        return self.location == 0

    # decide if this is a property, if it is do the propety thing else do the thing thing
    def space_action(self, lander: Player = None):
        if self.is_property():
            print(f'{self.property} is a property. ', end='')
            if self.is_owned():
                print(f"It's owned. ", end ='')
                self.property.pay_rent(lander)
            else:
                print(f"It's unowned. ", end ='')
                self.property.get_bought(lander)
                self.owner = self.property.owner
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
                    penalty = min(200,round(.1*(lander.money + sum([p.value for p in lander.properties])),0))
                    print(f'{lander} paid ${penalty}. ', end='')
                    lander.money -= penalty
                case 'Luxury Tax':
                    penalty = 100
                    lander.money -= penalty
                    print(f'{lander} paid ${penalty}. ', end='')
        if lander.money < 0:
            lander.active = False
        return 0
    
    def __str__(self):
        return f'{self.name}'


class UnrecognizedSquareException(Exception):
    pass