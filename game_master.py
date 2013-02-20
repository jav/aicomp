class GameMaster(object):

    """
    Creates a new GameMaster with the given players.
    """
    def __init__(self, player1, player2):
        self.player1 = player1 
        self.player2 = player2

    """
    Fetches the programs corresponding to each player,
    unpacks, spawns to subprocesses and plays a game 
    between them. Then returns the result of the game, or
    an error in case one of the players failed.
    """
    def playMatch(self):
        # TODO:
        # fetch player data
        # unpack
        # spawn the processes, use stdio to communicate
        # kill processes when game is over
        # return match result
        return
        
