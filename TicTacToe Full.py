import time
from random import randrange

class game_board:
    victory_matrix = [
        ['a','b','c'],
        ['d','e','f'],
        ['g','h','i'],
        ['a','d','g'],
        ['b','e','h'],
        ['c','f','i'],
        ['a','e','i'],
        ['g','e','c']
    ]
    winner = ''

    def __init__(self):
        self.board = {'a':1,'b':2,'c':3,'d':4,'e':5,'f':6,'g':7,'h':8,'i':9}
        self.choices = self.checkChoices()

    def display(self):
        print("+ - + - + - +")
        print("| ",self.board['a']," | ",self.board['b']," | ",self.board['c']," |", sep="")
        print("+ - + - + - +")
        print("| ",self.board['d']," | ",self.board['e']," | ",self.board['f']," |", sep="")
        print("+ - + - + - +")
        print("| ",self.board['g']," | ",self.board['h']," | ",self.board['i']," |", sep="")
        print("+ - + - + - +")

    def updateBoard(self, turn, is_player_go):
        for i in self.board.keys():
            if self.board[i] == turn:
                if is_player_go == True:
                    self.board[i] = 'X'
                else:
                    self.board[i] = 'O'

    def checkWinCondition(self):
        global winner
        for i in range(len(self.victory_matrix)):
            if self.board[self.victory_matrix[i][0]] == self.board[self.victory_matrix[i][1]] == self.board[self.victory_matrix[i][2]]:
                if self.board[self.victory_matrix[i][0]] == 'X':
                    self.winner = 'Player'
                    return True
                else:
                    self.winner = 'Computer'
                    return True
        else:
            return False

    def checkChoices(self):
        self.choices = []
        for i in self.board:
            if self.board[i] != 'X' and self.board[i] !='O':
                self.choices.append(self.board[i])
        return self.choices

    def checkPossVictories(self, opp_player):
        poss_victories = 0
        for i in range(len(self.victory_matrix)):
            if self.board[self.victory_matrix[i][0]] != opp_player and self.board[self.victory_matrix[i][1]] != opp_player and self.board[self.victory_matrix[i][2]] != opp_player:
                poss_victories += 1
        return poss_victories

