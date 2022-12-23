import time
from random import randrange
import pandas as pd

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
                    self.winner = 'Player1'
                    return True
                else:
                    self.winner = 'Player2'
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

class bot:
    def __init__(self, bot_variables):
        bot.bot_variables = bot_variables

    def randomGo(self, board):
        choices = board.checkChoices()
        choice = choices[randrange(len(choices))]
        return choice

    def AIGo(self, board, variables): #This is where the decision takes the input of the variables to make the right move
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

def runGeneration(generation, bots_per_gen, games_per_bot, scores_DF, top_n, variables_mean, generations, top_variables):
    #Bot variable generator
    if generation == 0:
        variables = [[[randrange(-100,100,1) for i in range(9)],[randrange(-100,100,1) for i in range(9)],[randrange(-100,100,1) for i in range(9)],[randrange(-100,100,1) for i in range(9)]] for j in range(bots_per_gen)]
    if generation >= 0: #bot variable generator based on previous generation
        #var = generations/(0.3*generation+1)
        var = 10
        variables = [[[0 for i in range(9)],[0 for i in range(9)],[0 for i in range(9)],[0 for i in range(9)]] for j in range(bots_per_gen)]
        for bot in range(bots_per_gen):
            for j in range(len(variables_mean)):
                variables[bot][j//9][j%9] = variables_mean[j] + (var * randrange(-100,100,1) * 0.01)
        variables[-1] = top_variables

    #Run games and collect scores
    for j in range(bots_per_gen):
        bot_score = 0
        for k in range(games_per_bot):
            outcome = gameCycle(variables[j])
            if outcome == 'Player2':
                bot_score +=1
            elif outcome == 'Player1':
                bot_score -=1
            elif outcome == 'Draw':
                bot_score +=0
        scores_DF = scores_DF.append({'generation': generation, 'bot': j, 'score': bot_score, 'variables': variables[j]}, ignore_index=True)

    sorted_scores = scores_DF.sort_values(by=['score'], ascending=False).head(top_n).reset_index()
    print(f"generation {generation}\n", sorted_scores)
    best_variables = sorted_scores['variables']
    gen_data = variable_data_mean(best_variables)
    top_variables = sorted_scores.head(1)
    top_variables = top_variables.iloc[0][4]
    return gen_data, best_variables, top_variables

def gameCycle(variables, whosTurn=False):

    game_running = True
    if whosTurn:
        is_player_go = True
    else:
        is_player_go = False
    current_board = game_board()
    compBot = bot(variables)

    while game_running == True:
        #current_board.display()
        game_won =  current_board.checkWinCondition()
        if game_won == True:
            winner = current_board.winner
            break
        current_board.choices = current_board.checkChoices()
        if not current_board.choices:
            winner = 'Draw'
            break
        if is_player_go == True:
            current_board.updateBoard(compBot.randomGo(current_board),is_player_go)
            is_player_go = False
        else:
            current_board.updateBoard(compBot.AIGo(current_board, variables),is_player_go)
            is_player_go = True

    if winner == 'Draw':
        #print("Draw")
        return "draw"
    else:
        #print(winner)
        return winner

def variable_data_mean(data):
    #Deconstruct df into an array
    array_ = []
    for row in range(len(data)):
        selected_row = data.iloc[row]
        list_ = []
        for item in range(len(selected_row)):
            for j in range(9):
                list_.append(selected_row[item][j])
        array_.append(list_)

    #Put array back into a df with values separated into 36 columns
    data_DF = pd.DataFrame(array_)

    #Calculate mean of each column
    mean = []
    for i in range(36):
        mean.append(data_DF[i].mean())
    return mean

def main():
    #Below are the simulation settings and setup
    bots_per_gen = 100
    games_per_bot = 100
    generations = 20
    top_n = 4
    scores_DF = pd.DataFrame(columns=['generation', 'bot', 'score', 'variables'])
    generation = 0

    #To start from random point
    #top_variables = [[randrange(-100,100,1) for i in range(9)] for j in range(4)]

    #Imports data from previous simulation for optimal starting point
    last_gen_data = [37.55170945279305, -98.3148521594261, -132.8919390869135, -96.69496082578407, -41.62159187905787, 222.77220150668867, -90.45681413976853, 20.736591299255124, -84.64888355237211, -198.9137093216921, -86.37151837823981, 93.27059933937583, 19.60721033217975, 31.908003350723025, -41.7984108767745, -6.33082834723411, 110.17894050630855, 60.64982528425844, -163.45569448210728, 98.58368755051092, 65.08074739000956, -105.28487036469747, -106.56248844146072, -68.7610126299707, 77.3801030965144, -137.3496411110769, -103.39020906436775, -7.79173998557955, 96.0480032253817, -106.94036343975925, 16.481483680635485, -203.98241657405242, 32.25857379720766, -130.64218702269534, 121.23674132422195, -22.68335726399495]
    top_variables = [[37.55170945279305, -98.3148521594261, -132.8919390869135, -96.69496082578407, -41.62159187905787, 222.77220150668867, -90.45681413976853, 20.736591299255124, -84.64888355237211], [-198.9137093216921, -86.37151837823981, 93.27059933937583, 19.60721033217975, 31.908003350723025, -41.7984108767745, -6.33082834723411, 110.17894050630855, 60.64982528425844], [-163.45569448210728, 98.58368755051092, 65.08074739000956, -105.28487036469747, -106.56248844146072, -68.7610126299707, 77.3801030965144, -137.3496411110769, -103.39020906436775], [-7.79173998557955, 96.0480032253817, -106.94036343975925, 16.481483680635485, -203.98241657405242, 32.25857379720766, -130.64218702269534, 121.23674132422195, -22.68335726399495]]
    for _ in range(generations):
        last_gen_data, best_variables, top_variables = runGeneration(generation, bots_per_gen, games_per_bot,scores_DF, top_n, last_gen_data, generations, top_variables)
        generation +=1

    best_variables.head(1)
    print(best_variables.iloc[0])


if __name__ == '__main__':
    start_time = time.time()
    main()
    print("Simulation time:", time.time() - start_time)
