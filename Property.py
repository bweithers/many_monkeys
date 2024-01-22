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
        if lander.money < self.value: 
            # TODO: auction
            outcome = f"{lander} does not have enough money to purchase. Should be an auction, but nothing happens for now."
            self.auction()
        else:
            lander.pay_money(self.value)
            self.owner = lander
            lander.add_property(self)
            outcome = f"{lander} is the new owner of {self.name}. They paid ${self.value}. They have ${lander.money} left."
        return outcome

    # TODO: lottery? select random player
    def auction(self):
        pass

    def get_house_price(self):
        return house_prices[self.color]
    
    def build_house(self):
        if self.houses >= 5: return -1
        self.owner.pay_money(self.get_house_price())
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
        if self.owner.money < self.value: 
            return -1
        self.mortgaged = False
        self.owner.pay_money(self.value)
        return 0
    
    def pay_rent(self, lander):
        outcome = ''

        if lander == self.owner: 
            outcome = f'{lander} owns {self.name}. No rent to pay.'
            return outcome
        rent_owed = self.rent_list[self.houses]

        if self.houses == 0 and self.color in self.owner.color_sets: 
            rent_owed *= 2

        paid_out = lander.pay_money(rent_owed)
        self.owner.money += paid_out
        outcome = f'{lander} paid ${paid_out} to {self.owner}.'
        return outcome
    
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