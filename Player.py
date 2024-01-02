import random as rd
from Property import Property

class Player:  
    def __init__(self, name: str,start_money: int = 1500):
        self.money = start_money
        self.properties = set()
        self.name = name
        self.location = 0
        self.active = True
        self.color_sets = set()
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
            
        
        self.location = (self.location + roll_a + roll_b) % 40
        if roll_a == roll_b:
            if doubles == 2:
                print('Straight to jail buddy!')
                self.location = 10
                self.jailed = 1
            else:
                print(f'{roll_a}, {roll_b} Doubles! Roll again.')
                return self.move(doubles=doubles+1)
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
        if other is None: return self is None
        return self.name == other.name
    
    def __str__(self):
        return self.name
    
    def get_player_info(self):
        return (f'{self.name}, {self.location}, ${self.money}, {self.properties}')
    