import numpy as np
from dataclasses import dataclass
from random import random

right = np.matrix([[ 0.4,    0.6,    0,      0,      0,      0    ], 
                   [ 0.05,   0.6,    0.35,   0,      0,      0    ],
                   [ 0,      0.05,   0.6,    0.35,   0,      0    ],
                   [ 0,      0,      0.05,   0.6,    0.35,   0    ],
                   [ 0,      0,      0,      0.05,   0.6,    0.35 ],
                   [ 0,      0,      0,      0,      0.4,    0.6  ]])


states: int = 6
first_and_last = (0.4, 0.6)
middle = (0.05, 0.6, 0.35)

# returns (new state, reward)
# Should also take state as input????
def step(old_state: int, action: str) -> (int, int):
    rnd = random()
    if action == "RIGHT":
        if old_state == 0:
            if rnd < first_and_last[0]:
                printState()
                return old_state, 0
            else:
                new_state = old_state + 1
                printState()
                return new_state, 0
            
        elif old_state == states - 1:
            if rnd < first_and_last[0]:
                new_state = old_state - 1
                printState()
                return new_state, 0
            else:
                printState()
                return old_state, 1
            
        else:
            if rnd < middle[0]:
                new_state = old_state - 1
                printState()
                return new_state, 0
            elif rnd < middle[0] + middle[1]:
                printState()
                return old_state, 0
            else:
                new_state = old_state + 1
                printState()
                return new_state, 0
            
    elif action == "LEFT":
        if old_state == 0:
            printState()
            return old_state, 5/1000
        new_state = old_state - 1
        printState()
        return new_state, 0
    
def printState():
    #print("Current state: " + str(self.current_state))
    return

#AGENT PART

# (old state, reward, new state)
STATE_ACTION = np.zeros((6, 2))
TRANSITION = np.zeros((6, 2, 6))
REWARD = np.zeros((6, 2))

#agent = (state, action) -> new state, reward
state = 0
while True:
    
    pass

#Test stuff
def leftOnly() -> int:
    state = 0
    reward = 0
    for i in range(1000):
        r = step(state, "LEFT")
        reward = reward + r[1]
        state = r[0]

    print("Reward for left only: " + str(reward))

def rightOnly() -> int:
    state = 0
    reward = 0
    for i in range(1000):
        r = step(state, "RIGHT")
        reward = reward + r[1]
        state = r[0]

    print("Reward for right only: " + str(reward))


leftOnly()
rightOnly()