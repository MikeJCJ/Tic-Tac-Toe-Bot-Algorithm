import time
from random import randrange

def drawBoard(board):
    print("+ - + - + - +")
    print("| ",board[0][0]," | ",board[0][1]," | ",board[0][2]," |", sep="")
    print("+ - + - + - +")
    print("| ",board[1][0]," | ",board[1][1]," | ",board[1][2]," |", sep="")
    print("+ - + - + - +")
    print("| ",board[2][0]," | ",board[2][1]," | ",board[2][2]," |", sep="")
    print("+ - + - + - +")

def computerGo(board):
    choices = checkChoices(board)
    choice = choices[randrange(len(choices))]
    return choice

def updateBoardData(choice,turn,board):
    row = (choice-1)//3
    column = (choice-1)%3
    if turn == 'Player':
        board[row][column] = 'X'
    else:
        board[row][column] = 'O'
    return board

def playerGo(board):
    choices = checkChoices(board)
    validChoice = False
    while validChoice!= True:
        playerInput = input("Please type your move: ")
        if  isValid(playerInput) == True:
            if int(playerInput) in choices:
                return int(playerInput)

def checkWinCondition(board):
    global winner
    for i in range(3):
        for j in range(3):
            if board[i][j] == 'X':
                if lineCheck(board, 'X') == True:
                    winner = 'Player'
                    return True
            elif board[i][j] == 'O':
                if lineCheck(board, 'O') == True:
                    winner = 'Computer'
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

def isValid(input):
    try:
        float(input)
        return True
    except ValueError:
        return False

def checkChoices(board):
    choices = []
    for i in range(3):
        for j in range(3):
            if board[i][j] != 'O' and board[i][j] != 'X':
                choices.append(board[i][j])
    return choices

def main():
    gameIsGoing = True
    isUserGo = False
    boardData = [[(3*i)-2, (3*i)-1, (3*i)] for i in range(1,4)]

    while gameIsGoing:
        if checkWinCondition(boardData) == True:
            print('Game is finished!')
            drawBoard(boardData)
            print(f"{winner} has won")
            break
        else:
            pass
        if not checkChoices(boardData) == True:
            drawBoard(boardData)
            print("Game has ended. There is no winner")
            break
        if isUserGo == True:
            drawBoard(boardData)
        if isUserGo == True:
            boardData = updateBoardData(playerGo(boardData),'Player', boardData)
            isUserGo = False
        else:
            boardData = updateBoardData(computerGo(boardData),'Computer', boardData)
            isUserGo = True

if __name__ == '__main__':
    start_time = time.time()
    main()
    print("Game won in", round(time.time() - start_time,2), "seconds")
