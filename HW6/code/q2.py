from random import choice
import os
import math
player, opponent = 'X', 'O'

class State:
    def __init__(self, board, player, parent=None, move=None):
        self.board = board
        self.player = player
        self.num_of_rollouts = 0
        self.total_utiliy = 0
        self.parent = parent
        self.move = move
        self.children = None

    def get_next_states(self):
        if self.children != None:
            return self.children
        else:
            next_states = []
            for i in range(3):
                for j in range(3):
                    if self.board[i][j] == '_':
                        new_board = [row[:] for row in self.board]
                        new_board[i][j] = self.player
                        next_states.append(
                            State(new_board, opponent if self.player == player else player, self, [i, j]))
            self.children = next_states
            return self.children

    def get_score(self):
        if checkWin(self.board):
            if self.player == player:
                return -1  # opponent wins
            else:
                return 1  # player wins
        else:
            return 1  # draw (it could be 0.85)

    def is_terminal(self):
        return checkWin(self.board) or not isMovesLeft(self.board)

    def UCBScore(self):
        if self.num_of_rollouts == 0:
            return float('inf')
        return (self.total_utiliy / self.num_of_rollouts) + 3 * math.sqrt(math.log(self.parent.num_of_rollouts) / self.num_of_rollouts)

    def __str__(self):
        return f"Player: {self.player}\n Board: {self.board}"

def findBestMove(board):

    ### YOUR CODE ###
    # return findRandom(board)
    # Monte Carlo Tree Search
    # https://en.wikipedia.org/wiki/Monte_Carlo_tree_search
    # implementation of the algorithm
    #
    # 1. Selection
    # 2. Expansion
    # 3. Simulation
    # 4. Backpropagation
    #
    root = State(board, opponent)
    for i in range(200): # 1000
        node = selection(root)
        if not node.is_terminal():
            node = expansion(node)
        utility = simulation(node)
        backpropagation(node, utility)
    
    # best_score = -float('inf')
    # best_child = None
    # for child in root.get_next_states():
    #     # score = child.UCBScore()
    #     score = child.total_utiliy / child.num_of_rollouts
    #     if score > best_score:
    #         best_score = score
    #         best_child = child
    
    # best_child = max(root.get_next_states(), key= lambda s:s.UCBScore())
    best_child = max(root.get_next_states(), key= lambda s:s.total_utiliy / s.num_of_rollouts)

    return best_child.move

def selection(node):
    if node.is_terminal():
        return node
    if node.num_of_rollouts == 0:
        return node
    best_score = -float('inf')
    best_child = None
    for child in node.get_next_states():
        score = child.UCBScore()
        if score > best_score:
            best_score = score
            best_child = child
    return selection(best_child)

def expansion(node):
    next_states = node.get_next_states()
    # return choice(next_states)
    board = [row[:] for row in node.board]
    node_player = node.player
    i, j = findThinkfully(board)
    board[i][j] = node_player
    # return next_states.filter(lambda s: s.board == board)
    for s in next_states:
        if s.board == board:
            return s
    return choice(next_states)

def simulation(node):
    board = [row[:] for row in node.board]
    node_player = node.player
    while not checkWin(board) and isMovesLeft(board):
        # if (node_player == player):
        #     i,j = findThinkfully(board)
        # else:
        #     i, j = findRandom(board)
        # i, j = findRandom(board)
        i, j = findThinkfully(board)
        board[i][j] = node_player
        node_player = opponent if node_player == player else player
    return get_score(board, node_player)

def backpropagation(node, utility):
    while (node != None):
        node.num_of_rollouts += 1
        node.total_utiliy += utility
        node = node.parent

# def backpropagation(node, utility):
#     node.num_of_rollouts += 1
#     node.total_utiliy += utility
#     if node.parent:
#         backpropagation(node.parent, utility)

def get_score(board, plyr):
    if checkWin(board):
        if plyr == player:
            return 1  # opponent wins
        else:
            return -1  # player wins
    else:
        return 1  # draw (it could be 0.85)

def findRandom(board):
    empty_spots = [i*3+j for i in range(3)
                   for j in range(3) if board[i][j] == "_"]
    idx = choice(empty_spots)
    return[int(idx/3), idx % 3]

