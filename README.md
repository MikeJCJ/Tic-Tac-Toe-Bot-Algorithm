# Tic-Tac-Toe Bot Algorithm

This python script creates an interactive Tic Tac Toe game within the IDE, with a computer opponent that uses an algorithm to choose the optimal move.

The bots success is determined by playing it against a bot which chooses randomly (the algorithm is assigned to Player 2) for 10,000 games.

The there are 3 levels of bot algorithm:
         *Level 1: Bot simply chooses randomly. results in a win rate of 29% (Due to the natural bias of the game).
         *Level 2: Bot Assesses each possible move, and chooses the move which results in maximising a success criterion
                  *(criterion=possibleVictoriesForBot/TotalVictoriesBothPlayers)
                  *In the case of multiple "best choices", a choice is picked randomly.
         *Level 3: In addition to the first step in Level 2, if there are multiple "best choices", the bot looks two steps ahead, and chooses the outcome which maximises the success criterion in two moves time.