class bot: #Can use for opponent but also when predicting opponents best move
    def __init__(self, difficulty):
        self.difficulty = difficulty

    def computerGo(self, board, player):
        if self.difficulty == '1':
            choice = self.bot1(board)
        elif self.difficulty == '2':
            choice = self.bot2(board, player)
        elif self.difficulty == '3':
            choice = self.bot3(board, player)
        elif self.difficulty == '4':
            choice = self.bot4(board)
        return choice

    def bot1(self,board):
        choices = board.checkChoices()
        choice = choices[randrange(len(choices))]
        return choice

    def bot2(self, board, player): #Initialised when bots turn, and also initialised with a different board
        choices = board.checkChoices()
        virtual_board1 = game_board()
        virtual_board1.board = dict(board.board)
        if player == 'X':
            is_player_go = True #This value is used by the updateBoard function, so this is assigned so a virtual board can be updated.
        else:
            is_player_go = False
        choice_strength = {}
        for i in choices:
            virtual_board1.updateBoard(i, is_player_go)
            x_poss_victories = virtual_board1.checkPossVictories('O')
            o_poss_victories = virtual_board1.checkPossVictories('X')
            if player == 'X':
                choice_strength[i] = x_poss_victories - o_poss_victories
            if player == 'O':
                choice_strength[i] = o_poss_victories - x_poss_victories
            virtual_board1.board = dict(board.board)
        highest_win_chance = None
        highest_tiles = []
        for key, value in choice_strength.items():
            if highest_win_chance == None or value > highest_win_chance:
                highest_win_chance = value
                highest_tiles = [key]
            elif value == highest_win_chance:
                highest_tiles.append(key)
        choice = highest_tiles[randrange(len(highest_tiles))]
        return choice

    def bot3(self, board, player):
        choices = board.checkChoices()
        virtual_board1 = game_board()
        virtual_board1.board = dict(board.board)
        if player == 'X':
            is_player_go = True #This value is used by the updateBoard function, so this is assigned so a virtual board can be updated.
        else:
            is_player_go = False

        choice_strength = {}
        for i in choices:
            virtual_board1.updateBoard(i, is_player_go)
            x_poss_victories = virtual_board1.checkPossVictories('O')
            o_poss_victories = virtual_board1.checkPossVictories('X')
            if player == 'X':
                choice_strength[i] = x_poss_victories - o_poss_victories
            if player == 'O':
                choice_strength[i] = o_poss_victories - x_poss_victories
            virtual_board1.board = dict(board.board)

        highest_win_chance = None
        highest_tiles = []
        for key, value in choice_strength.items():
            if highest_win_chance == None or value > highest_win_chance:
                highest_win_chance = value
                highest_tiles = [key]
            elif value == highest_win_chance:
                highest_tiles.append(key)

        if len(choice_strength) < 3 or len(highest_tiles) == 1:
            #print(f"Level 1 prediction, {highest_tiles}")
            choice = highest_tiles[randrange(len(highest_tiles))]
        else:
            choice_strength = {}
            for i in highest_tiles:
                virtual_board1.updateBoard(i, is_player_go)
                virtual_bot = bot(3)
                virtual_board1.updateBoard(virtual_bot.bot3(virtual_board1,'O'), is_player_go)
                x_poss_victories = virtual_board1.checkPossVictories('O')
                o_poss_victories = virtual_board1.checkPossVictories('X')
                if player == 'X':
                    choice_strength[i] = x_poss_victories - o_poss_victories
                if player == 'O':
                    choice_strength[i] = o_poss_victories - x_poss_victories
                virtual_board1.board = dict(board.board)

            highest_win_chance = None
            highest_tiles = []
            for key, value in choice_strength.items():
                if highest_win_chance == None or value > highest_win_chance:
                    highest_win_chance = value
                    highest_tiles = [key]
                elif value == highest_win_chance:
                    highest_tiles.append(key)
            #print(f"Level 2 prediction, {highest_tiles}")
            choice = highest_tiles[randrange(len(highest_tiles))]

        return choice

    def bot4(self, board):
        variables = [[2.166132648135669, -142.22918456849848, 28.802324702809166, -34.3591840976318, -23.83157279835686, 14.39072082337364, -52.395208135884374, -6.7683684970540625, -59.237616265372765], [-68.13084219769237, -51.757688938580515, 55.719251120947156, 4.639918804106063, -44.93581383527906, 21.16244770943952, -49.71911427114905, 34.62180883384773, -35.494084501215255], [-50.713408338613455, -11.957205487145297, 6.067003448307169, -91.81632835536917, -56.11678840311578, 28.982863674019946, 49.96543915222467, -107.1169153011864, 26.148348825788872], [74.58076876370274, 92.53229977265394, 11.292808426653258, 1.036661862896155, -121.92123444614899, -61.03363641167156, 21.616291599624564, 187.71571835547334, 127.30531500830912]]
        choices_num = board.checkChoices()
        choices_let = []
        board_tiles = {'a':1,'b':2,'c':3,'d':4,'e':5,'f':6,'g':7,'h':8,'i':9}
        for key in board_tiles:
            if board_tiles[key] in choices_num:
                choices_let.append(key)

        #Calculate the choice strength of each tile
        choice_strength = {}
        #print(variables)
        m = 0
        for tile in board_tiles:
            metrics = [0 for i in range(9)]
            for key, val in board_tiles.items():
                if board.board[key] == 'X':
                    #print("X is here")
                    metrics[val-1] = variables[0][val-1] * 1 * variables[3][m]
                if board.board[key] == 'O':
                    metrics[val-1] = variables[1][val-1] * -1 * variables[3][m]
                    #print("O is here")
                else:
                    metrics[val-1] = variables[2][val-1] * variables[3][m]
            m+=1
            #print(metrics)
            strength = sum(metrics)
            choice_strength[tile] = strength
        for key in choice_strength:
            if board.board[key] == 'X' or board.board[key] == 'O':
                choice_strength[key] = None
        #print("\n", choice_strength)

        #Calculate the tile with the highest win chance and choose a tile
        highest_win_chance = None
        highest_tiles = []
        for key, value in choice_strength.items():
            if value == None:
                continue
            if highest_win_chance == None or value > highest_win_chance:
                highest_win_chance = value
                highest_tiles = [key]
            elif value == highest_win_chance:
                highest_tiles.append(key)
        choice_let = highest_tiles[randrange(len(highest_tiles))]
        choice_num = board_tiles[choice_let]
        return choice_num

