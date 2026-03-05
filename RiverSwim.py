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
def step(old_state: int, action: int) -> (int, int):
    rnd = random()
    if action == 1:
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
            
    elif action == 0:
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
THRESHOLD = 1000

PROBABILITIES = np.zeros((6, 2, 6))
REWARD_PROBABILITIES = np.zeros((6, 2))

#MDP construction. If a state action pair have been visited THRESHOLD times, we estimate the probabilities and rewards for that state action pair. Otherwise, we assume that the action will lead to the same state with reward 1 (to encourage exploration).
def constructMDP():
    for state in range(states):
        for action in range(2): # 0 = left, 1 = right
            #We have visted enough times, and we can estimate the probabilities and rewards for this state action pair
            if STATE_ACTION[state, action] >= THRESHOLD:
                for new_state in range(states):
                    PROBABILITIES[state, action, new_state] = TRANSITION[state, action, new_state] / STATE_ACTION[state, action]
                REWARD_PROBABILITIES[state, action] = REWARD[state, action]
            else: #Else we assume that the action gives maximum reward and leads to the same state, to encourage exploration
                PROBABILITIES[state, action, state] = 1
                REWARD_PROBABILITIES[state, action] = 1


#Policy iteration. We can use the PROBABILITIES and REWARD_PROBABILITIES to compute the value function for each state, and then update the policy accordingly. We can repeat this process until convergence.
POLICY = np.zeros(states)
GAMMA = 0.99

def DPSolve():
    global POLICY
    VALUES = np.zeros(states)

    while True:
        #Policy evaluation, we can use the Bellman equation to compute the value function for each state given the current policy. We can repeat this process until convergence.
        while True:
            delta = 0
            for state in range(states):
                action = int(POLICY[state])
                #We estime the value of taking action a in state s, which is the reward for taking action a in state s plus the discounted value of the new state, which we can compute using the probabilities and values of the new states.
                new_value = REWARD_PROBABILITIES[state, action] + GAMMA * np.sum(PROBABILITIES[state, action] * VALUES)
                delta = max(delta, abs(new_value - VALUES[state]))
                VALUES[state] = new_value
            if delta < 0.001:
                break
        
        #Policy improvement
        stopping_criterion = True
        for state in range(states):
            old_action = POLICY[state]
            action_values = np.zeros(2)
            #Calculate the value for each action
            for action in range(2):
                action_values[action] = REWARD_PROBABILITIES[state, action] + GAMMA * np.sum(PROBABILITIES[state, action] * VALUES)

            #I set the policy to the best action.
            POLICY[state] = np.argmax(action_values)
            if old_action != POLICY[state]:
                stopping_criterion = False
        
        if stopping_criterion == True:
            break

EPISODE_LENGTH = 10000
EPISODE_AMOUNT = 1000    
EPSILON = 1
                
def run_agent():
    for episode in range(EPISODE_AMOUNT):
        state = 0
        for t in range(EPISODE_LENGTH):
            #action = action_decider(state) 
            action = int(POLICY[state])
            new_state, reward = step(state, action)
            STATE_ACTION[state, action] = STATE_ACTION[state, action] + 1
            TRANSITION[state, action, new_state] = TRANSITION[state, action, new_state] + 1
            REWARD[state, action] = REWARD[state, action] + (reward - REWARD[state, action]) / STATE_ACTION[state, action]
            state = new_state
        constructMDP()
        DPSolve()
    print("Final policy: " + str(POLICY))

def action_decider(state: int) -> str:
    pass


#Test stuff
def leftOnly() -> int:
    state = 0
    reward = 0
    for i in range(1000):
        r = step(state, 0)
        reward = reward + r[1]
        state = r[0]

    print("Reward for left only: " + str(reward))

def rightOnly() -> int:
    state = 0
    reward = 0
    for i in range(1000):
        r = step(state, 1)
        reward = reward + r[1]
        state = r[0]

    print("Reward for right only: " + str(reward))


leftOnly()
rightOnly()
run_agent()