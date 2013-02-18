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
        assert (pl_left, pl_right) == ("Player B", "Player A")
        assert len(self.queue) == 0
