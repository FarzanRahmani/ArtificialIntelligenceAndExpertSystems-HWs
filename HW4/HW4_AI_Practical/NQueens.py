from random import randrange


class NQueens:
    def __init__(self, N):
        self.N = N

    def initial(self):
        ''' Returns a random initial state '''
        return tuple(randrange(self.N) for i in range(self.N))

    def goal_test(self, state):
        ''' Returns True if the given state is a goal state '''
        for i in range(self.N):
            for j in range(i, self.N):
                if (i == j):
                    continue
                elif(state[i] == state[j]): # column check (row is already satisfied)
                    return False
                elif( (i + state[i]) == (j + state[j]) ): # Subdiameter
                    return False
                elif( (i - state[i]) == (j - state[j]) ): # main diameter check
                    return False
        return True


    def value(self, state):
        ''' Returns the value of a state. The higher the value, the closest to a goal state '''
        goal_value = 0
        for i in range(self.N):
            for j in range(i, self.N):
                if (i == j):
                    continue
                elif(state[i] == state[j]): # column check (row is already satisfied)
                    goal_value -= 1
                elif( (i + state[i]) == (j + state[j]) ): # Subdiameter
                    goal_value -= 1
                elif( (i - state[i]) == (j - state[j]) ): # main diameter check
                    goal_value -= 1
        return goal_value

    def neighbors(self, state):
        ''' Returns all possible neighbors (next states) of a state '''
        neigbors = []
        for row in range(self.N):
            for i in range(self.N):
                if (i != state[row]):
                    tmp = tuple((state[j] if (j != row ) else i) for j in range(self.N))
                    neigbors.append(tmp)
        return neigbors

