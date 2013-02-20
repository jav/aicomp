import json
import subprocess
import tarfile

# directory in which to unpack packages
# (should be a separate partition and properly sandboxed)
DIR_PREFIX = "tmp"

class GameMaster(object):

    """
    Creates a new GameMaster with two strings, one path
    to each .tar object. 

    The .tar should contain a manifest.json in the root
    directory.
    """
    def __init__(self, player1, player2):
        self.player1 = player1 
        self.player2 = player2

    """
    Fetches the programs corresponding to each player,
    unpacks, spawns to subprocesses and plays a game 
    between them. Then returns the result of the game, or
    an error in case one of the players failed.

    Note: This is completely insecure atm.
    """
    def playMatch(self):
        p1_tar = tarfile.open(self.player1)
        p2_tar = tarfile.open(self.player2)
        p1_tar.extractall(DIR_PREFIX + "/1")
        p2_tar.extractall(DIR_PREFIX + "/2")
        paths = [DIR_PREFIX+"/1/manifest.json",DIR_PREFIX+"/2/manifest.json"]
        files = []
        # open the config files
        for p in paths:
            files.append(open(p))
        # JSON parse them
        configs = map(json.load,files)
        # and close them
        for f in files:
            f.close()

        # TODO: Spawn threads and make them talk.
