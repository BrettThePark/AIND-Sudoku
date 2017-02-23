# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  
A: In the case of naked twins (or triplets, quadruplets, etc) we know that if the available solutions for a box are identical to that of other boxes in a unit and number of possibles digits for that box is also identical to the number of identical boxes, then the solution for those digits must be wholy contained within the set of boxes that have the identical digits. In the case of twins, if two boxes in a unit have two identical possible values (A,B) then we know that all other boxes cannot contain A or B.

# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  
A: The diagonal sudoku problem is a minor addition to the general sudoku problem. In order to use it we must treat the two diagonals as two additional units. When performing the elimate, only choice, or naked twin constraint method we simply consider the diagonal units as two additional units that need to be solved since they share the same constraints as the rest of the units (each diagonal unit must contain one and only one value from 1-9).

### Install

This project requires **Python 3**.

We recommend students install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project. 
Please try using the environment we provided in the Anaconda lesson of the Nanodegree.

##### Optional: Pygame

Optionally, you can also install pygame if you want to see your visualization. If you've followed our instructions for setting up our conda environment, you should be all set.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

### Code

* `solutions.py` - You'll fill this in as part of your solution.
* `solution_test.py` - Do not modify this. You can test your solution by running `python solution_test.py`.
* `PySudoku.py` - Do not modify this. This is code for visualizing your solution.
* `visualize.py` - Do not modify this. This is code for visualizing your solution.

### Visualizing

To visualize your solution, please only assign values to the values_dict using the ```assign_values``` function provided in solution.py

### Data

The data consists of a text file of diagonal sudokus for you to solve.