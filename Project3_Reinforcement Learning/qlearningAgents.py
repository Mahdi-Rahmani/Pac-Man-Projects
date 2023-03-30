# qlearningAgents.py
# ------------------
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


from game import *
from learningAgents import ReinforcementAgent
from featureExtractors import *

import random,util,math

class QLearningAgent(ReinforcementAgent):
    """
      Q-Learning Agent

      Functions you should fill in:
        - computeValueFromQValues
        - computeActionFromQValues
        - getQValue
        - getAction
        - update

      Instance variables you have access to
        - self.epsilon (exploration prob)
        - self.alpha (learning rate)
        - self.discount (discount rate)

      Functions you should use
        - self.getLegalActions(state)
          which returns legal actions for a state
    """
    def __init__(self, **args):
        "You can initialize Q-values here..."
        ReinforcementAgent.__init__(self, **args)

        "*** YOUR CODE HERE ***"
        #  we can initialize all QValues in form of (state, action) pair to 0
        #  key = (state, action)   val = value
        self.QValues = util.Counter()

    def getQValue(self, state, action):
        """
          Returns Q(state,action)
          Should return 0.0 if we have never seen a state
          or the Q node value otherwise
        """
        "*** YOUR CODE HERE ***"
        # it returns 0.0 if we never seen a state. we initialize it before to 0
        # otherwise return Q node value
        return self.QValues[(state, action)]


    def computeValueFromQValues(self, state):
        """
          Returns max_action Q(state,action)
          where the max is over legal actions.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return a value of 0.0.
        """
        "*** YOUR CODE HERE ***"
        # first we should find legal actions
        legal_actions = self.getLegalActions(state)
        # according to above explanation if there are no legal actions 
        # then we should return 0.0 . we can check this by find length of 
        # legal_actions list. if the length is 0 we return 0.0
        if len(legal_actions) == 0:
            return 0.0
        
        # now we should find best or in other word max_action
        # for do that we can use getPolicy function
        max_action = self.getPolicy(state)
        # now we can calculate the value related to max_action
        value = self.getQValue(state, max_action)
        return value

    def computeActionFromQValues(self, state):
        """
          Compute the best action to take in a state.  Note that if there
          are no legal actions, which is the case at the terminal state,
          you should return None.
        """
        "*** YOUR CODE HERE ***"
        # like previous function we should first find legal actions
        legal_actions = self.getLegalActions(state)
        # according to above explanation if there are no legal actions 
        # then we should return 0.0 . we can check this by find length of 
        # legal_actions list. if the length is 0 we return None
        if len(legal_actions) == 0:
            return None
        # now we can store the pairs of legal_action and its Qvalue as a dictionary
        legalAction_Qvalue = {legal_action:self.getQValue(state, legal_action) for legal_action in legal_actions}
        # now we should find the maximum QValue of the actions
        maximum_QValue = max(legalAction_Qvalue.values())
        # maybe we have multiple actions wuth maximum_QValue
        # so we store them in a list
        best_actions = [action for action, value in legalAction_Qvalue.items() if value == maximum_QValue]
        # now we can choose one of the actions in best_actions list randomly
        return random.choice(best_actions)

    def getAction(self, state):
        """
          Compute the action to take in the current state.  With
          probability self.epsilon, we should take a random action and
          take the best policy action otherwise.  Note that if there are
          no legal actions, which is the case at the terminal state, you
          should choose None as the action.

          HINT: You might want to use util.flipCoin(prob)
          HINT: To pick randomly from a list, use random.choice(list)
        """
        # Pick Action
        legalActions = self.getLegalActions(state)
        action = None
        "*** YOUR CODE HERE ***"
        # according to above explanation if there are no legal actions we should return None as the action
        if len(legalActions) == 0:
            return action
        # flipCoin get a probability as an entry and with that probability it returns true
        # here our probability is epsilon. so we give it to flipCoin function
        # with probability epsilon we should take a random action
        if util.flipCoin(self.epsilon):
            # in the other words we (explore) with probabilty epsilon
            action = random.choice(legalActions)
        # with probability 1-epsilon we take the best policy action 
        else:
            # we (exploit) with probability 1-epsilon 
            action = self.getPolicy(state)
            
        return action

    def update(self, state, action, nextState, reward):
        """
          The parent class calls this to observe a
          state = action => nextState and reward transition.
          You should do your Q-Value update here

          NOTE: You should never call this function,
          it will be called on your behalf
        """
        "*** YOUR CODE HERE ***"
        # for updating QValue we have the below formula:
        #    Q(s,a) = (1-alpha)*Q(s,a) + alpha * sample
        # the sample formula is:
        #    sample = R(s,a,s') + gamma * max_a'(Q(s',a'))
        # 1) first we find the values of the above variables of formulas
        R = reward
        gamma = self.discount
        Q_s_a = self.getQValue(state,action)
        future_QValue = self.getValue(nextState)
        # 2) now we can calculate sample value
        sample = R + gamma * future_QValue
        # 3) then we can find the new value of QValue with that formula
        new_Q_s_a = (1-self.alpha) * Q_s_a + self.alpha * sample
        # 4) now we can update QValue 
        self.QValues[(state, action)] = new_Q_s_a

    def getPolicy(self, state):
        return self.computeActionFromQValues(state)

    def getValue(self, state):
        return self.computeValueFromQValues(state)


