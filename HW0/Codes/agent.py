from queue import PriorityQueue
import random

#################################################################################
# Functions
#################################################################################

def ai_action(game_state): # return index
    ''' Generate and play move from tic tac toe AI'''
    #################################################################################
    # "*** YOUR CODE HERE ***"
    
    best_index = get_key_index(game_state) # index_priorities
    best_index = check_for_winning_2index(game_state, best_index)
    best_index = check_for_losing_2index(game_state, best_index)
    best_index = check_for_winning_3index(game_state, best_index)
    best_index = check_for_losing_3index(game_state, best_index)

    return best_index
    #################################################################################
    pass

def get_key_index(game_state):
    best_index = 0

    priority_1 = [12] # 8 states wins
    priority_2 = [6,7,8,11,13,16,17,18] # 6 states wins
    priority_3 = [1,3,5,9,15,19,21,23] # 4 states wins
    priority_4 = [2,10,14,22] # 3 states wins
    priority_5 = [0,4,20,24] # 2 states wins
    priorities = [priority_1, priority_2, priority_3, priority_4, priority_5]

    isChosen = False
    for priority in priorities:
        for i in priority:
            if game_state[i] is None:
                best_index = i
                isChosen = True
                break
        if isChosen:
            break

    return best_index

def check_for_winning_3index(game_state, index):
    best_index = index

    # without priotiy index
    # condition = [
    #         # horizontal
    #         (0 , 1 , 2 , 3 ),
    #         (1 , 2 , 3 , 4 ),
    #         (5 , 6 , 7 , 8 ),
    #         (6 , 7 , 8 , 9 ),
    #         (10, 11, 12, 13),
    #         (11, 12, 13, 14),
    #         (15, 16, 17, 18),
    #         (16, 17, 18, 19),
    #         (20, 21, 22, 23),
    #         (21, 22, 23, 24),

    #         # vertical
    #         (0 , 5 , 10 , 15),
    #         (5 , 10, 15 , 20),
    #         (1 , 6 , 11 , 16),
    #         (6 , 11, 16 , 21),
    #         (2 , 7 , 12 , 17),
    #         (7 , 12, 17 , 22),
    #         (3 , 8 , 13 , 18),
    #         (8 , 13, 18 , 23),
    #         (4 , 9 , 14 , 19),
    #         (9 , 14, 19 , 24),

    #         # diagonal
    #         (0 , 6 , 12, 18),
    #         (6 , 12, 18, 24),
    #         (4 , 8 , 12, 16),
    #         (8 , 12, 16, 20),
    #         (1 , 7 , 13, 19),
    #         (5 , 11, 17, 23),
    #         (3 , 7 , 11, 15),
    #         (9 , 13, 17, 21),

    #     ]

    # with priotiy index
    condition = [

            (10, 11, 12, 13),
            (11, 12, 13, 14),
            (2 , 7 , 12 , 17),
            (7 , 12, 17 , 22),
            (8 , 12, 16, 20),
            (6 , 12, 18, 24),
            (0 , 6 , 12, 18),
            (4 , 8 , 12, 16),

            (6 , 7 , 8 , 9 ),
            (15, 16, 17, 18),
            (16, 17, 18, 19),
            (1 , 6 , 11 , 16),
            (6 , 11, 16 , 21),
            (3 , 8 , 13 , 18),
            (8 , 13, 18 , 23),
            (5 , 6 , 7 , 8 ),

            (1 , 7 , 13, 19),
            (5 , 11, 17, 23),
            (9 , 13, 17, 21),
            (3 , 7 , 11, 15),

            (0 , 1 , 2 , 3 ),
            (1 , 2 , 3 , 4 ),
            (20, 21, 22, 23),
            (21, 22, 23, 24),
            (0 , 5 , 10 , 15),
            (5 , 10, 15 , 20),
            (4 , 9 , 14 , 19),
            (9 , 14, 19 , 24),

        ]
    
    for indexes in condition:
        index0 = indexes[0]
        index1 = indexes[1]
        index2 = indexes[2]
        index3 = indexes[3]
        check = (game_state[index0], game_state[index1], game_state[index2], game_state[index3])
        if (check == (None, False, False, False)) or check == (False, None, False, False) or check == (False, False, None, False) or check == (False, False, False, None):
            if check[0] == None:
                best_index = index0
            elif check[1] == None:
                best_index = index1
            elif check[2] == None:
                best_index = index2
            elif check[3] == None:
                best_index = index3
            break
    
    return best_index

