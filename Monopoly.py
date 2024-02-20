from Player import Player, Trade
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

def handle_trade(t: Trade):
    
    fr, to = t.from_player, t.to_player
    #flip trade?
    if t.money < 0:
        pass

    for p in t.inbound_props:
        p.owner = fr
        to.properties.remove(p)
        fr.properties.append(p)
    
    for p in t.outbound_props:
        p.owner = to
        fr.properties.remove(p)
        to.properties.append(p)
    
    to.money += fr.pay_money(t.money)

def gameplay_loop():
    current_player = g.players[g.turn]
    if not current_player.active: return 
    print(f"Turn {g.turn_counter}: {current_player}. ")

    # Has to happen when they go out... Can't collect rent after busting.
    # this shouldn't get triggered.. out ppl should have loc set to -1 as it happens
    
    # if current_player.active == False: 
    #     g.players.remove(current_player)
    #     return 0
    
    a,b,l,f = current_player.move()
    current_square = g.board[l] 
    # Handle Jail first
    if current_player.jailed >= 1:
        print(f'Starting {current_player.jailed} turn in jail. ', end='')
        if a == b:
            print(f'Rolled {a} doubles. Out of jail.')
            current_player.jailed = 0
            gameplay_loop()
            return
        if current_player.jailed >=3:
            current_player.pay_money(50)
            current_player.jailed = 0
            print(f'Finished third turn in jail. Paying to be out next turn.')
        else:
            print(f"Didn't roll doubles. Staying in jail.")
            current_player.jailed += 1
    
    if g.verbose:
        print(f'Rolled {a} and {b}. Landed on {current_square}. ', end='')
        if current_square == 'Jail':
            print('Just visiting. ',end='')
        if f:
            print(f'{current_player} passed Go. They collected $200 up to ${current_player.money}. ', end='')
    

    # collect rent, buy property, auction, special space event
    outcome = current_square.space_action(lander = current_player)
    
    if g.verbose:
        print(outcome)
    
    if current_player.active == False:
        print(f'{current_player} is out!')
        g.turn = (g.turn+1) % len(g.players) 
        return 0

    if current_player.can_build_house():
        current_player.build_houses()
    t = current_player.trade([p for p in g.players if p != current_player])
    if t:
        handle_trade(t)
    if a == b:
        print(f'{current_player} rolled doubles, they are continuing their turn.')
        gameplay_loop()
        return 
    
    g.turn = (g.turn+1) % len(g.players) 

    if g.verbose:
        print()

    return 0
    
def gameover():
    return sum([int(p.active) for p in g.players]) <= 1 or g.turn_counter >= 1000

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
        print(f"{p}: ${p.money}, {sorted(p.properties, key = lambda x: x.color)}, {len(p.properties)}")


def driver():
    add_players()
    setup_board()
    while not gameover():
        gameplay_loop()
        g.turn_counter += 1
    cleanup_game()
    return 0

driver()