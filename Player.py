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
    
    
    def pay_money(self, amount):
        if self.money >= amount:
            self.money -= amount
            return amount
        else:
            #TODO sell stuff etc
            paid_out = self.money
            self.money = 0
            self.active = False
            return paid_out
        return 0
    #TODO? 
    def trade(self):
        pass
    
    def move(self,doubles=0):
        roll_a, roll_b = rd.randint(1,6), rd.randint(1,6) 

        if self.jailed:
            return roll_a, roll_b, self.location, False

        self.location = (self.location + roll_a + roll_b)
        
        go_flag = self.location >= 40
        self.location%=40

        if go_flag:
            self.money += 200
        
        return roll_a, roll_b, self.location, go_flag

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