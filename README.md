aicomp
======

Intentions of this repo.

Create a platform for AIs to compete.

How to run
==========
Start the web-ui - python webfront.py
Start the coordinator - python coordinator.py
Now, make sure you observe on which ip:port the coordinator runs on (in future versions, this will be configurable)
Configure the worker(s), add the coordinator ip:port to poll for work.
Start the worker(s) - python game_master.py

WOHO!

More text (should be edited)
============================

It should consist of:
A nice web-ui allowing account registration and player upload.
A player is a tarball containings configuration and 'binaries' to execute.

A coordinator, which decides which AIs should compete, keeps track of rankings.

Workers, who allow the AIs to compete in a sandbox.

Game-masters, who implement the game logic and coordinates the players within a sandbox.


Web-ui -> coordinator -> workers (plural) -> Game-master(one per worker)


Here's a pretty drawing: https://docs.google.com/drawings/d/1CNR-bygFxTm2PgKa87mY51YLF9kd-gQ4qvTOURQUnJM/edit?usp=sharing

Q: Why didn't you just fork github.org/aichallenge/aichallenge?

A: I couldn't figure out their license. It seems to be a non-trivial issue: https://github.com/aichallenge/aichallenge/issues/276
