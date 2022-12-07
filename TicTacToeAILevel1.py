import time
from random import randrange

def player1Go(board):
    choices = checkChoices(board)
    choice = choices[randrange(len(choices))]
    return choice

def player2Go(board):
    choices = checkChoices(board)
    choice = choices[randrange(len(choices))]
    return choice

def updateBoardData(choice,turn,board):
    row = (choice-1)//3
    column = (choice-1)%3
    if turn == 'Player 1':
        board[row][column] = 'X'
    else:
        board[row][column] = 'O'
    return board

def checkWinCondition(board):
    global winner
    for i in range(3):
        for j in range(3):
            if board[i][j] == 'X':
                if lineCheck(board, 'X') == True:
                    winner = 'Player 1'
                    return True
            elif board[i][j] == 'O':
                if lineCheck(board, 'O') == True:
                    winner = 'Player 2'
                    return True
    return False

def lineCheck(board, value):
    if board[0][0] == value and board[0][1] == value and board[0][2] == value\
    or board[1][0] == value and board[1][1] == value and board[1][2] == value\
    or board[2][0] == value and board[2][1] == value and board[2][2] == value\
    or board[0][0] == value and board[1][0] == value and board[2][0] == value\
    or board[0][1] == value and board[1][1] == value and board[2][1] == value\
    or board[0][2] == value and board[1][2] == value and board[2][2] == value\
    or board[0][0] == value and board[1][1] == value and board[2][2] == value\
    or board[2][0] == value and board[1][1] == value and board[0][2] == value:
        return True

def checkChoices(board):
    choices = []
    for i in range(3):
        for j in range(3):
            if board[i][j] != 'O' and board[i][j] != 'X':
                choices.append(board[i][j])
    return choices

def gameRun():
    gameIsGoing = True
    isPlayer1Go = True
    boardData = [[(3*i)-2, (3*i)-1, (3*i)] for i in range(1,4)]

    while gameIsGoing:
        if checkWinCondition(boardData) == True:
            return winner
        else:
            pass
        if not checkChoices(boardData):
            return 'draw'
        if isPlayer1Go == True:
            boardData = updateBoardData(player1Go(boardData),'Player 1', boardData)
            isPlayer1Go = False
        else:
            boardData = updateBoardData(player2Go(boardData),'Player 2', boardData)
            isPlayer1Go = True

def checkChoices(board):
    choices = []
    for i in range(3):
        for j in range(3):
            if board[i][j] != 'O' and board[i][j] != 'X':
                choices.append(board[i][j])
    return choices

def main():
    player1wins = 0
    player2wins = 0
    draws = 0
    for i in range(10000):
        winner = gameRun()
        if winner == 'Player 1':
            player1wins +=1
        elif winner == 'Player 2':
            player2wins +=1
        elif winner == 'draw':
            draws +=1
    print(f"In 10000 games, Player 1 won {player1wins}, Player 2 won {player2wins}, and there were {draws} draws")

if __name__ == '__main__':
    start_time = time.time()
    main()
    print("Games finished in", round(time.time() - start_time,2), "seconds")