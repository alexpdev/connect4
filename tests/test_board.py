from unittest import TestCase
from connect4 import board

class TestBoard(TestCase):

    def setUp(self):
        self.board = Board()

    def board_test(self):
        self.assertTrue(self.board)
