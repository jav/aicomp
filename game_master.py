import json
import os
import subprocess
import tarfile
import sys

from threading import Thread

# directory in which to unpack packages
# (should be a separate partition and properly sandboxed)
DIR_PREFIX = "tmp"

class ProcessHandler():
    last_line = ""

    def __init__(self, args):
        self.process = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def communicate(self,input_list):
        for data in input_list:
            self.process.stdin.write(data)

    def readline(self): 
        def readline_threaded():
            self.last_line = self.process.stdout.readline()
        t = Thread(target=readline_threaded)
        t.start()
        t.join(1)
        if t.isAlive():
            print "ERROR"
        return self.last_line


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

        config_paths = [DIR_PREFIX+"/1/manifest.json",DIR_PREFIX+"/2/manifest.json"]
        files = []
        # open the config files
        for p in config_paths:
            files.append(open(p))
        # JSON parse them
        configs = map(json.load,files)
        # and close them
        for f in files:
            f.close()

        # make the players talk!
        player1_bin_args = ["python",os.getcwd()+"/"+DIR_PREFIX+"/1/" + configs[0]['executable']]
        player2_bin_args = ["python",os.getcwd()+"/"+DIR_PREFIX+"/2/" + configs[1]['executable']]
        
        p1 = ProcessHandler(player1_bin_args)
        p2 = ProcessHandler(player2_bin_args)
        
        # p1 thinks about a number
        p1.communicate("think\n")
        number = int(p1.readline())
        
        # p2 tries to guess the number
        p2.communicate("guess\n")
        guessed = int(p2.readline())

        print "thought about " + str(number) + ", guessed " + str(guessed)
