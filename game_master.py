import json
import os
from random import randrange
import subprocess
import sys
import tarfile
import tempfile
import time
import urllib2

from threading import Thread

# directory in which to unpack packages
# (should be a separate partition and properly sandboxed)
DIR_PREFIX = "tmp"

class ProcessHandler():
    last_line = ""

    def __init__(self, args):
        print "Spawning process: %s" %(args,)
        self.process = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def communicate(self,input_list):
        # TODO: blocking?
        for data in input_list:
            print "communicate(%s): data:%s in input_list: %s"%(input_list, data, input_list)
            self.process.stdin.write(data)
            print "communicate(%s): process: %s"%(input_list, self.process)
            self.process.stdin.flush()

    def readline(self):
        def readline_threaded():
            self.last_line = self.process.stdout.readline()
        t = Thread(target=readline_threaded)
        t.start()
        t.join(1)
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
            req = urllib2.Request("http://localhost:5000/match/get/2")

            opener = urllib2.build_opener()
            f = opener.open(req)
            jsonz = json.load(f)

            print jsonz

            # check json file for paths, call setUp with player paths, then do
            # playMatch

            print jsonz

            try:
                urls = ["http://localhost:5000/"+x['files'] for x in jsonz['players']]
            except:
                continue # UGLY SHIIIT!
            self.setUp(urls[0], urls[1])
            self.reportWinner(self.playMatch())

            time.sleep(1)
        return

    def setUp(self, player1_url, player2_url):
        (self.player1_fh, self.player1) = tempfile.mkstemp()
        (self.player2_fh, self.player2) = tempfile.mkstemp()

        print "Opening url: %s" % (player1_url,)
        req = urllib2.urlopen(player1_url)
        CHUNK = 16 * 1024
        with open(self.player1, 'wb') as fp:
            while True:
                chunk = req.read(CHUNK)
                if not chunk: break
                fp.write(chunk)

        print "Opening url: %s" % (player2_url,)
        req = urllib2.urlopen(player2_url)
        CHUNK = 16 * 1024
        with open(self.player2, 'wb') as fp:
            while True:
                chunk = req.read(CHUNK)
                if not chunk: break
                fp.write(chunk)


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
        secret_number=randrange(1,10)
        print "PLAYING GAME: Guess %d"%(secret_number,)

        turns = 100
        for turn in range(turns):
            # p1 gets to guess
            guess = -1
            self.p1.communicate(["guess\n"])
            try:
                guess = int(self.p1.readline())
                print 'Player one: "I guess: %d."'%(guess,)
            except Exception as ex:
                print 'Player one: "I pass.", %s'%(ex,)
                pass
            if guess == secret_number:
                return [1,0]
            # p2 tries to guess the number
            self.p2.communicate(["guess\n"])
            try:
                guess = int(self.p2.readline())
                print 'Player two: "I guess: %d."'%(guess,)
            except:
                print 'Player two: "I pass.", %s'%(ex,)
                pass
            if guess == secret_number:
                return [0,1]

        return [0,0] # Tied game

    def reportWinner(self):
        #This should call the coordinator and let it know what the result was
        pass

if __name__ == "__main__":

    url = "http://localhost:5000/match/get/2" # should be sys.argv[1]
    gm = GameMaster(url)
    gm.run()


    
