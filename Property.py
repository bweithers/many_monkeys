#TODO : Enum property colors? 
class Property:
    def __init__(self, name: str, color, value: int, rent_list: list[int]):
        self.name = name
        self.color = color
        self.rent_list = rent_list
        self.value = value

        self.houses = 0
        self.owner = None
        self.mortgaged = False

    def mortgage(self):
        self.mortgaged = True
        self.owner.money += self.value/2
        return 0
    
    def unmortage(self):
        if self.owner.money < self.value: return -1
        self.mortgaged = False
        self.owner.money -= self.value
        return 0
    
    def __eq__(self, other):
        return self.name == other.name
    
    def __str__(self):
        return self.name