import random
from fsm import *


class NPC:
    UP, DOWN, LEFT, RIGHT = "u", "d", "l", "r"
    TIMER_UP = "tu"
    DIRECTIONS = {UP: "npc_up.png", DOWN: "npc_down.png", LEFT: "npc_left.png", RIGHT: "npc_right.png"}

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.directions = list(self.DIRECTIONS.keys())
        self.direction = random.choice(self.directions)
        self.fsm = FSM(self.DOWN)
        self.init_fsm()

    def init_fsm(self):
        self.fsm.add_transition(self.TIMER_UP, self.DOWN, self.turn_LEFT, self.LEFT)
        self.fsm.add_transition(self.TIMER_UP, self.LEFT, self.turn_UP, self.UP)
        self.fsm.add_transition(self.TIMER_UP, self.UP, self.turn_RIGHT, self.RIGHT)
        self.fsm.add_transition(self.TIMER_UP, self.RIGHT, self.turn_DOWN, self.DOWN)

    def turn_UP(self):
        self.direction = self.UP

    def turn_DOWN(self):
        self.direction = self.DOWN

    def turn_LEFT(self):
        self.direction = self.LEFT

    def turn_RIGHT(self):
        self.direction = self.RIGHT
