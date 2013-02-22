import json
import os
import subprocess
import tarfile
import sys
import time
import urllib2

from threading import Thread

# directory in which to unpack packages
# (should be a separate partition and properly sandboxed)
DIR_PREFIX = "tmp"

class ProcessHandler():
    last_line = ""

    def __init__(self, args):
        self.process = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def communicate(self,input_list):
        # TODO: blocking?
        for data in input_list:
            self.process.stdin.write(data)

    def readline(self): 
        def readline_threaded():
            self.last_line = self.process.stdout.readline()
        t = Thread(target=readline_threaded)
        t.start()
        t.join(0.5) 
        if t.isAlive():
            print "ERROR"
        return self.last_line


class GameMaster(object):

    """
    Create a GameMaster with a coordinator. GameMaster will poll
    the Coordinator for jobs.
    """
    def __init__(self, coordinator):
        self.coordinator = coordinator

    """
    Enter work-polling mode.
    """
    def run(self):
        while True:
            print "checking for data ..."
            
            # Check if the coordinator has any jobs for us, if so play a game,
            # and report the result back to the coordinator.
            
            # REST API for fetching game information
            req = urllib2.Request("http://ws.spotify.com/search/1/track.json?q=kaizers+orchestra")
            opener = urllib2.build_opener()
            f = opener.open(req)
            jsonz = json.load(f)
            
            print jsonz

            # check json file for paths, call setUp with player paths, then do
            # playMatch

            time.sleep(1)
        return

    def setUp(self, player1, player2):
        self.player1 = player1 
        self.player2 = player2
    
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
        
        self.p1 = ProcessHandler(player1_bin_args)
        self.p2 = ProcessHandler(player2_bin_args)

    def playMatch(self):
        print "PLAYING GAME!"
        # p1 thinks about a number
        self.p1.communicate("think\n")
        number = int(self.p1.readline())
        
        # p2 tries to guess the number
        self.p2.communicate("guess\n")
        guessed = int(self.p2.readline())

        print "thought about " + str(number) + ", guessed " + str(guessed)