def findThinkfully(board):
    for row in range(3):
        if (board[row][0] == board[row][1] and not board[row][0] == '_'):
            if (board[row][2] == '_'):
                return [row, 2]
        if (board[row][0] == board[row][2] and not board[row][0] == '_'):
            if board[row][1] == '_':
                return [row, 1]
        if (board[row][2] == board[row][1] and not board[row][1] == '_'):
            if board[row][0] == '_':
                return [row, 0]
        
    for col in range(3):
        if (board[0][col] == board[1][col] and not board[0][col] == '_'):
            if board[2][col] == '_':
                return [2, col]
        if (board[0][col] == board[2][col] and not board[0][col] == '_'):
            if board[1][col] == '_':
                return [1, col]
        if (board[2][col] == board[1][col] and not board[1][col] == '_'):
            if board[0][col] == '_':
                return [0, col]

    # main diameter check (col - row = 0)
    if (board[0][0] == board[1][1] and not board[0][0] == '_'):
        if board[2][2] == '_':
            return [2,2]
    if (board[0][0] == board[2][2] and not board[0][0] == '_'):
        if board[1][1] == '_':
            return [1,1]
    if (board[2][2] == board[1][1] and not board[1][1] == '_'):
        if board[0][0] == '_':
            return [0,0]

    # secondary diameter (col + row = 2)
    if (board[0][2] == board[1][1] and not board[0][2] == '_'):
        if board[2][0] == '_':
            return [2,0]
    if (board[0][2] == board[2][0] and not board[0][2] == '_'):
        if board[1][1] == '_':
            return [1,1]
    if (board[2][0] == board[1][1] and not board[1][1] == '_'):
        if board[0][2] == '_':
            return [0,2]

    empty_spots = [i*3+j for i in range(3)
                    for j in range(3) if board[i][j] == "_"]
    idx = choice(empty_spots)
    return[int(idx/3), idx % 3]

def isMovesLeft(board):
    return ('_' in board[0] or '_' in board[1] or '_' in board[2])

def checkWin(board):
    for row in range(3):
        if (board[row][0] == board[row][1] and board[row][1] == board[row][2] and not board[row][0] == '_'):
            return True
    for col in range(3):
        if (board[0][col] == board[1][col] and board[1][col] == board[2][col] and not board[0][col] == '_'):
            return True

    # main diameter check (col - row = 0)
    if (board[0][0] == board[1][1] and board[1][1] == board[2][2] and not board[0][0] == '_'):
        return True

    # secondary diameter (col + row = 2)
    if (board[0][2] == board[1][1] and board[1][1] == board[2][0] and not board[0][2] == '_'):
        return True

    return False

def printBoard(board):
    os.system('cls||clear')
    print("\n Player : X , Agent: O \n")
    for i in range(3):
        print(" ", end=" ")
        for j in range(3):
            if(board[i][j] == '_'):
                print(f"[{i*3+j+1}]", end=" ")
            else:
                print(f" {board[i][j]} ", end=" ")

        print()
    print()

if __name__ == "__main__":
    board = [
            ['_', '_', '_'],
            ['_', '_', '_'],
            ['_', '_', '_']
    ]

    turn = 0

    while isMovesLeft(board) and not checkWin(board):
        if(turn == 0):
            printBoard(board)
            print(" Select Your Move :", end=" ")
            tmp = int(input())-1
            userMove = [int(tmp/3),  tmp % 3]
            while((userMove[0] < 0 or userMove[0] > 2) or (userMove[1] < 0 or userMove[1] > 2) or board[userMove[0]][userMove[1]] != "_"):
                print('\n \x1b[0;33;91m' + ' Invalid move ' + '\x1b[0m \n')
                print("Select Your Move :", end=" ")
                tmp = int(input())-1
                userMove = [int(tmp/3),  tmp % 3]
            board[userMove[0]][userMove[1]] = player
            print("Player Move:")
            printBoard(board)
            turn = 1
        else:
            bestMove = findBestMove(board)
            board[bestMove[0]][bestMove[1]] = opponent
            print("Agent Move:")
            printBoard(board)
            turn = 0

    if(checkWin(board)):
        if(turn == 1):
            print('\n \x1b[6;30;42m' + ' Player Wins! ' + '\x1b[0m')

        else:
            print('\n \x1b[6;30;42m' + ' Agent Wins! ' + '\x1b[0m')
    else:
        print('\n \x1b[0;33;96m' + ' Draw! ' + '\x1b[0m')

    input('\n Press Enter to Exit... \n')
