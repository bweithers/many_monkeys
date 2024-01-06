from BoardParameters import prop_set_sizes, house_prices

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
            # TODO: auction
            self.auction()
        else:
            lander.money -= self.value
            self.owner = lander
            lander.add_property(self)
            print(f"{lander} is the new owner of {self.name}. They paid ${self.value}. They have ${lander.money} left.")
        return 0

    # TODO: lottery? select random player
    def auction(self):
        pass

    def get_house_price(self):
        return house_prices[self.color]
    
    def build_house(self):
        if self.houses >= 5: return -1
        self.owner.money -= self.get_house_price()
        self.houses += 1
        print(f"{self.owner} built house {self.houses} on {self.name}. ", end='')
        return 0
    
    def remove_house(self):
        if self.houses <= 0: return -1
        self.owner.money += self.get_house_price() // 2
        self.houses -= 1
        return 0
    
    def mortgage(self):
        self.mortgaged = True
        self.owner.money += self.value // 2
        return 0
    
    def unmortage(self):
        if self.owner.money < self.value: return -1
        self.mortgaged = False
        self.owner.money -= self.value
        return 0
    
    def pay_rent(self, lander):
        if lander == self.owner: 
            print(f'{lander} owns {self.name}. No rent to pay.')
            return 0
        rent_owed = self.rent_list[self.houses]
        if self.houses == 0 and self.color in self.owner.color_sets: 
            rent_owed *= 2

        if lander.money < rent_owed:
            # TODO: sell houses, mortgage etc
            print(f'Money too low. {lander} is now out.')
            lander.go_out()
        else:
            print(f'{lander} paid {rent_owed} to {self.owner}.')
            self.owner.money += rent_owed
            lander.money -= rent_owed
        return 0
    
    def __eq__(self, other):
        if not other: return False 
        return self.name == other.name
    
    def __str__(self):
        if self.color in ['utility', 'railroad'] or self.houses == 0:
            return f"{self.name}"
        else:
            return f"[{self.houses}]{self.name}"
    
    def __repr__(self):
        if self.color in ['utility', 'railroad'] or self.houses == 0:
            return f"{self.name}"
        else:
            return f"[{self.houses}]{self.name}"
    
    
    def get_info(self):
        return f"{self.name} Owner: {self.owner}, Houses: {self.houses if self.houses <= 5 else 'hotel'}"