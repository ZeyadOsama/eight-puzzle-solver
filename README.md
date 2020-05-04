# Eight Puzzle Solver
<p>
  <img src="https://img.shields.io/pypi/status/Django.svg"/>
</p>
<p>
Given a 3×3 board with 8 tiles (every tile has one number from 1 to 8) and one empty space. The objective is to place the numbers on tiles to match final configuration using the empty space. We can slide four adjacent (left, right, above and below) tiles into the empty space.
</p>

## Algorithms
A variety of algorithms can be used to achieve the best solution. They vary in their time and space complexity.
* BFS
* DFS
* A*

## Heuristics
For A* algorithm, heuristics should be provided.

#### Manhattan Distance
```
abs(start_point.x - end_point.x) + abs(start_point.y - end_point.y)

```

#### Euclidean Distance
```
math.sqrt(math.pow(start_point.x - end_point.x, 2) + math.pow(start_point.y - end_point.y, 2))

```

## Puzzle State
The PuzzleState Class is the class used to keep track of the states of the puzzle while solving it, When initialized it:
* Gets the current configuration of the puzzle,  the size,  the goal
* Gets the parent state, the move and the cost

## Puzzle Solver
The PuzzleSolver Class is the class used to solve the puzzle, by communicating between the PuzzleState and the Algorithms, when initialized it:
* Gets the initial state entered by the user
* Gets the algorithm chosen by the user to solve it.
* Creates a puzzle state for the puzzle
Checks if a puzzle with the inserted description can be solved

The PuzzleSolver Class has a solve method, when called it:
* Tracks memory resources usage
* Tracks the run time
* Call the solve method from the Algorithms class that checks which algorithm is selected and starts solving the puzzle using it
* Returns an Information object with the solution, the running time and the memory usage

The PuzzleSolver Class has  a calculate total cost method, that is used to calculate the total estimated cost of a state


## Usage 
```
About:
		Given a 3×3 board with 8 tiles (every tile has one number from 1 to
		8)and one empty space. The objective is to place the numbers on tiles
		to match final configuration using the empty space. We can slide four
		adjacent (left, right, above and below) tiles into the empty space.

Usage:
		python3 puzzle.py -p <order> -a <algorithm> [options]

Options:
		-v		Verbose Mode.
```

## Sample Runs

### BFS
<img width="782" alt="bfs" src="https://user-images.githubusercontent.com/30150819/80987102-d8cbd480-8e31-11ea-9265-c9afee6edafb.png">

### DFS
<img width="782" alt="dfs" src="https://user-images.githubusercontent.com/30150819/80987170-f0a35880-8e31-11ea-9c91-bb5ccc77ce9c.png">

### A* - Manhattan
<img width="782" alt="astar-man" src="https://user-images.githubusercontent.com/30150819/80987257-16306200-8e32-11ea-8237-d537451cfcba.png">

### A* - Euclidean
<img width="782" alt="astar-euc" src="https://user-images.githubusercontent.com/30150819/80987336-3102d680-8e32-11ea-9099-ecc0133a241f.png">
