# backgammon
A popular luck and strategy game, which is made as a project of DATA STUCTURE and algorithm

Concept of Development

Programming language (Used in development): Python 3

Basic Algorithm of game (step by step):
1. By default, on the start of game, human has first turn
2. If turn == player => Dice roll button appear
2.1. On pressing the dice button, dice rolls and stuck when leave pressing
3. Else => dice rolls automatically
4. Saving dice values in txt file
5. If all pieces has been reached in home => allow to bear off
6. Highlighting the piece that can be moved
7. If turn == player:
7.1. On clicking, one of the highlighted pieces, highlighting the possible
destinations (each piece has maximum 2 possible destinations say a & b)
7.2. Press M to move that piece to go to a, press SPACE to move to b.
8. Else = > Piece move automatically using AI algorithm.
9. If new destination has one piece of opponent => move to middle stack
10.If both dice values has been used to moved
10.1. Change the turn
10.2. Repeat step 1 to step 9 for opponent
11.If human has beard off all pieces first => winning message shows
12.If cpu has beard off all pieces first => losing message shows

DATA STRUCTURES (Used in development)

Stack:

“A stack is a linear data structure that stores items in a Last-In/First-Out
(LIFO). In stack, a new element is added at one end and an element is
removed from that end only. The insert and delete operations are called
push and pop.”
Implementation in Project:
Stacks are the most important, most used and are the basis of the game. This
whole game follows the style of stack. All the 24 columns have been
implemented through stack following LIFO protocol. Movements of pieces are
validated through stacks. There’s a rule that after getting our piece hit by the
opponent, our piece would start again from the initial position. This has been
implemented though stack. Also, a piece cannot beat opponent’s piece at the
opening turn, our stack also assures this.

Python Lists:

“A collection which is ordered and changeable. Allows duplicate members.
In Python lists are written with square brackets.”
Implementation in Project:
In project, they are used for various purposes
1-After rolling the dice, all possible movable pieces would be stored in a separate list.
They are used so to highlight the movable pieces.
2-All the legal destinations (the stack column’s places where pieces can be moved to)
would be stored separately in a list.
3-All the bared off pieces would also be stored in a separate list to assure that these
pieces are now in home.

Dictionary:

A dictionary is a collection which is unordered, changeable and indexed. In Python
dictionaries are written with curly brackets, and they have keys and values.
Implementation in Project:
All of the 24 objects of the stack class are kept in a dictionary with corresponding
values as their key.
e.g {1:obj1 of stack}
This would also provide the functionality to access the needed stack through its
location (i.e key).

LIBRARIES USED

1-Pygame:
The pygame library is an open-source module for the Python programming
language specifically intended to help you make games and other multimedia
applications.

2-Random:
To generate random numbers.

3-OS:
To launch our game always on top of the screen
The OS module in Python provides a way of using operating system dependent
functionality. The functions that the OS module provides allows you to interface with the
underlying operating system that Python is running on.

4-Time:
Python time sleep. Python time sleep function is used to add delay in the execution of a
program. We can use python sleep function to halt the execution of the program for
given time in seconds. Notice that python time sleep

DEVELOPED BY SYED MAAZ HASSAN
