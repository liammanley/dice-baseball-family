## Dice Baseball Family Game
The purpose of this program is to simulate a 162 game season between four teams. Each of the four teams was drafted by one of my family members, and is composed of 1985 Major League Baseball players.

At the core of this program is
1. A player class, which calculates a players' probabilities of possible outcomes (home run, double, out, etc)
2. A function, sim_game(). This function simulates a baseball game between two teams, which are passed to the function as an argument. The winner is returned.

The rest of the program is composed of creating the players, adding them to the teams, calling sim_game() many times, and displaying the standings at the end. The player class and sim_game() function can easily be reused for other programs that involve simulating baseball games even if the rest of the program may need modification.

