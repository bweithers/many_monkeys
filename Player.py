import random as rd
from Property import Property
from BoardParameters import prop_set_sizes, house_prices

class Trade:
    def __init__(self, outbound_props: list[Property],inbound_props: list[Property], money: int, from_player, to_player):
        # money will be positive if inbound, negative if outbound
        self.outbound_props, self.inbound_props, self.money = outbound_props, inbound_props, money
        self.from_player, self.to_player = from_player, to_player

    def flip(self):
        return Trade(outbound_props=self.inbound_props, inbound_props=self.outbound_props, money=-self.money, from_player=self.to_player, to_player=self.from_player)
    
    def __repr__(self):
        return f'Give: {self.outbound_props} For: {self.inbound_props} Cash: ${self.money}'

class PropertySetSizeException(Exception):
    pass

class Player:  
    def __init__(self, name: str,start_money: int = 1500, score_trade = lambda x: 1, color_preferences: list[str] = ['brown', 'light blue','pink','orange','red','yellow','green','blue']):
        self.money = start_money
        self.properties = []
        self.name = name
        self.location = 0
        self.active = True
        self.color_counts = {s: 0 for s in prop_set_sizes}
        self.color_sets = []
        self.jailed = 0
        self.score_trade = score_trade
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
    def trade(self, other_players):
        possible = self.generate_trades(other_players)
        for t in sorted(possible, key = lambda x: possible[x],reverse=True):
            # print(t, possible[t], end= '; ')
            # ask them to score it
            outcome = t.to_player.score_trade(t.flip())
            if outcome > 0:
                return t
        

    def move(self,doubles=0):
        roll_a, roll_b = rd.randint(1,6), rd.randint(1,6) 

        if self.jailed:
            return roll_a, roll_b, self.location, False

        self.location = (self.location + roll_a + roll_b)
        
        go_flag = self.location > 40
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
    
    def generate_trades(self, other_players: list):
        # generate list of possible trades, and score them
        trades = {}
        
        for op in other_players:
            # start with one-for-one trades
            for op_p in op.properties:
                for p in self.properties:
                    t = Trade(outbound_props=[p], inbound_props=[op_p], money=0, from_player=self, to_player=op)
                    score = self.score_trade(t)
                    if score >= 0:
                        trades[t] = score
        
        return trades
    
    # def score_trade(self, t: Trade) -> float:
    #     # straight facevalue valuation
    #     outbound, inbound = 0,0
    #     for p in t.inbound_props:
    #         inbound += p.value
    #     for p in t.outbound_props:
    #         outbound += p.value
    #     inbound += t.money
    #     return inbound - outbound

    def __eq__(self,other):
        if other is None: return self is None
        return self.name == other.name
    
    def __str__(self):
        return self.name
    
    def get_player_info(self):
        return (f'{self.name}, {self.location}, ${self.money}, {self.properties}')
    