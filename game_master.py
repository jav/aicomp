import json
import os
from random import randrange
import subprocess
import sys
import tarfile
import tempfile
from threading import Thread
import time
import urllib
import urllib2



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
        self.last_line = ""
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
        game_count = 0
        while True:
            if gm.config.get('MATCHLIMIT',-1) >= 0:
                if game_count >= gm.config['MATCHLIMIT']:
                    break
            game_count += 1

            print "checking for data ..."

            # Check if the coordinator has any jobs for us, if so play a game,
            # and report the result back to the coordinator.

            # REST API for fetching game information
            url = self.config['COORDINATOR_URL'] + "match/get/2"
            req = urllib2.Request(url)

            print "Fetching data from url:" ,url
            opener = urllib2.build_opener()
            f = opener.open(req)
            jsonz = json.load(f)

            print jsonz

            # check json file for paths, call setUp with player paths, then do
            # playMatch

            try:
                urls = [self.config['COORDINATOR_URL']+x['player']['files'] for x in jsonz['playerresults']]
            except Exception as e:
                print "NO GOOD, CONTINUE! (exception: %s)" % (e.message,)
                continue # UGLY SHIIIT!


            print "jsonz:", jsonz

            self.reportMatchResult(
                **self.playMatch(
                    **self.setUpMatch(
                        match=jsonz,
                        config=self.config)
                    )
                )

            time.sleep(1)
        return

    def setUpMatch(self, **kwargs):
        match = kwargs['match']
        config = kwargs['config']
        print 'setUpMatch(match=%s, config=%s)'%(match, config)
        for i in range(len(match['playerresults'])):
            player = match['playerresults'][i]['player']
            player['url'] = config['COORDINATOR_URL']+player['files']
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
            match['playerresults'][i]['player'] = player
        print "match['playerresults']",match['playerresults']

        def mkProcessHandlers(player):
            print "mkProcesshandlers(%s)"%(player,)
            player['process'] = ProcessHandler(["python",os.path.join(os.getcwd(), player['exec'])])
            return player


        print "map(mkProcessHandlers, playerresults=%s)"%(match['playerresults'],)

        for i in range(len(match['playerresults'])):
            match['playerresults'][i]['player'] = mkProcessHandlers(match['playerresults'][i]['player'])

        return {'match':match, 'config':config}
#        self.p2 = ProcessHandler(player2_bin_args)



    def playMatch(self, **kwargs):
        match = kwargs['match']
        config = kwargs['config']
        match['state'] = "inprogress"
        secret_number=randrange(1,10)
        print "PLAYING GAME: Guess %d"%(secret_number,)

        print "match:", match
        turns = 6
        for turn in range(turns):
            for playerresult in match['playerresults']:
                print "playerresult:", playerresult
                player = playerresult['player']
                guess = -1
                player['process'].communicate("guess")
            try:
                guess = int(player['process'].readline())
                print 'Player %d: "I guess: %d."'%(player['id'], guess)
            except Exception as ex:
                print 'Player %d: "I pass.", %s'%(player['id'], ex)
                pass
            if guess == secret_number:
                print "WE HAVE A WINRAR!!!"
                result = [1 if p['id'] == player['id'] else 0 for p in match['playerresults']]
                match['playerresults'] = zip(match['playerresults'], result)
                # result = dict([(p['id'],1) if p['id'] == player['id'] else (p['id'],0) for p in match['playerresults']]) # This would be more readable with map() and a support function, code-golf FTL.
                match['state'] = "sucessfull"
                return {'match':match, 'config': config}

        print "DRAW GAME!"
        # result = [(x['id'], 0) for x in match['playerresults']] # Tied game
        match['playerresults'] = zip(match['playerresults'], [0 for x in match['playerresults'] ])
        match['state'] = "sucessfull"
        return {'match':match, 'config': config}

    def reportMatchResult(self, **kwargs):
        match=kwargs['match']
        print "reportMatchResult(): match: %s"%(match,)
        config=kwargs['config']
        # We really don't need all the info in match, we could/should
        # filter out local-scope things
        print "reportMatchResult(): config:", config

        url = '%smatch/report/%d'%(config['COORDINATOR_URL'],int(match['id']))
        req = urllib2.Request(url)

        req.add_data(urllib.urlencode(match))
        print 'urllib2.get_method(%s): %s'% (req.get_full_url(), req.get_method())
        r=urllib2.urlopen(req)

if __name__ == "__main__":
    config = json.load(open('game_master.conf','r'))
    gm = GameMaster(config['COORDINATOR_URL'])
    gm.config = config
    try:
        gm.config['MATCHLIMIT'] = int(sys.argv[1] if len(sys.argv) > 1 else -1)
    except:
        print "Argument 1, number of matches not an integer."
        exit(1)

    gm.run()
