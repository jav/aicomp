import unittest

from challenge_queue import ChallengeQueue, QueueEmptyError

class ChallengeQueueTestCase(unittest.TestCase):

    def setUp(self):
        self.queue = ChallengeQueue()
        pass

    def tearDown(self):
        pass

    def test_append_challenger(self):
        assert len(self.queue) == 0
        self.queue.append("Player")
        assert len(self.queue) == 1
        assert self.queue.pop() == "Player"
        assert len(self.queue) == 0

    def test_get_challenges_from_empty_queue(self):
        assert len(self.queue) == 0
        self.assertRaises(QueueEmptyError, self.queue.pop)

    def test_get_challenges_from_queue(self):
        assert len(self.queue) == 0
        self.queue.append("Player A")
        self.queue.append("Player B")
        assert len(self.queue) == 2
        pl_left = self.queue.pop()
        pl_right = self.queue.pop()
        print (pl_left, pl_right)
        assert (pl_left, pl_right) == ("Player A", "Player B")
        assert len(self.queue) == 0

    def test_get_challenges_with_priorities_from_queue(self):
        assert len(self.queue) == 0
        self.queue.append("Un-important A", 100)
        self.queue.append("Un-important B", 100)
        self.queue.append("Semi-important A", 50)
        self.queue.append("Un-important C", 100)
        self.queue.append("Important A", 0)
        self.queue.append("Semi-important B", 50)
        assert len(self.queue) == 6
        assert self.queue.pop() == "Important A"
        assert self.queue.pop() == "Semi-important A"
        assert self.queue.pop() == "Semi-important B"
        assert len(self.queue) == 3
        assert self.queue.pop() == "Un-important A"
        assert self.queue.pop() == "Un-important B"
        assert self.queue.pop() == "Un-important C"
        assert len(self.queue) == 0


