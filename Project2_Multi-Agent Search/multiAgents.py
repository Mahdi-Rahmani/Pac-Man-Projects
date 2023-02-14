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
import random, util

from game import Agent


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
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices)  # Pick randomly among the best

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
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        return successorGameState.getScore()

        # first we check the ghost scared timer is 0 or not. 
        # if the scared timer is 0 then we calculate our manhattan distance to ghost
        # if the ghost is too close then the evaluation function should return minimum value that possible
        # then because of this bad value pacman dont go to this state
        # if the scared timer is not 0 then we can get closer to ghosts and it doesnt matter
        # so here first we find manhattan distance betwwen pacman and positions of ghost states
        ghostDistances = []
        for ghost_state in newGhostStates:
            if ghost_state.scaredTimer == 0:
                ghostDistances.append(util.manhattanDistance(newPos, ghost_state.getPosition()))
        # if the distance < 2 ( or =0 || =1) exists in ghostDistances it means the ghost may eat us
        if (0 in ghostDistances) or (1 in ghostDistances):
            return -float('inf')

        # we know if we eat food we can get score 
        # first we try find the closest food manhattan distance
        closest_food_dist = float("inf")
        newFood_list = newFood.asList()
        for food in newFood_list:
            closest_food_dist = min(closest_food_dist, manhattanDistance(newPos, food))

        # its better for us to choose shorter distance. so the return value has an inverse relationship with each other
        # so we try to increase the score and eat food but if the food closer, we return higher value
        value = (1.0/closest_food_dist) + successorGameState.getScore()
        return value


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
        
        # we want to choose best action
        # first we should find possible successors for this state of pacman
        # then we should find best action to best successor for get maximum value
        # for do this job we need find the value for possible succesors with the help of value function(minimax algorithm)
        # then we choose maximum value from them and return the action related to that
        value_action = (-float("inf"), None)
        for action in gameState.getLegalActions(self.index):
            new_value_action = ((self.value(gameState.generateSuccessor(self.index, action), 1, 1)), action)
            value_action = max(value_action, new_value_action, key=lambda x:x[0])
        return value_action[1]

    # according to slides our pseudocode for min_value function:
    """
        def min_value(state):
            initialize v = + inf
            for each succesor of state:
                v = min(v, value(successor))
            return v
    """
    def min_value(self, gameState, agentIndex, depth):
        # first step : initialize v = + inf
        v = float("inf")
        # second step : find successors list
        legal_actions = gameState.getLegalActions(agentIndex)
        successor_list = []
        for action in legal_actions:
            successor = gameState.generateSuccessor(agentIndex, action)
            successor_list.append(successor)
        # third step : find minimum value and update v 
        for successor in successor_list:
            v = min(v, (self.value(successor, (agentIndex+1)%gameState.getNumAgents(), depth+1)))
        return v

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()


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
        util.raiseNotDefined()


def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()


# Abbreviation
better = betterEvaluationFunction
