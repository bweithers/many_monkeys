#TODO : Enum property colors? 
house_prices = {'brown': 50,
                'light blue': 50,
                'pink': 100,
                'orange': 100,
                'red': 150,
                'yellow': 150,
                'green': 200,
                'blue': 200
            }
class Property:
    def __init__(self, name: str, color, value: int, rent_list: list[int]):
        self.name = name
        self.color = color
        self.rent_list = rent_list
        self.value = value
        self.houses = 0
        self.mortgaged = False
        self.owner = None

    def get_bought(self,lander):
        if lander.money <= self.value: 
            self.auction()
        else:
            lander.money -= self.value
            self.owner = lander
            lander.properties.add(self)
        return 0

    # lottery? select random player
    def auction(self):
        pass

    def get_house_price(self):
        return house_prices[self.color]
    
    def build_house(self):
        if self.owner.money < self.get_house_price() or self.houses >= 5: return -1
        # TODO Implement even house rules
        self.owner.money -= self.get_house_price()
        self.houses += 1
    
    def remove_house(self):
        if self.houses <= 0: return -1
        self.owner.money += self.get_house_price()//2
        self.houses -= 1
        return 0
    
    def mortgage(self):
        self.mortgaged = True
        self.owner.money += self.value/2
        return 0
    
    def unmortage(self):
        if self.owner.money < self.value: return -1
        self.mortgaged = False
        self.owner.money -= self.value
        return 0
    
    def pay_rent(self, lander):
        if lander == self.owner: return
        rent_owed = self.rent_list[self.houses]
        
        if lander.money < rent_owed:
            print('Money too low.')
        else:
            self.owner.money += rent_owed
            lander.money -= rent_owed
        return 0
    
    def __eq__(self, other):
        if other is None: return self is None
        return self.name == other.name
    
    def __str__(self):
        return self.name