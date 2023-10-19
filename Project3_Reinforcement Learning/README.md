# Reinforcement Learning
<p align="center">
  <a href="https://github.com/Mahdi-Rahmani/Pac-Man-Projects/blob/main/Project3_Reinforcement%20Learning/pics/RL.png">
    <img src="https://github.com/Mahdi-Rahmani/Pac-Man-Projects/blob/main/Project3_Reinforcement%20Learning/pics/RL.png" alt="RL Image">
  </a>
</p>

------------------

## Introduction

In this project, you will implement value iteration and Q-learning. You will test your agents first on Gridworld (from class), then apply them to a simulated robot controller (Crawler) and Pacman.

### Getting Started

To begin, you will need to clone or download the project repository. After obtaining the project files, follow these steps:

1. Unzip the downloaded [`reinforcement.zip`](https://inst.eecs.berkeley.edu/~cs188/su21/assets/files/reinforcement.zip) file.
2. Navigate to the project directory using your command line terminal.

### Running the Autograder

The project includes an autograder that enables you to assess your solutions locally. To run the autograder, execute the following command in your terminal:

```
python autograder.py
```
This will evaluate your implemented solutions and provide feedback on your progress.

### Project Structure
The project code is organized into several Python files. You'll mainly work with the following files: 

- `valueIterationAgents.py`: A value iteration agent for solving known MDPs.

- `qlearningAgents.py`: Q-learning agents for Gridworld, Crawler and Pacman. 

- `analysis.py`: A file to put your answers to questions given in the project.

You should focus on editing these files to complete the project's assignments.

## Welcome to Pacman MDPs
To get started, run Gridworld in manual control mode, which uses the arrow keys:

```
python gridworld.py -m
```
You will see the two-exit layout from class. The blue dot is the agent. Note that when you press up, the agent only actually moves north 80% of the time. Such is the life of a Gridworld agent!

You can control many aspects of the simulation. A full list of options is available by running:
```
python gridworld.py -h
```
The default agent moves randomly
```
python gridworld.py -g MazeGrid
```
You should see the random agent bounce around the grid until it happens upon an exit. Not the finest hour for an AI agent.

### Question1: Value Iteration
Recall the value iteration state update equation:
<p align="center">
  <a href="https://inst.eecs.berkeley.edu/~cs188/sp20/assets/images/bellman2.png">
    <img src="https://inst.eecs.berkeley.edu/~cs188/sp20/assets/images/bellman2.png" alt="Belman Image">
  </a>
</p>

According to above formula, in the ValueIterationAgent, you need to implement a value iteration planner with a specified number of iterations. Value iteration computes k-step estimates of optimal values, V_k, and you should implement methods to compute the best action and Q-value based on these values. Use the "batch" version of value iteration where each V_k is computed from the previous V_(k-1). The policy and Q-values should reflect one more reward than the values, i.e., π_(k+1) and Q_(k+1). Handle cases where a state has no available actions in an MDP, considering their impact on future rewards. The agent computes these values based on a given MDP and returns the synthesized policy π_(k+1). 

On the default BookGrid, running value iteration for 5 iterations should give you this output:
<p align="center">
  <a href="https://inst.eecs.berkeley.edu/~cs188/sp20/assets/images/value.png">
    <img src="https://inst.eecs.berkeley.edu/~cs188/sp20/assets/images/value.png" alt="Res1 Image" width=500 height=400>
  </a>
</p>

### Question2: Bridge Crossing Analysis
`BridgeGrid` is a grid world map with the a low-reward terminal state and a high-reward terminal state separated by a narrow “bridge”, on either side of which is a chasm of high negative reward. The agent starts near the low-reward state. With the default discount of 0.9 and the default noise of 0.2, the optimal policy does not cross the bridge. Change only ONE of the discount and noise parameters so that the optimal policy causes the agent to attempt to cross the bridge. Put your answer in `question2()` of `analysis.py`. (Noise refers to how often an agent ends up in an unintended successor state when they perform an action.)
<p align="center">
  <a href="https://inst.eecs.berkeley.edu/~cs188/sp20/assets/images/value-q2.png">
    <img src="https://inst.eecs.berkeley.edu/~cs188/sp20/assets/images/value-q2.png" alt="Res2 Image" width=500 height=250>
  </a>
</p>

### Question3: Policies
Consider the `DiscountGrid` layout, shown below. This grid has two terminal states with positive payoff (in the middle row), a close exit with payoff +1 and a distant exit with payoff +10. The bottom row of the grid consists of terminal states with negative payoff (shown in red); each state in this “cliff” region has payoff -10. The starting state is the yellow square. We distinguish between two types of paths: (1) paths that “risk the cliff” and travel near the bottom row of the grid; these paths are shorter but risk earning a large negative payoff, and are represented by the red arrow in the figure below. (2) paths that “avoid the cliff” and travel along the top edge of the grid. These paths are longer but are less likely to incur huge negative payoffs. These paths are represented by the green arrow in the figure below.
<p align="center">
  <a href="https://inst.eecs.berkeley.edu/~cs188/sp20/assets/images/discountgrid.png">
    <img src="https://inst.eecs.berkeley.edu/~cs188/sp20/assets/images/discountgrid.png" alt="Res3 Image" width=400 height=350>
  </a>
</p>

In this question, you will choose settings of the discount, noise, and living reward parameters for this MDP to produce optimal policies of several different types. **Your setting of the parameter values for each part should have the property that, if your agent followed its optimal policy without being subject to any noise, it would exhibit the given behavior.** If a particular behavior is not achieved for any setting of the parameters, assert that the policy is impossible by returning the string `'NOT POSSIBLE'`.

Here are the optimal policy types you should attempt to produce:

- Prefer the close exit (+1), risking the cliff (-10)
- Prefer the close exit (+1), but avoiding the cliff (-10)
- Prefer the distant exit (+10), risking the cliff (-10)
- Prefer the distant exit (+10), avoiding the cliff (-10)
- Avoid both exits and the cliff (so an episode should never terminate)

### Question4 : Asynchronous Value Iteration
Create an AsynchronousValueIterationAgent in valueIterationAgents.py that uses cyclic value iteration, updating one state per iteration. It runs for a specified number of iterations during construction and reverts to the first state after updating all states once. If a terminal state is picked, there's no update in that iteration.

As a reminder, here’s the value iteration state update equation:

$`V_{k+1}(s) \leftarrow \max _{a} \sum_{s^{\prime}} T\left(s, a, s^{\prime}\right)\left[R\left(s, a, s^{\prime}\right)+\gamma V_{k}\left(s^{\prime}\right)\right]`$

### Question5 : Prioritized Sweeping Value Iteration
You will now implement `PrioritizedSweepingValueIterationAgent`, which has been partially specified for you in `valueIterationAgents.py`. Note that this class derives from `AsynchronousValueIterationAgent`, so the only method that needs to change is `runValueIteration`, which actually runs the value iteration.

Prioritized sweeping attempts to focus updates of state values in ways that are likely to change the policy.

For this project, you will implement a simplified version of the standard prioritized sweeping algorithm, which is described in this [paper](http://papers.nips.cc/paper/651-memory-based-reinforcement-learning-efficient-computation-with-prioritized-sweeping.pdf). 

### Question6 : Q-Learning
Note that your value iteration agent does not actually learn from experience. Rather, it ponders its MDP model to arrive at a complete policy before ever interacting with a real environment. When it does interact with the environment, it simply follows the precomputed policy (e.g. it becomes a reflex agent). This distinction may be subtle in a simulated environment like a Gridword, but it’s very important in the real world, where the real MDP is not available.

You will now write a Q-learning agent, which does very little on construction, but instead learns by trial and error from interactions with the environment through its `update(state, action, nextState, reward)` method. A stub of a Q-learner is specified in `QLearningAgent` in `qlearningAgents.py`, and you can select it with the option `'-a q'`. For this question, you must implement the `update`, `computeValueFromQValues`, `getQValue`, and `computeActionFromQValues` methods.

### Question7 : Epsilon Greedy
Complete your Q-learning agent by implementing epsilon-greedy action selection in `getAction`, meaning it chooses random actions an epsilon fraction of the time, and follows its current best Q-values otherwise. Note that choosing a random action may result in choosing the best action - that is, you should not choose a random sub-optimal action, but rather any random legal action.

### Question8 : Bridge Crossing Revisited
First, train a completely random Q-learner with the default learning rate on the noiseless BridgeGrid for 50 episodes and observe whether it finds the optimal policy.

Now try the same experiment with an epsilon of 0. Is there an epsilon and a learning rate for which it is highly likely (greater than 99%) that the optimal policy will be learned after 50 iterations?

### Question9 : Q-Learning and Pacman
Time to play some Pacman! Pacman will play games in two phases. In the first phase, training, Pacman will begin to learn about the values of positions and actions. Because it takes a very long time to learn accurate Q-values even for tiny grids, Pacman’s training games run in quiet mode by default, with no GUI (or console) display. Once Pacman’s training is complete, he will enter testing mode. When testing, Pacman’s `self.epsilon` and `self.alpha` will be set to 0.0, effectively stopping Q-learning and disabling exploration, in order to allow Pacman to exploit his learned policy. 

### Question10 : Approximate Q-Learning
Develop an approximate Q-learning agent within the `ApproximateQAgent` class, a subclass of `PacmanQAgent` in `qlearningAgents.py.` This agent learns weightings for state features where multiple states may share the same features. It relies on a feature function, denoted as `f(s, a),` which generates a vector of feature values. These vectors are represented as `util.Counter` objects, containing the non-zero feature-value pairs. Feature functions are available in `featureExtractors.py.`

The approximate Q-function takes the following form:

$`Q(s, a)=\sum_{i=1}^{n} f_{i}(s, a) w_{i}`$

In your code, each weight "w_i" corresponds to a specific feature "f_i(s, a)." You should represent the weight vector as a dictionary that links features (which are generated by the feature extractors) to their respective weight values. You'll adjust and modify these weight vectors in a similar fashion to how you handled updates to Q-values.

$`\begin{array}{c}{w_{i} \leftarrow w_{i}+\alpha \cdot \text {difference} \cdot f_{i}(s, a)} \\ {\text {difference}=\left(r+\gamma \max _{a^{\prime}} Q\left(s^{\prime}, a^{\prime}\right)\right)-Q(s, a)}\end{array}`$

Note that the difference term is the same as in normal Q-learning, and r is the experienced reward.

## My Grades
------------------

Question q1: 4/4

Question q2: 1/1

Question q3: 5/5

Question q4: 1/1

Question q5: 3/3

Question q6: 4/4

Question q7: 2/2

Question q8: 1/1

Question q9: 1/1

Question q10: 3/3

------------------
Total: 25/25
