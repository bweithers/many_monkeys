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

def setup_board():
    for i in range(40):
        p = Property(f'Prop{i}', 'Red', i*100, [i*10**j for j in range(4)])
        b = BoardSpace(p, i)
        g.board.append(b)
    print_board()
    return 0

def gameplay_loop():
    a,b,l = g.players[g.turn].move()
    if g.verbose:
        print(f"{g.players[g.turn]}'s turn. They rolled a {a} and a {b} landing them on {g.board[l]}.")
    g.turn = (g.turn+1) % len(g.players) 
    return 0
    
def gameover():
    return len(g.players) <= 1 or g.turn_counter >= 1000

def print_board():
    for i,b in enumerate(g.board):
        print(b, end = ' | ')
        if i+1 % 10 == 0:
            print()
    
    return 0

def driver():
    add_players()
    setup_board()
    while not gameover():
        gameplay_loop()
        sleep(0.1)
    return 0

driver()