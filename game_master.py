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

    def communicate(self,inp):
        # TODO: blocking?
        print "communicate(%s)"%(inp,)
        print >>self.process.stdin, inp

    def readline(self):
        def readline_threaded():
            self.last_line = self.process.stdout.readline()
        t = Thread(target=readline_threaded)
        t.start()
        t.join(3)
        return self.last_line


class GameMaster(object):
    """
    Create a GameMaster with a coordinator. GameMaster will poll
    the Coordinator for jobs.
    """
    config = {}

    def __init__(self, coordinator):
        # Redundant with the internal 'config' dict.
        # Osk: Which should stay?
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
            req = urllib2.Request(self.config['COORDINATOR_URL'] + "match/get/2")

            opener = urllib2.build_opener()
            f = opener.open(req)
            jsonz = json.load(f)

            print jsonz

            # check json file for paths, call setUp with player paths, then do
            # playMatch

            print jsonz

            try:
                urls = [self.config['COORDINATOR_URL']+x['files'] for x in jsonz['players']]
            except Exception as e:
                print "NO GOOD, CONTINUE!: %s" % (e,)
                continue # UGLY SHIIIT!


            self.reportMatchResult(
                self.playMatch(
                    self.setUpMatch(
                        jsonz,
                        self.config['COORDINATOR_URL'])
                    )
                )

            time.sleep(1)
        return

    def setUpMatch(self, match, config):
        for player in match['players']:
            player['url'] = self.config['COORDINATOR_URL']+player['files']
            (player['local_tar_file_fh'], player['local_tar_file']) = tempfile.mkstemp()
            print "Opening url: %s" % (player['url'],)
            req = urllib2.urlopen(player['url'])
            CHUNK = 16 * 1024
            with open(player['local_tar_file'], 'wb') as fp:
                while True:
                    chunk = req.read(CHUNK)
                    if not chunk: break
                    fp.write(chunk)

            player['tar'] = tarfile.open(player['local_tar_file'])
            player['local_files'] = tempfile.mkdtemp()
            player['tar'].extractall(player['local_files'])
            print "player['local_files']:",player['local_files']
            print "os.join():", os.path.join(player['local_files'], "manifest.json")
            player['manifest'] = os.path.join(player['local_files'], "manifest.json")
            print "player['manifest']:", player['manifest']
            player['exec'] = os.path.join(player['local_files'], json.load(open(player['manifest'], 'r'))['executable'])

            # make the players talk!
            player['bin_args'] = ["python",os.path.join(os.getcwd(),player['exec'])]

        def mkProcessHandlers(player):
            print "mkProcesshandlers(%s)"%(player,)
            player['process'] = ProcessHandler(["python",os.path.join(os.getcwd(), player['exec'])])
            return player

        print "map(mkProcessHandlers, player=%s)"%(match['players'],)
        match['players'] = map(mkProcessHandlers, match['players'])
        return match
#        self.p2 = ProcessHandler(player2_bin_args)



    def playMatch(self, match):
        secret_number=randrange(1,10)
        print "PLAYING GAME: Guess %d"%(secret_number,)

        print "match:", match
        turns = 100
        for turn in range(turns):
            for player in match['players']:
                guess = -1
                player['process'].communicate("guess")
            try:
                guess = int(player['process'].readline())
                print 'Player %d: "I guess: %d."'%(player['id'], guess)
            except Exception as ex:
                print 'Player %d: "I pass.", %s'%(player['id'], ex)
                pass
            if guess == secret_number:
                return [1 if p['id'] == player['id'] else 0 for p in match['players']] # This would be more readable with map() and a support function, code-golf FTL.
        return [0 for x in match['players']] # Tied game

    def reportMatchResult(self, match):
        #This should call the coordinator and let it know what the result was
        pass

if __name__ == "__main__":
    config = json.load(open('game_master.conf','r'))
    gm = GameMaster(config['COORDINATOR_URL'])
    gm.config = config
    gm.run()
