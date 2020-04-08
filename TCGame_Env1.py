from gym import spaces
import pandas as pd
import numpy as np
import random
from itertools import groupby
from itertools import product
import itertools 



class TicTacToe():

    def __init__(self):
        """initialise the board"""
        
        # initialise state as an array
        self.state = [np.nan for _ in range(9)]  # initialises the board position, can initialise to an array or matrix
        # all possible numbers
        self.all_possible_numbers = [i for i in range(1, len(self.state) + 1)] # , can initialise to an array or matrix
    
        self.reset()


    def is_winning(self, curr_state):
   
        """Takes state as an input and returns whether any row, column or diagonal has winning sum
        Example: Input state- [1, 2, 3, 4, nan, nan, nan, nan, nan]
        Output = False"""
        # Check each row sum
        # 0->1->2 = 15
        # 3->4->5 = 15
        # 6->7->8 = 15
        for i in range(3):
            if (curr_state[i * 3] + curr_state[i * 3 + 1] + curr_state[i * 3 + 2]) == 15:
                print('Row win!')
                return True
        
        # Check each col sum
        # 0->3->6 = 15
        # 1->4->7 = 15
        # 2->5->8 = 15
        for i in range(3):
            if (curr_state[i + 0] + curr_state[i + 3] + curr_state[i + 6]) == 15:
                print('Col win!')
                return True
        
        # Check each diagonal sum
        # 0->4->8 = 15
        # 2->4->6 = 15
        if (curr_state[0] + curr_state[4] + curr_state[8]) == 15:
            print('Diagonal win!')
            return True
        if (curr_state[2] + curr_state[4] + curr_state[6]) == 15:
            print('Diagonal win!')
            return True

      
        return False
 

    def is_terminal(self, curr_state):
        
        # Terminal state could be winning state or when the board is filled up

        if self.is_winning(curr_state) == True:
           
            return True, 'Win'

        elif len(self.allowed_positions(curr_state)) == 0:
         
            return True, 'Tie'

        else:
            
            return False, 'Resume'


    def allowed_positions(self, curr_state):
        """Takes state as an input and returns all indexes that are blank"""
        return [i for i, val in enumerate(curr_state) if np.isnan(val)]#np.isnan(val)]


    def allowed_values(self, curr_state):
        """Takes the current state as input and returns all possible (unused) values that can be placed on the board"""

#         print(curr_state)
        used_values = [val for val in curr_state if not np.isnan(val)]#np.isnan(val)]
#         print('*** Used values ***')
#         print(used_values)
        agent_values = [val for val in self.all_possible_numbers if val not in used_values and val % 2 !=0]
        env_values = [val for val in self.all_possible_numbers if val not in used_values and val % 2 ==0]

        return (agent_values, env_values)


    def action_space(self, curr_state):
        """Takes the current state as input and returns all possible actions, i.e, all combinations of allowed positions and allowed values"""
#         print('*** Inside action_space ***')

        agent_actions = product(self.allowed_positions(curr_state), self.allowed_values(curr_state)[0])
        env_actions = product(self.allowed_positions(curr_state), self.allowed_values(curr_state)[1])
        return (agent_actions, env_actions)



    def state_transition(self, curr_state, curr_action):
        """Takes current state and action and returns the board position just after agent's move.
        Example: Input state- [1, 2, 3, 4, nan, nan, nan, nan, nan], action- [7, 9] or [position, value]
        Output = [1, 2, 3, 4, nan, nan, nan, 9, nan]
        """

        move_position = curr_action[0]
        move_value = curr_action[1]
        curr_state[move_position] = move_value

        return curr_state

    def step(self, curr_state, curr_action):
        """Takes current state and action and returns the next state, reward and whether the state is terminal. Hint: First, check the board position after
        agent's move, whether the game is won/loss/tied. Then incorporate environment's move and again check the board status.
        Example: Input state- [1, 2, 3, 4, nan, nan, nan, nan, nan], action- [7, 9] or [position, value]
        Output = ([1, 2, 3, 4, nan, nan, nan, 9, nan], -1, False)"""

        terminal = self.is_terminal(curr_state)[1]
       
        if terminal == 'Win':
            
            print('***** game over, agent won *****')
            #print(curr_state)
            return (curr_state, 10, True)
    
                
        elif terminal == 'Tie':
                print('***** game over, it is a tie *****')
                return (curr_state, 0, True)
            
        else:
            #Incorporate environment's move
            #print('*** Environment move ***')

            env_action = random.sample(list(self.action_space(curr_state)[1]), 1)

            env_action = list(itertools.chain(*env_action))

            # State transition after environment's action
            transitioned_state = self.state_transition(curr_state, env_action)

            #print(transitioned_state)
            terminal =  self.is_terminal(transitioned_state)[1]
            #print(terminal)
            if terminal == 'Win':
                print('***** game over, environment won *****')

                return (transitioned_state, -10, True)
#             elif terminal == 'Tie':
#                 print('***** game over, it is a tie due to env move *****')  #The tie will always be because of the agent move
#                 return (transitioned_state, 0, True)                         # because the agent starts first
            else:
                #print('*** Non terminal state ***')
                return (transitioned_state, -1, False)
            
                        
            
            
            

            
                


    def reset(self):
        return self.state
