from Player import Player
from Property import Property
from BoardSpace import BoardSpace
from Game import Game
from time import sleep


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
    value = int(value)
    rent_list_size = 0
    match color:
        case 'utility':
            rent_list_size = 2
        case 'railroad':
            rent_list_size = 4
        case _:
            rent_list_size = 6
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
            p = parse_property(line)
            b = BoardSpace(Property=p, location=i)
        g.board.append(b)
    print_board()
    f.close()
    return 0

#TODO: take in all turn events, print in one place in order.
def print_turn():
    pass

def gameplay_loop():
    current_player = g.players[g.turn]
    # Has to happen when they go out... Can't collect rent after busting.
    # this shouldn't get triggered.. out ppl should have loc set to -1 as it happens
    # if current_player.active == False: 
    #     g.players.remove(current_player)
    #     return 0
    a,b,l = current_player.take_turn()
    if l == -1:
        print(f'{current_player} is out!')
        g.players.remove(current_player)
        return 0
    current_square = g.board[l]
    if g.verbose:
        if g.players[g.turn].jailed >= 1:
            print(f"{g.players[g.turn]}'s turn. They rolled a {a} and a {b}. They are still in Jail.")
        else:
            print(f"{g.players[g.turn]}'s turn. They have ${g.players[g.turn].money}. They rolled a {a} and a {b} landing them on {current_square}.")
    # collect rent, buy property, auction, special space event
    current_square.space_action(lander = current_player)
    if g.verbose:
        print_turn()
    g.turn = (g.turn+1) % len(g.players) 
    if g.verbose:
        print()
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

def cleanup_game():
    print(f"Game Over! Game lasted: {g.turn_counter} Turns!")
    for p in g.players:
        print(f"{p}: ${p.money}, {p.properties}, {len(p.properties)}")


def driver():
    add_players()
    setup_board()
    while not gameover():
        gameplay_loop()
        g.turn_counter += 1
    cleanup_game()
    return 0

driver()