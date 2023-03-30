# valueIterationAgents.py
# -----------------------
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


# valueIterationAgents.py
# -----------------------
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


import mdp, util

from learningAgents import ValueEstimationAgent
import collections

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0
        self.runValueIteration()

    def runValueIteration(self):
        # Write value iteration code here
        "*** YOUR CODE HERE ***"
        # for calculating value iteration we have this formula:
        #    V_k+1(s) = max_a ( sigma_s'( T(s,a,s')*[R(s,a,s') + gamma*V_k(s')] ) )
        # also instead of that we can use this formula:
        #    V_k+1(s) = max_a ( Q(s, a) )
        # and instead of calculating max on different possible action we can find policy according to current q values at first
        # then we use this formula:
        #    V_k+1(s) = Q(s, policy)
        for k in range(self.iterations):
            # for each state we find new value with value iteration and store it in new_values
            new_values = util.Counter()
            # in each iteration we do this calculations on all states so we need a loop
            all_states = self.mdp.getStates()
            for state in all_states:
                # only for terminal states we dont run value iteration algorithm
                if not self.mdp.isTerminal(state):
                    # first) we should find the best action according to current values 
                    policy = self.computeActionFromValues(state)
                    # second) from this values we can calculate 
                    newValue = self.computeQValueFromValues(state, policy)
                    # third) add this new value for this state to new_values
                    new_values[state] = newValue
            # update values of all state after iteration k
            self.values = new_values


    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]


    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"
        # our formula for calculating Q value is :
                #QValue = sigma_s' ( T(s,a,s') [R(s,a,s') + gamma * V(s')])
        # so first we should find all possible transactions from current state:
        posssibleTransactions = self.mdp.getTransitionStatesAndProbs(state, action)
        # initialize QValue to 0
        QValue = 0
        # now according to formula we should find T(s,a,s') and R(s,a,s') and V(s')
        #   state = s
        #   next_state = s' 
        #   T = T(s,a,s')
        #   R = R(s,a,s')
        #   discount = gamma
        for next_state, T in posssibleTransactions:
            # calculate R(s,a,s')
            R = self.mdp.getReward(state, action, next_state)
            # calculate V(s')
            V_next_state = self.getValue(next_state)
            # find gamma value (discount factor)
            discount = self.discount
            # finally calculate QValue according to formula
            QValue += T * (R + discount * V_next_state)
        return QValue

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"
        # according to above explanation we should check if we are in terminal state then return None
        if self.mdp.isTerminal(state):
            return None
        # according to below figure we should calculate QValue for current state and all possible actions(mabe some q aren`t accessible`)
        # ---------
        # | \ q1 / |
        # |q4 \/ q2|
        # |   /\   |
        # | / q3 \ |
        # ----------
        # then for finding policy or best action we have this formula:
        #    policy(s) = argmax_a (Qvalue(s,a))
        # so first we should find all possible actions in current state
        possible_actions = self.mdp.getPossibleActions(state)
        # with the help of util.counter we can create a dict of qvalues according to each action
        QValues = util.Counter()
        # then we can calculate QValue for each action with computeQValueFromValues() function
        for action in possible_actions:
            QValues[action] = self.computeQValueFromValues(state, action)

        policy = QValues.argMax()
        return policy

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)

