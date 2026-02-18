import numpy as np
from dataclasses import dataclass
from random import random

right = np.matrix([[ 0.4,    0.6,    0,      0,      0,      0    ], 
                   [ 0.05,   0.6,    0.35,   0,      0,      0    ],
                   [ 0,      0.05,   0.6,    0.35,   0,      0    ],
                   [ 0,      0,      0.05,   0.6,    0.35,   0    ],
                   [ 0,      0,      0,      0.05,   0.6,    0.35 ],
                   [ 0,      0,      0,      0,      0.4,    0.6  ]])

@dataclass
class RiverSwim:
    states: int
    current_state: int = 0
    first_and_last = (0.4, 0.6)
    middle = (0.05, 0.6, 0.35)

    def __init__( self, states: int = 6 ):
        self.states = states
        self.actions = ("LEFT", "RIGHT")
    
    # returns (new state, reward)
    def step(self, action: str) -> (int, int):
        if action == "RIGHT":
            if self.current_state == 0:
                if random() < self.first_and_last[0]:
                    self.printState()
                    return self.current_state, 0
                else:
                    self.current_state = self.current_state + 1
                    self.printState()
                    return self.current_state, 0
                
            elif self.current_state == self.states - 1:
                if random() < self.first_and_last[0]:
                    self.current_state = self.current_state - 1
                    self.printState()
                    return self.current_state, 0
                else:
                    self.printState()
                    return self.current_state, 1
                
            else:
                if random() < self.middle[0]:
                    self.current_state = self.current_state - 1
                    self.printState()
                    return self.current_state, 0
                elif random() < self.middle[1]:
                    self.printState()
                    return self.current_state, 0
                else:
                    self.current_state = self.current_state + 1
                    self.printState()
                    return self.current_state, 0
                
        elif action == "LEFT":
            if self.current_state == 0:
                self.printState()
                return self.current_state, 5/1000
            self.current_state = self.current_state - 1
            self.printState()
            return self.current_state, 0
        
    def printState(self):
        #print("Current state: " + str(self.current_state))
        return
    

#Test stuff
riverSwim1 = RiverSwim(60)
riverSwim2 = RiverSwim(60)

def leftOnly(riverSwim1) -> int:
    reward = 0
    for i in range(1000):
        reward = reward + riverSwim1.step("LEFT")[1]

    print("Reward for left only: " + str(reward))

def rightOnly(riverSwim2) -> int:
    reward = 0
    for i in range(1000):
        reward = reward + riverSwim2.step("RIGHT")[1]

    print("Reward for right only: " + str(reward))


leftOnly(RiverSwim())
rightOnly(RiverSwim())