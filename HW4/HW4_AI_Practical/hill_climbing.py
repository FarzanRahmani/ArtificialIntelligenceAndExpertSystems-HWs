def hill_climbing(problem):
    ''' Returns a state as the solution of the problem '''
    # current_state = problem.initial()
    # current_value = problem.value(current_state)
    # while (not problem.goal_test(current_state)):
    #     neighbors = problem.neighbors(current_state)
    #     flag = True
    #     for neighbor in neighbors:
    #         if (problem.value(neighbor) > current_value):
    #             current_state = neighbor
    #             current_value = problem.value(current_state)
    #             flag = False
    #     if (flag):
    #         return current_state
    # return current_state

    #-------------------

    current_state = problem.initial()
    while(True):
        neighbors = problem.neighbors(current_state)
        neighbor = max(neighbors, key= lambda s : problem.value(s))
        if (problem.value(neighbor) <= problem.value(current_state)):
            return current_state
        current_state = neighbor

def hill_climbing_random_restart(problem, limit = 10):
    state = problem.initial()
    cnt = 0
    while problem.goal_test(state) == False and cnt < limit:
        state = hill_climbing(problem)
        cnt += 1
    return state
