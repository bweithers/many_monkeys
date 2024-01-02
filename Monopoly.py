from Player import Player
from Property import Property
from BoardSpace import BoardSpace
from Game import Game
from time import sleep


ansi_colors = {
    'soft_gray': '\033[90m',
    'red': '\033[91m',
    'green': '\033[92m',
    'yellow': '\033[93m',
    'blue': '\033[94m',
    'purple': '\033[95m',
    'cyan': '\033[96m',
    'reset': '\033[0m',
    'bold': '\033[1m',
    'underline': '\033[4m'
    }

g = Game(verbose = True)

def add_players():
    p1 = Player('Jacem')
    p2 = Player('Bot')
    g.players.append(p1)
    g.players.append(p2)
    return 0

def parse_property(csv_line: str) -> Property:
    elements = csv_line.split(', ')
    name, color, value = elements[:3]
    rent_list_size = 0
    match color:
        case 'utility':
            rent_list_size = 2
        case 'railroad':
            rent_list_size = 4
        case _:
            rent_list_size = 5
    rent_list = list(map(int, elements[-rent_list_size:]))
    return Property(name, color, value, rent_list)

def setup_board():
    f = open('./board.csv')
    non_prop_spaces = {0:'Go', 2: 'Community Chest', 4: 'Income Tax', 7: 'Chance', 10: 'Jail', 17: 'Community Chest', 20: 'Free Parking', 22: 'Chance',
                        30: 'Go to Jail', 33: 'Community Chest', 36: 'Chance', 38: 'Luxury Tax'}
    for i in range(40):
        if i in non_prop_spaces:
            b = BoardSpace(name = non_prop_spaces[i], location = i)
        else:
            line = f.readline()
            # p = Property(f'Prop{i}', 'Red', i*100, [i*10**j for j in range(4)])
            p = parse_property(line)
            b = BoardSpace(Property=p, location=i)
        g.board.append(b)
    print_board()
    f.close()
    return 0

def buy_property(player,prop):
    pass

def gameplay_loop():
    current_player = g.players[g.turn]
    a,b,l = current_player.move()
    current_square = g.board[l]
    if g.verbose:
        print(f"{g.players[g.turn]}'s turn. They rolled a {a} and a {b} landing them on {current_square}.")
    # collect rent, buy property, auction, special space event
    current_square.space_action(lander = current_player)
    g.turn = (g.turn+1) % len(g.players) 
    return 0
    
def gameover():
    return len(g.players) <= 1 or g.turn_counter >= 1000

def print_board():
    for i,b in enumerate(g.board[:-1]):
        print(b, end = ' | ')
        if i+1 % 10 == 0:
            print()
    print(g.board[-1])
    
    return 0

def driver():
    add_players()
    setup_board()
    while not gameover():
        gameplay_loop()
        sleep(0.1)
    return 0

driver()