class AsynchronousValueIterationAgent(ValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        An AsynchronousValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs cyclic value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 1000):
        """
          Your cyclic value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy. Each iteration
          updates the value of only one state, which cycles through
          the states list. If the chosen state is terminal, nothing
          happens in that iteration.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state)
              mdp.isTerminal(state)
        """
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):
        "*** YOUR CODE HERE ***"
        # for calculating value iteration we have this formula:
        #    V_k+1(s) = max_a ( sigma_s'( T(s,a,s')*[R(s,a,s') + gamma*V_k(s')] ) )
        # also instead of that we can use this formula:
        #    V_k+1(s) = max_a ( Q(s, a) )
        # and instead of calculating max on different possible action we can find policy according to current q values at first
        # then we use this formula:
        #    V_k+1(s) = Q(s, policy)

        # first we need the list of all states
        states = self.mdp.getStates()
        # then we need a loop in range of given iterations
        for iteration in range(self.iterations):
            # in each iteration we just update one state
            # for example in itertion1 we update state1 and go on
            # so we need the index of state in states list and then find it
            state_index = iteration % len(states)
            purpose_state = states[state_index]
            # according to problem if the state is terminal we shouldnt update anything in that iteration
            if self.mdp.isTerminal(purpose_state):
                continue
            # first) we should find the best action according to current values for purpose_state
            policy = self.computeActionFromValues(purpose_state)
            # second) according to best action(policy) we can find the maximum value
            value = self.computeQValueFromValues(purpose_state, policy)
            # then we can update the value of purpose_state in current iteration
            self.values[purpose_state] = value

class PrioritizedSweepingValueIterationAgent(AsynchronousValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A PrioritizedSweepingValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs prioritized sweeping value iteration
        for a given number of iterations using the supplied parameters.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100, theta = 1e-5):
        """
          Your prioritized sweeping value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy.
        """
        self.theta = theta
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):
        "*** YOUR CODE HERE ***"
        all_states = self.mdp.getStates()
        # 1) we need to hold predecessors of all states and compute them
        #    1-1) define predecessors variable with util.counter()
        self.predecessors = util.Counter()
        #    1-2) for holding the predecessors we need to set because of avoiding duplicates
        for state in all_states:
            if not self.mdp.isTerminal(state):
                # define set
                self.predecessors[state] = set()
        #    1-3) we should calculate and initialize predecessors of each state      
        for state in all_states:
            if not self.mdp.isTerminal(state):
                # calculate predecessors
                # according to definition of predecessors:
                #    predecessors of a state s as all states that have a nonzero probability of reaching s by taking some action a
                allowable_actions = self.mdp.getPossibleActions(state)
                for action in allowable_actions:
                    allowable_transitions = self.mdp.getTransitionStatesAndProbs(state, action)
                    for next_state, T in allowable_transitions:
                        if not self.mdp.isTerminal(next_state) and T != 0 :
                            self.predecessors[next_state].add(state)

        # 2) define an empty priority queue for holding priority
        self.queue = util.PriorityQueue()

        # 3) For each non-terminal state
        for state in self.mdp.getStates():
            if not self.mdp.isTerminal(state):
                # 3-1) calculate priority and store it in variable diff
                current_value = self.values[state]
                policy = self.computeActionFromValues(state)
                maximum_QValue = self.computeQValueFromValues(state, policy)
                diff = abs(current_value - maximum_QValue)
                # 3-2) push the state with calculated diff in priority queue
                self.queue.push(state, -diff)

        # 4) for designated iterations (in self.iterations):
        for iteration in range(self.iterations):
            # 4-1) If the priority queue is empty, then terminate.
            if self.queue.isEmpty():
                return
            # 4-2) else pop a state s off the priority queue.
            s = self.queue.pop()
            # 4-3) Update the value of s if it is not a terminal state 
            #      Note: in step3 we push non-terminal states in queue so we dont need check again
            policy = self.computeActionFromValues(s)
            self.values[s] = self.computeQValueFromValues(s, policy)
            # 4-4) For each predecessor p of s, do:
            for p in self.predecessors[s]:
                # 4-4-1) calculate the value of variable diff 
                current_value = self.values[p]
                policy = self.computeActionFromValues(p)
                maximum_QValue = self.computeQValueFromValues(p, policy)
                diff = abs(current_value - maximum_QValue)
                # 4-4-2) If diff > theta, push p into the priority queue with priority -diff
                if diff > self.theta:
                    self.queue.update(p, -diff)