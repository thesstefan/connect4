# Connect 4
Implementation of the [Connect Four](https://en.wikipedia.org/wiki/Connect_Four)
game using Python. The game is highly extensible through the YAML configuration file
and the program's versatile architecture. 

# Extensibility
The game can have any number of human and AI players and can be played on
any board shape. Even more, the user can choose between a text UI or the
GUI created using `pygame` or can choose the algorithm used by the AI players.
All this can be configured through the YAML configuration file. A sample is
provided at [`config.yaml`](https://github.com/thesstefan/connect4/blob/master/config.yaml).

Currently, the AI can make choices randomly or by using a minimax algorithm
enhanced by the [alpha-beta pruning](https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning)
technique.

New user interfaces and AI engines can easily be integrated in the existing program.

# Installation and Usage
The game requires pygame and Python3 to be installed. pygame can be installed through pip:
```bash
pip install pygame
```

After the requirements are satisfied, clone the project
```bash
git clone git@github.com:thesstefan/connect4.git
```
and run the provided ['start.py'](https://github.com/thesstefan/connect4/blob/master/start.py) script
through your preferred IDE or in a terminal.

# Demo
A game round example (Player vs AI, standard Connect 4 rules) is shown below:
<p align="center">
  <img src="https://github.com/thesstefan/connect4/blob/master/readme/demo.gif" alt="Game Demo GIF"/>
</p>
