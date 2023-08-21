# Search
<p align="center">
  <a href="https://inst.eecs.berkeley.edu/~cs188/sp20/assets/images/maze.png">
    <img src="https://inst.eecs.berkeley.edu/~cs188/sp20/assets/images/maze.png" alt="Maze Image" width="300" height="200">
  </a>
</p>

------------------

## Introduction

Welcome to the Pacman Maze Solver project! In this project, your task is to create an intelligent Pacman agent that can navigate through mazes, reach specific locations, and efficiently collect food. You will implement various search algorithms and apply them to different Pacman scenarios to showcase its problem-solving capabilities.

### Getting Started

To begin, you will need to clone or download the project repository. After obtaining the project files, follow these steps:

1. Unzip the downloaded [`search.zip`](https://inst.eecs.berkeley.edu/~cs188/su20/assets/files/search.zip) file.
2. Navigate to the project directory using your command line terminal.

### Running the Autograder

The project includes an autograder that enables you to assess your solutions locally. To run the autograder, execute the following command in your terminal:

```
python autograder.py
```
This will evaluate your implemented solutions and provide feedback on your progress.

### Project Structure
The project code is organized into several Python files. You'll mainly work with the following files: 

- `search.py`: Implement your general search algorithms here 

- `searchAgents.py`: Define agents that utilize your search algorithms. 

You should focus on editing these files to complete the project's assignments.

## Welcome to Pacman
Once you've set up the project, you can play a game of Pacman by running the following command:
```
python pacman.py
```
Pacman resides in a colorful maze filled with corridors and delicious treats. Efficiently navigating this maze is crucial for Pacman's success.
The initial agent provided is called the GoWestAgent. It always moves West and is a basic example of a reflex agent. You can try it out with the following commands:

For a simple layout:
```
python pacman.py --layout testMaze --pacman GoWestAgent
```
For a more challenging layout:
```
python pacman.py --layout tinyMaze --pacman GoWestAgent
```
If Pacman gets stuck, you can exit the game by pressing `CTRL-c` in your terminal.

Your ultimate goal is to develop an agent that can solve not only `tinyMaze` but also any maze you encounter.

The `pacman.py` script supports various command-line options. To view a list of all available options and their default values, use the following command:
```
python pacman.py -h
```
For your convenience, all commands mentioned in this project are also compiled in the `commands.txt` file, allowing for easy copying and pasting. On UNIX/Mac OS X systems, you can even execute all these commands in sequence using the following bash command:
```
bash commands.txt
```
### Question1 to Question4: DFS-BFS-UCS-A* algorithms
Each algorithm is very similar. Algorithms for DFS, BFS, UCS, and A* differ only in the details of how the fringe is managed. So, concentrate on getting DFS right and the rest should be relatively straightforward. Indeed, one possible implementation requires only a single generic search method which is configured with an algorithm-specific queuing strategy. (Your implementation need not be of this form to receive full credit).

The idea is to check the node if has been visited before. Then you push it to visited list and check if we reached goalState - if not expand children based on algorithm.
### Question5: Finding All the Corners
The real strength of the A* algorithm comes into play when dealing with complex search challenges. In this context, a fresh problem needs to be formulated, along with the creation of an appropriate heuristic.

In corner mazes, where each corner has a dot, a new search problem is introduced. The objective is to determine the shortest route through the maze while touching all four corners, regardless of whether there is food in those corners. It's worth noting that, for certain mazes like tinyCorners, the most efficient path may not necessarily lead to the closest food first. A hint is provided that the optimal path through tinyCorners involves 28 steps.

The task involves creating the `CornersProblem` search problem within `searchAgents.py`.
### Question6: Corners Problem: Heuristic
To enhance the performance of the CornersProblem in the cornersHeuristic, develop a heuristic that is both non-trivial and consistent. 
- Implementing an Effective Heuristic:

    - The goal is to design a heuristic that is significant and contributes to the efficiency of the CornersProblem.
    - This heuristic should be consistent and provide reliable cost estimates to the nearest goal.
- Admissibility vs. Consistency:

    - Heuristics are functions that estimate the cost to reach a nearest goal from a given search state.
    - Admissible heuristics offer lower bound estimates on the actual shortest path cost to the nearest goal, ensuring non-negativity.
    - Consistency goes a step further; it ensures that if an action has a cost c, then that action won't lead to a heuristic decrease of more than c.
- Admissibility and Consistency Importance:

    - While admissibility is necessary, consistency is more robust for graph search correctness.
    - Admissible heuristics often align with consistency, particularly when derived from problem simplifications.
- Non-Trivial Heuristics:

    - Trivial heuristics, returning zero (UCS) or true completion cost, are ineffective.
    - The former doesn't improve computation time, and the latter may lead to timeouts.
    - A desirable heuristic minimizes computation time; the autograder checks node counts primarily for this assignment.

By developing a heuristic that is both non-trivial and consistent for the CornersProblem, you will optimize the efficiency of the search and improve the effectiveness of the solution. Admissibility and consistency are key principles in constructing useful heuristics.
### Question7 : Eating All The Dots
Now we’ll solve a hard search problem: eating all the Pacman food in as few steps as possible. For this, we’ll need a new search problem definition which formalizes the food-clearing problem: `FoodSearchProblem` in `searchAgents.py` (implemented for you). A solution is defined to be a path that collects all of the food in the Pacman world. For the present project, solutions do not take into account any ghosts or power pellets; solutions only depend on the placement of walls, regular food and Pacman.

Fill in `foodHeuristic` in `searchAgents.py` with a consistent heuristic for the `FoodSearchProblem`. Our UCS agent finds the optimal solution in about 13 seconds, exploring over 16,000 nodes.

### Question8 : Suboptimal Search
Sometimes, even with A* and a good heuristic, finding the optimal path through all the dots is hard. In these cases, we’d still like to find a reasonably good path, quickly. In this section, you’ll write an agent that always greedily eats the closest dot. `ClosestDotSearchAgent` is implemented for you in `searchAgents.py`, but it’s missing a key function that finds a path to the closest dot.

Implement the function `findPathToClosestDot` in `searchAgents.py`. Our agent solves this maze (suboptimally!) in under a second with a path cost of 350.

## My Grades
------------------

Question q1: 3/3

Question q2: 3/3

Question q3: 3/3

Question q4: 3/3

Question q5: 3/3

Question q6: 3/3

Question q7: 4/4

Question q8: 3/3

------------------
Total: 25/25