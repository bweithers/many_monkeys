import random as rd
from Property import Property
from BoardParameters import prop_set_sizes, house_prices
class Player:  
    def __init__(self, name: str,start_money: int = 1500):
        self.money = start_money
        self.properties = []
        self.name = name
        self.location = 0
        self.active = True
        self.color_counts = {s: 0 for s in prop_set_sizes}
        self.color_sets = []
        self.jailed = 0

    def move(self,doubles=0):
        roll_a = rd.randint(1,6)
        roll_b = rd.randint(1,6)
        
        if self.jailed: 
            if roll_a == roll_b:
                self.jailed = 0
                print(f'{roll_a} Doubles. Out of jail! Roll again to move.')
                return self.move(doubles = 1)
            else:
                self.jailed += 1
                return roll_a, roll_b, self.location
            
        
        self.location = (self.location + roll_a + roll_b)
        if self.location >= 40:
            print(f'{self.name} passed Go. Collect $200 up to: {self.money}. ')
            self.money += 200
            self.location %= 40
        
        if roll_a == roll_b:
            if doubles == 2:
                print('Straight to jail buddy!')
                self.location = 10
                self.jailed = 1
            else:
                # TODO: cant skip board action
                print(f'{roll_a}, {roll_b} Doubles! Roll again.')
                return self.move(doubles=doubles+1)
        return roll_a, roll_b, self.location

    def add_property(self, property: Property):
        if self.color_counts[property.color] >= prop_set_sizes[property.color]:
            raise PropertySetSizeException
        self.color_counts[property.color] += 1
        self.properties.append(property)
        if self.color_counts[property.color] == prop_set_sizes[property.color]:
            self.color_sets.append(property.color)
        return 0 
        
    def can_build_house(self):
        if not self.color_sets:
            return False
        # check which colors we can build houses on
        else:
            possible_houses = {c: self.money // house_prices[c] for c in prop_set_sizes}
        return possible_houses
  
    # choose a color, choose an amount, 
    def build_houses(self):
        pass
    def __eq__(self,other):
        if other is None: return self is None
        return self.name == other.name
    
    def __str__(self):
        return self.name
    
    def get_player_info(self):
        return (f'{self.name}, {self.location}, ${self.money}, {self.properties}')
    
class PropertySetSizeException(Exception):
    pass