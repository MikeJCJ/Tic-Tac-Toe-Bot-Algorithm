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
    choice = makeDecision(board)
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
    choices = []
    validChoice = False
    for i in range(3):
        for j in range(3):
            if board[i][j] != 'O' and board[i][j] != 'X':
                choices.append(board[i][j])
    while validChoice!= True:
        playerInput = input("Please type your move: ")
        if  isValid(playerInput) == True:
            if int(playerInput) in choices:
                return int(playerInput)

def checkWinCondition(board):
    global winner
    for i in range(3):
        for j in range(3):
            tile = [i,j]
            if board[i][j] == 'X':
                if lineCheck(tile, board, 'X') == True:
                    winner = 'Player'
                    return True
            elif board[i][j] == 'O':
                if lineCheck(tile, board, 'O') == True:
                    winner = 'Computer'
                    return True
    return False

def lineCheck(tile, board, value):
    row = tile[0]
    column = tile[1]
    if row == 0 and column == 0:
        if board[0][1] == value and board[0][2] == value:
            return True
        elif board[1][0] == value and board[2][0] == value:
            return True
        elif board[1][1] == value and board[2][2] == value:
            return True
        else:
            pass
    else:
        pass
    if row == 1 and column == 0:
        if board[1][1] == value and board[1][2] == value:
            return True
        else:
            pass
    else:
        pass
    if row == 2 and column == 0:
        if board[2][1] == value and board[2][2] == value:
            return True
        elif board[1][1] == value and board[0][2] == value:
            return True
        else:
            pass
    else:
        pass
    if row == 0 and column == 1:
        if board[1][1] == value and board[2][1] == value:
            return True
        else:
            pass
    else:
        pass
    if row == 0 and column == 2:
        if board[1][2] == value and board[2][2] == value:
            return True
        else:
            pass
    else:
        pass

def isValid(input):
    try:
        float(input)
        return True
    except ValueError:
        return False

def outOfChoices(board):
    choices = []
    for i in range(3):
        for j in range(3):
            if board[i][j] != 'O' and board[i][j] != 'X':
                choices.append(board[i][j])
    if not choices:
        return True
    else:
        return False

def makeDecision(board): #Function being tested
    victoryMatrix = [
        [[0,0],[0,1],[0,2]],
        [[1,0],[1,1],[1,2]],
        [[2,0],[2,1],[2,2]],
        [[0,0],[1,0],[2,0]],
        [[0,1],[1,1],[2,1]],
        [[0,2],[1,2],[2,2]],
        [[0,0],[1,1],[2,2]],
        [[0,2],[1,1],[2,0]]
    ]
    choices = checkChoices(board)
    choiceOutcomesX = {}
    choiceOutcomesO = {}

    if len(choices) == 1:
        choice = choices[0]
        return choice

    for choice in choices:
        victoriesBoolX = [True for i in range(8)]
        victoriesX = 0
        for i in range(len(victoryMatrix)):
            for j in range(len(victoryMatrix[i])):
                if board[victoryMatrix[i][j][0]][victoryMatrix[i][j][1]] == 'O':
                    victoriesBoolX[i] = False
        for i in victoriesBoolX:
            if i == True:
                victoriesX +=1
        choiceOutcomesX[choice] = victoriesX

        victoriesBoolO = [True for i in range(8)]
        victoriesO = 0
        for i in range(len(victoryMatrix)):
            for j in range(len(victoryMatrix[i])):
                if board[victoryMatrix[i][j][0]][victoryMatrix[i][j][1]] == 'X' \
                        or board[victoryMatrix[i][j][0]][victoryMatrix[i][j][1]] == choice:
                    victoriesBoolO[i] = False
        for i in victoriesBoolO:
            if i == True:
                victoriesO +=1
        choiceOutcomesO[choice] = victoriesO

    choiceTable = {}
    for i in choiceOutcomesX.keys():
        choiceTable[i] = (choiceOutcomesX[i]/(choiceOutcomesX[i]+choiceOutcomesO[i]))
    bestChoices = [key for key, value in choiceTable.items() if value == max(choiceTable.values())]
    choice = bestChoices[randrange(len(bestChoices))]

    if len(choices) >= 3 and len(bestChoices) > 1:
        betterChoiceOutcomesO = {}
        betterChoiceOutcomesX = {}
        for bestChoice in bestChoices:
            OChoices1 = choices[:]
            del OChoices1[OChoices1.index(bestChoice)]
            victoriesOO1 = 0
            victoriesXO1 = 0
            for OChoice1 in OChoices1:
                victoriesXX2 = 0
                victoriesOX2 = 0
                XChoices2 = OChoices1[:]
                del XChoices2[XChoices2.index(OChoice1)]
                for k in XChoices2:
                    victoriesBoolX2 = [True for i in range(8)]
                    for i in range(len(victoryMatrix)):
                        for j in range(len(victoryMatrix[i])):
                            if board[victoryMatrix[i][j][0]][victoryMatrix[i][j][1]] == 'O' \
                                    or board[victoryMatrix[i][j][0]][victoryMatrix[i][j][1]] == OChoice1:
                                victoriesBoolX2[i] = False
                    for i in victoriesBoolX2:
                        if i == True:
                            victoriesXX2 +=1

                    victoriesBoolO2 = [True for i in range(8)]
                    for i in range(len(victoryMatrix)):
                        for j in range(len(victoryMatrix[i])):
                            if board[victoryMatrix[i][j][0]][victoryMatrix[i][j][1]] == 'X' \
                                    or board[victoryMatrix[i][j][0]][victoryMatrix[i][j][1]] == k \
                                    or board[victoryMatrix[i][j][0]][victoryMatrix[i][j][1]] == bestChoice:
                                victoriesBoolO2[i] = False
                    for i in victoriesBoolO2:
                        if i == True:
                            victoriesOX2 +=1
                victoriesOO1 += victoriesOX2
                victoriesXO1 += victoriesXX2
            betterChoiceOutcomesX[bestChoice] = victoriesXO1
            betterChoiceOutcomesO[bestChoice] = victoriesOO1
        betterChoiceTable = {}
        for i in betterChoiceOutcomesX.keys():
            betterChoiceTable[i] = (betterChoiceOutcomesX[i]/(betterChoiceOutcomesX[i]+betterChoiceOutcomesO[i]))
            bestestChoices = [key for key, value in betterChoiceTable.items() if value == max(betterChoiceTable.values())]
            bestestChoice = bestestChoices[randrange(len(bestestChoices))]

        return bestestChoice

    return choice

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
        winCondition = checkWinCondition(boardData)
        if winCondition == True:
            print('Game is finished!')
            drawBoard(boardData)
            print(f"{winner} has won")
            break
        else:
            pass
        if outOfChoices(boardData) == True:
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