def check_for_losing_3index(game_state, index):
    best_index = index

    # without priotiy index
    # condition = [
    #         # horizontal
    #         (0 , 1 , 2 , 3 ),
    #         (1 , 2 , 3 , 4 ),
    #         (5 , 6 , 7 , 8 ),
    #         (6 , 7 , 8 , 9 ),
    #         (10, 11, 12, 13),
    #         (11, 12, 13, 14),
    #         (15, 16, 17, 18),
    #         (16, 17, 18, 19),
    #         (20, 21, 22, 23),
    #         (21, 22, 23, 24),

    #         # vertical
    #         (0 , 5 , 10 , 15),
    #         (5 , 10, 15 , 20),
    #         (1 , 6 , 11 , 16),
    #         (6 , 11, 16 , 21),
    #         (2 , 7 , 12 , 17),
    #         (7 , 12, 17 , 22),
    #         (3 , 8 , 13 , 18),
    #         (8 , 13, 18 , 23),
    #         (4 , 9 , 14 , 19),
    #         (9 , 14, 19 , 24),

    #         # diagonal
    #         (0 , 6 , 12, 18),
    #         (6 , 12, 18, 24),
    #         (4 , 8 , 12, 16),
    #         (8 , 12, 16, 20),
    #         (1 , 7 , 13, 19),
    #         (5 , 11, 17, 23),
    #         (3 , 7 , 11, 15),
    #         (9 , 13, 17, 21),

    #     ]

    # with priotiy index
    condition = [

            (10, 11, 12, 13),
            (11, 12, 13, 14),
            (2 , 7 , 12 , 17),
            (7 , 12, 17 , 22),
            (8 , 12, 16, 20),
            (6 , 12, 18, 24),
            (0 , 6 , 12, 18),
            (4 , 8 , 12, 16),

            (6 , 7 , 8 , 9 ),
            (15, 16, 17, 18),
            (16, 17, 18, 19),
            (1 , 6 , 11 , 16),
            (6 , 11, 16 , 21),
            (3 , 8 , 13 , 18),
            (8 , 13, 18 , 23),
            (5 , 6 , 7 , 8 ),

            (1 , 7 , 13, 19),
            (5 , 11, 17, 23),
            (9 , 13, 17, 21),
            (3 , 7 , 11, 15),

            (0 , 1 , 2 , 3 ),
            (1 , 2 , 3 , 4 ),
            (20, 21, 22, 23),
            (21, 22, 23, 24),
            (0 , 5 , 10 , 15),
            (5 , 10, 15 , 20),
            (4 , 9 , 14 , 19),
            (9 , 14, 19 , 24),

        ]
    
    for indexes in condition:
        index0 = indexes[0]
        index1 = indexes[1]
        index2 = indexes[2]
        index3 = indexes[3]
        check = (game_state[index0], game_state[index1], game_state[index2], game_state[index3])
        if (check == (None, True, True, True)) or check == (True, None, True, True) or check == (True, True, None, True) or check == (True, True, True, None):
            if check[0] == None:
                best_index = index0
            elif check[1] == None:
                best_index = index1
            elif check[2] == None:
                best_index = index2
            elif check[3] == None:
                best_index = index3
            break
    
    return best_index

def check_for_winning_2index(game_state, index):
    best_index = index

    # without priotiy index
    # condition = [
    #         # horizontal
    #         (0 , 1 , 2 , 3 ),
    #         (1 , 2 , 3 , 4 ),
    #         (5 , 6 , 7 , 8 ),
    #         (6 , 7 , 8 , 9 ),
    #         (10, 11, 12, 13),
    #         (11, 12, 13, 14),
    #         (15, 16, 17, 18),
    #         (16, 17, 18, 19),
    #         (20, 21, 22, 23),
    #         (21, 22, 23, 24),

    #         # vertical
    #         (0 , 5 , 10 , 15),
    #         (5 , 10, 15 , 20),
    #         (1 , 6 , 11 , 16),
    #         (6 , 11, 16 , 21),
    #         (2 , 7 , 12 , 17),
    #         (7 , 12, 17 , 22),
    #         (3 , 8 , 13 , 18),
    #         (8 , 13, 18 , 23),
    #         (4 , 9 , 14 , 19),
    #         (9 , 14, 19 , 24),

    #         # diagonal
    #         (0 , 6 , 12, 18),
    #         (6 , 12, 18, 24),
    #         (4 , 8 , 12, 16),
    #         (8 , 12, 16, 20),
    #         (1 , 7 , 13, 19),
    #         (5 , 11, 17, 23),
    #         (3 , 7 , 11, 15),
    #         (9 , 13, 17, 21),

    #     ]

    # with priotiy index
    condition = [

            (10, 11, 12, 13),
            (11, 12, 13, 14),
            (2 , 7 , 12 , 17),
            (7 , 12, 17 , 22),
            (8 , 12, 16, 20),
            (6 , 12, 18, 24),
            (0 , 6 , 12, 18),
            (4 , 8 , 12, 16),

            (6 , 7 , 8 , 9 ),
            (15, 16, 17, 18),
            (16, 17, 18, 19),
            (1 , 6 , 11 , 16),
            (6 , 11, 16 , 21),
            (3 , 8 , 13 , 18),
            (8 , 13, 18 , 23),
            (5 , 6 , 7 , 8 ),

            (1 , 7 , 13, 19),
            (5 , 11, 17, 23),
            (9 , 13, 17, 21),
            (3 , 7 , 11, 15),

            (0 , 1 , 2 , 3 ),
            (1 , 2 , 3 , 4 ),
            (20, 21, 22, 23),
            (21, 22, 23, 24),
            (0 , 5 , 10 , 15),
            (5 , 10, 15 , 20),
            (4 , 9 , 14 , 19),
            (9 , 14, 19 , 24),

        ]
    
    for indexes in condition:
        index0 = indexes[0]
        index1 = indexes[1]
        index2 = indexes[2]
        index3 = indexes[3]
        check = (game_state[index0], game_state[index1], game_state[index2], game_state[index3])
        if (check == (None, None, False, False)) or check == (None, False, None, False) or check == (None, False, False, None) or check == (False, None, None, False) or check == (False, None, False, None) or check == (False, False, None, None):
            if check[1] == None:
                best_index = index1
            elif check[2] == None:
                best_index = index2
            elif check[0] == None:
                best_index = index0
            elif check[3] == None:
                best_index = index3
            break
    
    return best_index

