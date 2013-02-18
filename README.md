aicomp
======

Intentions of this repo.

Create a platform for AIs to compete.

It should consist of:
A nice web-ui allowing account registration and player upload.
A player is a tarball containings configuration and 'binaries' to execute.

A coordinator, which decides which AIs should compete, keeps track of rankings.

Workers, who allow the AIs to compete in a sandbox.

Game-masters, who implement the game logic and coordinates the players within a sandbox.


Web-ui -> coordinator -> workers (plural) -> Game-master(one per worker)


Here's a pretty drawing: https://docs.google.com/drawings/d/1CNR-bygFxTm2PgKa87mY51YLF9kd-gQ4qvTOURQUnJM/edit?usp=sharing

Q: Why didn't you just fork github.org/aichallenge/aichallenge?
A: I couldn't figure out their license.