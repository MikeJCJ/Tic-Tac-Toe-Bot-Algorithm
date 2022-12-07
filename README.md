# Tic-Tac-Toe Bot Algorithm

This python script creates an interactive Tic Tac Toe game within the IDE, with a computer opponent that uses an algorithm to choose the best move.

The bots success is determined by playing it against a bot which chooses randomly (the algorithm is assigned to Player 2) for 10,000 games.

The there are 3 levels of bot algorithm:

         *Level 1: Bot simply chooses randomly. results in a win rate of 29% (Due to the natural bias of the game).
         
         *Level 2: Bot Assesses each possible move, and chooses the move which results in maximising a success criterion. Results in a win rate of 72%.
         
                  *(criterion=possibleVictoriesForBot/TotalVictoriesBothPlayers)
                  
                  *In the case of multiple "best choices", a choice is picked randomly.
                  
         *Level 3: In addition to the first step in Level 2, if there are multiple "best choices", the bot looks two steps ahead, and chooses the outcome which maximises the success criterion in two moves time. Results in a win rate of 86%.



Future work:

        [ ] Cleanup the code with the use of classes in order for it to be more readable, and expandable.
        [ ] Create a Level 4 bot. The optimal bot should win or draw 100% of the time.
        [ ] Allow the user to choose the level of bot to play.
