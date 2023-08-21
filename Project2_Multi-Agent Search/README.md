# Multi-Agent Search
<p align="center">
  <a href="https://inst.eecs.berkeley.edu/~cs188/sp20/assets/images/pacman_multi_agent.png">
    <img src="https://inst.eecs.berkeley.edu/~cs188/sp20/assets/images/pacman_multi_agent.png" alt="Multi_Agent" width="400" height="300">
  </a>
</p>

------------------

## Introduction

In this project, you will design agents for the classic version of Pacman, including ghosts. Along the way, you will implement both minimax and expectimax search and try your hand at evaluation function design.

The code base has not changed much from the previous project, but please start with a fresh installation, rather than intermingling files from project 1.

### Getting Started

To begin, you will need to clone or download the project repository. After obtaining the project files, follow these steps:

1. Unzip the downloaded [`multiagent.zip`](https://inst.eecs.berkeley.edu/~cs188/su21/assets/files/multiagent.zip) file.
2. Navigate to the project directory using your command line terminal.

### Running the Autograder

As in Project 1, this project includes an autograder for you to grade your answers on your machine. This can be run on all questions with the command:
```
python autograder.py
```
This will evaluate your implemented solutions and provide feedback on your progress.
It can be run for one particular question, such as q2, by:
```
python autograder.py -q q2
```

### Project Structure
The project code is organized into several Python files. You'll mainly work with the following file: 

- `multiAgents.py`: Where all of your multi-agent search agents will reside.

You should focus on editing this file to complete the project's assignments.

## Welcome to Multi-Agent Pacman
Once you've set up the project, you can play a game of Pacman by running the following command:
```
python pacman.py
```
and using the arrow keys to move. Now, run the provided `ReflexAgent` in `multiAgents.py`:
```
python pacman.py -p ReflexAgent
```
Note that it plays quite poorly even on simple layouts:
```
python pacman.py -p ReflexAgent -l testClassic
```
### Question1 : Reflex Agent
Improve the `ReflexAgent` in `multiAgents.py` to play respectably. The provided reflex agent code provides some helpful examples of methods that query the GameState for information. A capable reflex agent will have to consider both food locations and ghost locations to perform well. 

### Question2: Minimax
Now you will write an adversarial search agent in the provided `MinimaxAgent` class stub in `multiAgents.py`. Your minimax agent should work with any number of ghosts, so you’ll have to write an algorithm that is slightly more general than what you’ve previously seen in lecture. In particular, your minimax tree will have multiple min layers (one for each ghost) for every max layer.

Your code should also expand the game tree to an arbitrary depth. Score the leaves of your minimax tree with the supplied `self.evaluationFunction`, which defaults to `scoreEvaluationFunction`. `MinimaxAgent` extends `MultiAgentSearchAgent`, which gives access to `self.depth` and `self.evaluationFunction`. Make sure your minimax code makes reference to these two variables where appropriate as these variables are populated in response to command line options.
### Question3: Alpha-Beta Pruning
Make a new agent that uses alpha-beta pruning to more efficiently explore the minimax tree, in AlphaBetaAgent. Again, your algorithm will be slightly more general than the pseudocode from lecture, so part of the challenge is to extend the alpha-beta pruning logic appropriately to multiple minimizer agents.
The pseudo-code below represents the algorithm you should implement for this question.
<p align="center">
  <a href="https://inst.eecs.berkeley.edu/~cs188/sp20/assets/images/alpha_beta_impl.png">
    <img src="https://inst.eecs.berkeley.edu/~cs188/sp20/assets/images/alpha_beta_impl.png" alt="Alpha_Beta">
  </a>
</p>

### Question4 : Expectimax
Minimax and alpha-beta are great, but they both assume that you are playing against an adversary who makes optimal decisions. As anyone who has ever won tic-tac-toe can tell you, this is not always the case. In this question you will implement the `ExpectimaxAgent`, which is useful for modeling probabilistic behavior of agents who may make suboptimal choices.

Once your algorithm is working on small trees, you can observe its success in Pacman. Random ghosts are of course not optimal minimax agents, and so modeling them with minimax search may not be appropriate. ExpectimaxAgent, will no longer take the min over all ghost actions, but the expectation according to your agent’s model of how the ghosts act. To simplify your code, assume you will only be running against an adversary which chooses amongst their `getLegalActions` uniformly at random.

### Question5 : Evaluation Function
Write a better evaluation function for pacman in the provided function `betterEvaluationFunction`. The evaluation function should evaluate states, rather than actions like your reflex agent evaluation function did. With depth 2 search, your evaluation function should clear the `smallClassic` layout with one random ghost more than half the time and still run at a reasonable rate (to get full credit, Pacman should be averaging around 1000 points when he’s winning).

## My Grades
------------------

Question q1: 4/4

Question q2: 5/5

Question q3: 5/5

Question q4: 5/5

Question q5: 6/6

------------------
Total: 25/25