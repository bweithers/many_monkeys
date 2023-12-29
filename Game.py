class Game:
    def __init__(self, verbose: bool = True) -> None:        
        self.players = []
        self.board = []
        self.turn = 0
        self.turn_counter = 0
        self.verbose = verbose