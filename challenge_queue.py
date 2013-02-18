#This class should not need persistant backing.

class QueueEmptyError(Exception):
    pass


class ChallengeQueue(object):
    queue = []

    def __init__(self):
        self.queue = []

    def append(self, item):
        #Sort-algo here?
        #Right now, consider sort() = null
        self.queue.append(item)

    def pop(self):
        if len(self.queue) <= 0:
            raise QueueEmptyError
        else:
            return self.queue.pop()

    def __len__(self):
        return len(self.queue)


