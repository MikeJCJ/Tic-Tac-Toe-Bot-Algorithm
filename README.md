# Tic-Tac-Toe Bot Algorithm

This python script creates an interactive Tic Tac Toe game within the IDE, with a computer opponent that uses an algorithm (or machine learning) to choose the best move. The bots success is determined by playing it against a bot which chooses randomly for 10,000 games.

The there are 4 levels of bot algorithm:

         *Level 1: Bot simply chooses randomly. results in a win rate of 29% (Due to the natural bias of the game, note it is assumed with the win rates   mentioned that the Bot in question plays second).
         
         *Level 2: Bot Assesses each possible move, and chooses the move which results in maximising a success criterion. Results in a win rate of 72%.
         
                  *(criterion=possibleVictoriesForBot/TotalVictoriesBothPlayers)
                  
                  *In the case of multiple "best choices", a choice is picked randomly.
                  
         *Level 3: In addition to the first step in Level 2, if there are multiple "best choices", the bot looks two steps ahead, and chooses the outcome which maximises the success criterion in two moves time. Results in a win rate of 86%.
         
         *Level 4: This bot consists of a neural network with 9 input nodes and 9 output nodes, representing the 9 tiles on the board. The weights for each node is calculated in the TicBotMachineLearning file, and are copied into the bot 4 code



By running the script, you can select whether you would like to play the AI, or have them play eachother for 10,000 games, returning the wins from each AI.
