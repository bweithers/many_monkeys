import random as rd
from Property import Property
from BoardParameters import prop_set_sizes, house_prices
class Player:  
    def __init__(self, name: str,start_money: int = 1500, color_preferences: list[str] = ['brown', 'light blue','pink','orange','red','yellow','green','blue']):
        self.money = start_money
        self.properties = []
        self.name = name
        self.location = 0
        self.active = True
        self.color_counts = {s: 0 for s in prop_set_sizes}
        self.color_sets = []
        self.jailed = 0
        self.color_preferences = color_preferences
    
    def go_out(self):
        self.active = False

    #TODO? 
    def trade(self):
        pass
    
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
            self.money += 200
            self.location %= 40
            print(f'{self.name} passed Go. Collect $200 up to: {self.money}. ')
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
        if property.color in ['utility', 'railroad']:
            self.properties.append(property)
            return 0
        if property.color in self.color_counts and self.color_counts[property.color] >= prop_set_sizes[property.color]:
            raise PropertySetSizeException
        self.color_counts[property.color] += 1
        self.properties.append(property)
        if self.color_counts[property.color] == prop_set_sizes[property.color]:
            self.color_sets.append(property.color)
        return 0 
        
    def can_build_house(self):
        return any([(self.money // house_prices[c]) > 0 for c in self.color_sets])
  
    # choose a color, choose an amount, 
    def build_houses(self):
        # choose color according to preferences
        # choose amount according to cutoff rules (all, above x, above x% max rent, * turn counter etc)
        if self.money <= self.get_house_cutoff(): return
        prop = self.choose_house_prop()
        if prop:
            prop.build_house()
        
            # call again to build more houses.. Will prop.build_house properly remove money to hit stopping condition?
            self.build_houses()
            
        return 0

    def choose_house_prop(self) -> Property:
        # pick our favorite color according to preferences dict
        ordered_colors = sorted(self.color_sets, key = lambda x: self.color_preferences.index(x))
        for color in ordered_colors:
            # list of props from this color
            c_props = [p for p in self.properties if p.color == color and p.houses < 5]
            # make sure we have buildable props
            if c_props: 
                props = sorted([p for p in c_props], key = lambda x: (x.houses, -1*x.value))
                return props[0]
        return 0



    def get_house_cutoff(self):
        return 200
    
    def __eq__(self,other):
        if other is None: return self is None
        return self.name == other.name
    
    def __str__(self):
        return self.name
    
    def get_player_info(self):
        return (f'{self.name}, {self.location}, ${self.money}, {self.properties}')
    
class PropertySetSizeException(Exception):
    pass