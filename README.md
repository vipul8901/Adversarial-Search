# Adversarial-Search

In this project we are creating an agent to intelligently play the **2048-puzzle game**, using more advanced techniques to probe the search space than the simple methods used in the previous assignment. 

Try playing the game here: [gabrielecirulli.github.io/2048](https://gabrielecirulli.github.io/2048) to get a sense of how the game works. 
The project implements an adversarial search algorithm that plays the game intelligently.

![2048.png](img/2048.png)

## Code structure
The skeleton code includes the following files. Note that from the '.py' files, only PlayerAI.py file has been written by author; the rest of the files were provided as part of the assignment and could not be modified. The exception was the time.clock() vs time.process_time() as the former had been deprecated in current version of Python. 

### Read-only: GameManager.py. 
This is the driver program that loads your Computer AI and Player AI, and begins a game where they compete with each other. See below on how to execute this program.

### Read-only: Grid.py. 
This module defines the Grid object, along with some useful operations: move(), getAvailableCells(), insertTile(), and clone(), which you may use in your code. These are available to get you started, but they are by no means the most efficient methods available. If you wish to strive for better performance, feel free to ignore these and write your own helper methods in a separate file.

### Read-only: BaseAI.py. 
This is the base class for any AI component. All AIs inherit from this module, and implement the getMove() function, which takes a Grid object as parameter and returns a move (there are different "moves" for different AIs).


### Read-only: ComputerAI.py. 
This inherits from BaseAI. The getMove() function returns a computer action that is a tuple (x, y) indicating the place you want to place a tile.


### Writable: PlayerAI.py. 
This is where the coding work for this assignment has taken place. This file inherits from BaseAI. The getMove() function returns a number that indicates the player’s action. In particular: 
- 0 stands for "Up", 
- 1 stands for "Down", 
- 2 stands for "Left", and 
- 3 stands for "Right". 


### Read-only: BaseDisplayer.py and Displayer.py. 
These print the grid.

### Execute the GameManager as follows:

$ python3 GameManager.py

The progress of the game will be displayed on your terminal screen, with one snapshot printed after each move that the Computer AI or Player AI makes. Note that the Player AI is allowed 0.2 seconds to come up with each move. The process continues until the game is over; that is, until no further legal moves can be made. At the end of the game, the maximum tile value on the board is printed.

