# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random
import util

from game import Agent

# q1
class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """

    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(
            gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(
            len(scores)) if scores[index] == bestScore]
        # Pick randomly among the best
        chosenIndex = random.choice(bestIndices)

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action) # action:  West, North, East, South, Stop
        # %%%%%%%%%%%%%%%%%%%% (^:agent, o:power pellet, G:ghost, .:food, %:wall)
        # %o...%.G......%....%
        # %.%%.%.%%%%%%.%G%%.%
        # %.%..............%.%
        # %.%.%%.%%  %%.%%.%.%
        # %......%    %      %
        # %.%.%%.%%%%%% %%.% %
        # %.%.......... ...% %
        # %.%%.%.%%%%%% %.%%^%
        # %....%...     %...o%
        # %%%%%%%%%%%%%%%%%%%%
        # Score: 135
        newPos = successorGameState.getPacmanPosition() # (3, 8) 
        newFood = successorGameState.getFood()
        # %%
        # FFFFFFFFFFFFFFFFFFFF
        # FFTTTFTTTTTTTTFTTTTF
        # FTFFTFTFFFFFFTFTFFTF
        # FTFTTTTTTTTTTTTTTFTF
        # FTFTFFTFFFFFFTFFTFTF
        # FTTTTTTFFFFFFFFFFFFF
        # FTFTFFTFFFFFFFFFTFFF
        # FTFTTTTTTTTTTFTTTFFF
        # FTFFTFTFFFFFFFFTFFFF
        # FTTTTFTTTFFFFFFTTTFF
        # FFFFFFFFFFFFFFFFFFFF
        # %%
        newGhostStates = successorGameState.getGhostStates() #  [<game.AgentState object at 0x00000211085E65B0>, <game.AgentState object at 0x00000211085E65E0>]
        newScaredTimes = [
            ghostState.scaredTimer for ghostState in newGhostStates] # [40, 40] down to  [0, 0]
        "*** YOUR CODE HERE ***"
        oldCapsules = currentGameState.getCapsules() # [(1, 1), (1, 9)]
        evaluation_value = successorGameState.getScore() # or 0
        for food in newFood.asList(): # [(1, 5), (1, 7), (2, 6), (2, 8), (3, 5), (3, 7)]
            evaluation_value += 1 / manhattanDistance(food, newPos)
        for capsule in oldCapsules: 
            if manhattanDistance(capsule, newPos) == 0:
                evaluation_value += 10 # (or 100)
            else:
                evaluation_value += (1 / manhattanDistance(capsule, newPos)) * 2
        # for ghost in newGhostStates: # [<game.AgentState object at 0x00000211085E65B0>, <game.AgentState object at 0x00000211085E65E0>]
        #     if manhattanDistance(ghost.getPosition(), newPos) < 2:
        #         evaluation_value -= 1000
        # for scaredTime in newScaredTimes:
        #     if scaredTime > 0:
        #         evaluation_value += 1000
        for i in range(len(newGhostStates)):
            ghost = newGhostStates[i]
            if manhattanDistance(ghost.getPosition(), newPos) < 2:
                if newScaredTimes[i] > 2:
                    evaluation_value += 1000
                else:
                    evaluation_value -= 1000
        # return successorGameState.getScore() # 131.0
        return evaluation_value # 131.0


def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()


class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn='scoreEvaluationFunction', depth='2'):
        self.index = 0  # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)
        self.nodesCount = 0

# q2
class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        # util.raiseNotDefined()
        self.nodesCount = 0
        # function decision(s) returns an action
        # return the action a in Actions(s) with the highest minimax_value(Result(s,a))
        actions = gameState.getLegalActions(0) # pacman's actions
        bestScore = float("-inf")
        bestAction = None
        self.nodesCount += 1
        for action in actions:
            successorGameState = gameState.generateSuccessor(0, action)
            score = self.minimax_value(successorGameState, 0, 1)
            if score > bestScore:
                bestScore = score
                bestAction = action
        with open('MinimaxAgent.txt', 'a') as f:
            f.write(f"\n {self.nodesCount}")
        return bestAction

    def minimax_value(self, gameState, depth, agentIndex):
        self.nodesCount += 1
        if gameState.isWin() or gameState.isLose() or depth == self.depth: # if Terminal-Test(s) then return Utility(s)
            return self.evaluationFunction(gameState)
        if agentIndex == 0: # pacman
            return self.max_value(gameState, depth, agentIndex) # if Player(s) = MAX then return maxa in Actions(s) minimax_value(Result(s,a))
        else:
            return self.min_value(gameState, depth, agentIndex) # if Player(s) = MIN then return mina in Actions(s) minimax_value(Result(s,a))

    def max_value(self, gameState, depth, agentIndex): # for pacman
        v = float("-inf")
        for action in gameState.getLegalActions(agentIndex):
            successorGameState = gameState.generateSuccessor(agentIndex, action)
            v = max(v, self.minimax_value(successorGameState, depth, agentIndex + 1))
        return v

    def min_value(self, gameState, depth, agentIndex): # for ghosts
        v = float("inf")
        for action in gameState.getLegalActions(agentIndex):
            successorGameState = gameState.generateSuccessor(agentIndex, action)
            if agentIndex == gameState.getNumAgents() - 1: # last ghost
                v = min(v, self.minimax_value(successorGameState, depth + 1, 0)) # next depth
            else:
                v = min(v, self.minimax_value(successorGameState, depth, agentIndex + 1)) # next ghost
        return v
# q3
class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        # util.raiseNotDefined()
        self.nodesCount = 0
        # function decision(s) returns an action
        # return the action a in Actions(s) with the highest minimax_value(Result(s,a))
        actions = gameState.getLegalActions(0) # pacman's actions
        bestScore = float("-inf") # alpha
        bestAction = None
        self.nodesCount += 1
        for action in actions:
            successorGameState = gameState.generateSuccessor(0, action)
            score = self.minimax_value(successorGameState, 0, 1, bestScore, float("inf"))
            if score > bestScore:
                bestScore = score
                bestAction = action
        with open('AlphaBetaAgent.txt', 'a') as f:
            f.write(f"\n {self.nodesCount}")
        return bestAction

    def minimax_value(self, gameState, depth, agentIndex, alpha, beta):
        self.nodesCount += 1
        if gameState.isWin() or gameState.isLose() or depth == self.depth:
            return self.evaluationFunction(gameState)
        if agentIndex == 0: # pacman
            return self.max_value(gameState, depth, agentIndex, alpha, beta)
        else:
            return self.min_value(gameState, depth, agentIndex, alpha, beta)

    def max_value(self, gameState, depth, agentIndex, alpha, beta):
        v = float("-inf")
        for action in gameState.getLegalActions(agentIndex):
            successorGameState = gameState.generateSuccessor(agentIndex, action)
            v = max(v, self.minimax_value(successorGameState, depth, agentIndex + 1, alpha, beta))
            if v > beta:
                return v
            alpha = max(alpha, v)
        return v

    def min_value(self, gameState, depth, agentIndex, alpha, beta):
        v = float("inf")
        for action in gameState.getLegalActions(agentIndex):
            successorGameState = gameState.generateSuccessor(agentIndex, action)
            if agentIndex == gameState.getNumAgents() - 1:
                v = min(v, self.minimax_value(successorGameState, depth + 1, 0, alpha, beta))
                if v < alpha:
                    return v
                beta = min(beta, v)
            else:
                v = min(v, self.minimax_value(successorGameState, depth, agentIndex + 1, alpha, beta))
                if v < alpha:
                    return v
                beta = min(beta, v)
        return v
# q4
class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        # util.raiseNotDefined()
        self.nodesCount = 0
        # function decision(s) returns an action
        # return the action a in Actions(s) with the highest minimax_value(Result(s,a))
        actions = gameState.getLegalActions(0) # pacman's actions
        bestScore = float("-inf") # alpha
        bestAction = None
        self.nodesCount += 1
        for action in actions:
            successorGameState = gameState.generateSuccessor(0, action)
            score = self.minimax_value(successorGameState, 0, 1)
            if score > bestScore:
                bestScore = score
                bestAction = action
        return bestAction

    def minimax_value(self, gameState, depth, agentIndex):
        self.nodesCount += 1
        if gameState.isWin() or gameState.isLose() or depth == self.depth:
            return self.evaluationFunction(gameState)
        if agentIndex == 0: # pacman
            return self.max_value(gameState, depth, agentIndex)
        else:
            return self.expectation(gameState, depth, agentIndex)

    def max_value(self, gameState, depth, agentIndex):
        v = float("-inf")
        for action in gameState.getLegalActions(agentIndex):
            successorGameState = gameState.generateSuccessor(agentIndex, action)
            v = max(v, self.minimax_value(successorGameState, depth, agentIndex + 1))
        return v

    def expectation(self, gameState, depth, agentIndex):
        # assume you will only be running against an adversary that chooses among its getLegalActions uniformly at random.
        v = 0
        for action in gameState.getLegalActions(agentIndex):
            successorGameState = gameState.generateSuccessor(agentIndex, action)
            if agentIndex == gameState.getNumAgents() - 1:
                v += self.minimax_value(successorGameState, depth + 1, 0)
            else:
                v += self.minimax_value(successorGameState, depth, agentIndex + 1)
        return v / len(gameState.getLegalActions(agentIndex))

# q5
def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    # util.raiseNotDefined()
    Pos = currentGameState.getPacmanPosition() # (3, 8) 
    Food = currentGameState.getFood()
    Capsules = currentGameState.getCapsules()
    GhostStates = currentGameState.getGhostStates() #  [<game.AgentState object at 0x00000211085E65B0>, <game.AgentState object at 0x00000211085E65E0>]
    ScaredTimes = [
        ghostState.scaredTimer for ghostState in GhostStates] # [40, 40] down to  [0, 0]
    evaluation_value = currentGameState.getScore() # or 0
    for food in Food.asList(): # [(1, 5), (1, 7), (2, 6), (2, 8), (3, 5), (3, 7)]
        evaluation_value += 1 / manhattanDistance(food, Pos)
    evaluation_value += (2 - len(Capsules))*200 # suppose there are 2 capsules at start (if changed, change 2 to len(Capsules) at start of the game or comment this)
    for capsule in Capsules: # [(1, 1), (5, 1)]
        evaluation_value += (1 / manhattanDistance(capsule, Pos))*3 # 3(or 2 could be) is a weight
    for i in range(len(GhostStates)):
        ghost = GhostStates[i]
        if manhattanDistance(ghost.getPosition(), Pos) < 2:
            if ScaredTimes[i] > 2:
                evaluation_value += 1000
            else:
                evaluation_value -= 1000
    return evaluation_value # 131.0



# Abbreviation
better = betterEvaluationFunction