class PacmanQAgent(QLearningAgent):
    "Exactly the same as QLearningAgent, but with different default parameters"

    def __init__(self, epsilon=0.05,gamma=0.8,alpha=0.2, numTraining=0, **args):
        """
        These default parameters can be changed from the pacman.py command line.
        For example, to change the exploration rate, try:
            python pacman.py -p PacmanQLearningAgent -a epsilon=0.1

        alpha    - learning rate
        epsilon  - exploration rate
        gamma    - discount factor
        numTraining - number of training episodes, i.e. no learning after these many episodes
        """
        args['epsilon'] = epsilon
        args['gamma'] = gamma
        args['alpha'] = alpha
        args['numTraining'] = numTraining
        self.index = 0  # This is always Pacman
        QLearningAgent.__init__(self, **args)

    def getAction(self, state):
        """
        Simply calls the getAction method of QLearningAgent and then
        informs parent of action for Pacman.  Do not change or remove this
        method.
        """
        action = QLearningAgent.getAction(self,state)
        self.doAction(state,action)
        return action


class ApproximateQAgent(PacmanQAgent):
    """
       ApproximateQLearningAgent

       You should only have to overwrite getQValue
       and update.  All other QLearningAgent functions
       should work as is.
    """
    def __init__(self, extractor='IdentityExtractor', **args):
        self.featExtractor = util.lookup(extractor, globals())()
        PacmanQAgent.__init__(self, **args)
        self.weights = util.Counter()

    def getWeights(self):
        return self.weights

    def getQValue(self, state, action):
        """
          Should return Q(state,action) = w * featureVector
          where * is the dotProduct operator
        """
        "*** YOUR CODE HERE ***"
        # first we should find features vector
        features_vector = self.featExtractor.getFeatures(state, action)
        QValue = features_vector * self.weights
        return QValue

    def update(self, state, action, nextState, reward):
        """
           Should update your weights based on transition
        """
        "*** YOUR CODE HERE ***"
        # according to explanation of project we have this formula:
        #   W_i = W_i + alpha * difference *f_i(s,a)
        # also the difference formula is:
        #   difference = (r + gamma * max_a'(Q(s',a'))) - Q(s,a)
        # 1) first we find the values of the above variables of formulas
        features_vector = self.featExtractor.getFeatures(state, action)
        Q_s_a = self.getQValue(state, action)
        future_QValue = self.getValue(nextState)
        r = reward
        gamma = self.discount
        # 2) now we can calculate difference with formula
        difference = (r + gamma * future_QValue) - Q_s_a
        # 3) now we can update weight i for each feature i
        for feature in features_vector:
            self.weights[feature] = self.weights[feature] + self.alpha * difference * features_vector[feature]

    def final(self, state):
        "Called at the end of each game."
        # call the super-class final method
        PacmanQAgent.final(self, state)

        # did we finish training?
        if self.episodesSoFar == self.numTraining:
            # you might want to print your weights here for debugging
            "*** YOUR CODE HERE ***"
            pass
