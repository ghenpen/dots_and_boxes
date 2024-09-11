# Dots and Boxes Game
This is an implementation of the classic Dots and Boxes game using Python's tkinter for the graphical user interface. The game supports two modes: playing with another player or playing against a computer.

## Features
Two-player mode: Players take turns to form boxes by connecting dots.
AI mode: Play against the computer with basic AI to make moves.
Score tracking: Keeps track of the scores for both players.
Visual feedback: Each player has a unique color to differentiate their moves and shaded boxes.
## How to Play
The game is played on a 6x6 grid of dots:

Players take turns connecting two adjacent dots either horizontally or vertically.
If a player forms a complete box, that box is shaded in their color, and they get another turn.
The game ends when all possible boxes have been formed, and the player with the most boxes wins.
## Code Structure
### Main classes:

GameModeSelection: Handles the initial selection of game mode.
Dots_and_Boxes: Core class that implements the game logic for two players.
DotsAndBoxesWithComputer: Implements the same game logic but with AI capabilities for playing against the computer.
### Key methods:

play_with_player(): Starts the two-player game.
play_with_computer(): Starts the AI-based game.
mark_box(): Updates the board whenever a box is completed.
display_turn_text(): Displays the current player's turn.
is_gameover(): Checks if the game has ended.
## Requirements
Python 3.x
Tkinter (comes pre-installed with Python)
Numpy for handling matrix operations.
