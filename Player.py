import random as rd
from Property import Property

class Player:  
    def __init__(self, name: str,start_money = 1500):
        self.money = start_money
        self.properties = {}
        self.name = name
        self.location = 0
        self.active = True
        self.color_sets = set()

    def move(self,doubles=0):
        roll_a = rd.randint(1,6)
        roll_b = rd.randint(1,6)
        
        self.location = (self.location + roll_a + roll_b) % 40
        if roll_a == roll_b:
            if doubles == 2:
                print('Straight to jail buddy!')
                self.location = 10
            else:
                print(f'{roll_a}, {roll_b} Doubles! Roll again.')
                self.move(doubles=doubles+1)
        return roll_a, roll_b, self.location

    def buy_property(self, property: Property):
        if self.money < property.value: return -1
        
        self.money -= property.value
        property.owner = self
        
        if property.color in self.properties:
            self.properties[property.color].add(property)
        else:
            self.properties[property.color] = tuple(property)

    def __eq__(self,other):
        return self.name == other.name
    
    def __str__(self):
        return self.name
    
    def get_player_info(self):
        return (f'{self.name}, {self.location}, ${self.money}, {self.properties}')
    