def check_for_losing_2index(game_state, index):
    best_index = index

    # without priotiy index
    # condition = [
    #         # horizontal
    #         (0 , 1 , 2 , 3 ),
    #         (1 , 2 , 3 , 4 ),
    #         (5 , 6 , 7 , 8 ),
    #         (6 , 7 , 8 , 9 ),
    #         (10, 11, 12, 13),
    #         (11, 12, 13, 14),
    #         (15, 16, 17, 18),
    #         (16, 17, 18, 19),
    #         (20, 21, 22, 23),
    #         (21, 22, 23, 24),

    #         # vertical
    #         (0 , 5 , 10 , 15),
    #         (5 , 10, 15 , 20),
    #         (1 , 6 , 11 , 16),
    #         (6 , 11, 16 , 21),
    #         (2 , 7 , 12 , 17),
    #         (7 , 12, 17 , 22),
    #         (3 , 8 , 13 , 18),
    #         (8 , 13, 18 , 23),
    #         (4 , 9 , 14 , 19),
    #         (9 , 14, 19 , 24),

    #         # diagonal
    #         (0 , 6 , 12, 18),
    #         (6 , 12, 18, 24),
    #         (4 , 8 , 12, 16),
    #         (8 , 12, 16, 20),
    #         (1 , 7 , 13, 19),
    #         (5 , 11, 17, 23),
    #         (3 , 7 , 11, 15),
    #         (9 , 13, 17, 21),

    #     ]

    # with priotiy index
    condition = [

            (10, 11, 12, 13),
            (11, 12, 13, 14),
            (2 , 7 , 12 , 17),
            (7 , 12, 17 , 22),
            (8 , 12, 16, 20),
            (6 , 12, 18, 24),
            (0 , 6 , 12, 18),
            (4 , 8 , 12, 16),

            (6 , 7 , 8 , 9 ),
            (15, 16, 17, 18),
            (16, 17, 18, 19),
            (1 , 6 , 11 , 16),
            (6 , 11, 16 , 21),
            (3 , 8 , 13 , 18),
            (8 , 13, 18 , 23),
            (5 , 6 , 7 , 8 ),

            (1 , 7 , 13, 19),
            (5 , 11, 17, 23),
            (9 , 13, 17, 21),
            (3 , 7 , 11, 15),

            (0 , 1 , 2 , 3 ),
            (1 , 2 , 3 , 4 ),
            (20, 21, 22, 23),
            (21, 22, 23, 24),
            (0 , 5 , 10 , 15),
            (5 , 10, 15 , 20),
            (4 , 9 , 14 , 19),
            (9 , 14, 19 , 24),

        ]
    
    for indexes in condition:
        index0 = indexes[0]
        index1 = indexes[1]
        index2 = indexes[2]
        index3 = indexes[3]
        check = (game_state[index0], game_state[index1], game_state[index2], game_state[index3])
        
        if (check == (None, None, True, True)) or check == (None, True, None, True) or check == (None, True, True, None) or check == (True, None, None, True) or check == (True, None, True, None) or check == (True, True, None, None):
            if check[1] == None:
                best_index = index1
            elif check[2] == None:
                best_index = index2
            elif check[0] == None:
                best_index = index0
            elif check[3] == None:
                best_index = index3

            break
    
    return best_index