def playerGo(board):
    choices = board.checkChoices()
    print(choices)
    valid_choice = False
    player_turn = input("Please enter a tile: ")
    while valid_choice == False:
        if validInput(player_turn) == True:
            if int(player_turn) in choices:
                return int(player_turn)
            else:
                player_turn = input("Please enter a valid tile: ")
        else:
            player_turn = input("Please enter a valid tile: ")

def validInput(player_turn):
    try:
        int(player_turn)
        return True
    except ValueError:
        return False

def userDecision(decision_type, text=''):
    if decision_type == 1: #Game Type
        decision = input("Choose the simulation type, [1] for active game, [2] to run 10000 simulations: ")
        if decision == "1" or decision == "2":
            return decision
        else:
            print("\nPlease choose a valid input")
            userDecision()
    elif decision_type == 2: #Difficulty
        decision = input(f"Choose bot{text} difficulty, [1], [2], [3], [4]: ")
        if decision == "1" or decision == "2" or decision == "3" or decision == "4":
            return decision
        else:
            print("\nPlease choose a valid input")
            userDecision()
    elif decision_type == 3: #Who starts
        decision = input("Who starts first, Player 1 [1] or Player 2 [2]? ")
        if decision == "1":
            return True
        elif decision == "2":
            return False
        else:
            print("\nPlease choose a valid input")
            userDecision()

def gameCycle(opp1, opp2, whosTurn=True):

    game_running = True
    if whosTurn:
        is_player_go = True
    else:
        is_player_go = False
    current_board = game_board()

    if opp1 != "player":
        bot1 = bot(opp1)
    bot2 = bot(opp2)

    while game_running == True:
        game_won =  current_board.checkWinCondition()
        if game_won == True:
            winner = current_board.winner
            break
        current_board.choices = current_board.checkChoices()
        if opp1 == "player":
            current_board.display()
        if not current_board.choices:
            winner = 'Draw'
            break
        if is_player_go == True:
            if opp1 == "player":
                current_board.updateBoard(playerGo(current_board),is_player_go)
            else:
                current_board.updateBoard(bot1.computerGo(current_board,'X'),is_player_go)
            is_player_go = False
        else:
            current_board.updateBoard(bot2.computerGo(current_board,'O'),is_player_go)
            is_player_go = True

    if winner == 'Draw':
        if opp1 == "player":
            print("The game was a draw.")
        return "draw"
    else:
        if opp1 == "player":
            print(f"\nThe game was won by {winner}.\n")
        return winner

def main():
    game_type = userDecision(1)
    whosTurn = userDecision(3)
    if game_type == "2":
        opp1  = userDecision(2," 1")
        opp2 = userDecision(2," 2")
        opp1_wins = 0
        opp2_wins = 0
        draws = 0
        for _ in range(10_000):
            outcome = gameCycle(opp1, opp2, whosTurn)
            if outcome == "Player":
                opp1_wins +=1
            elif outcome == "Computer":
                opp2_wins +=1
            elif outcome == "draw":
                draws +=1
        print(f"From the simulations, bot 1 won {opp1_wins} times, bot 2 won {opp2_wins}, and there were {draws} draws.")
    elif game_type == "1":
        opp1 = "player"
        opp2 = userDecision(2)
        gameCycle(opp1, opp2, whosTurn)

if __name__ == '__main__':
    start_time = time.time()
    main()
    print("Game time:", time.time() - start_time)
