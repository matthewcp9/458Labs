import random
import copy

global bestMove
def redraw(board):
    for row in board:
        print(row[0], row[1], row[2])

def checkWin(bo):
    #row wins
    if (bo[0][0] == bo[0][1] and bo[0][1] == bo[0][2] and bo[0][0] != ' '):
        return 10 if bo[0][0] == 'X' else -10
    if bo[1][0] == bo[1][1] and bo[1][0] == bo[1][2] and bo[1][0] != ' ':
        return 10 if bo[1][0] == 'X' else -10
    if bo[2][0] == bo[2][1] and bo[2][0] == bo[2][2] and bo[2][0] != ' ':
        return 10 if bo[2][0] == 'X' else -10

    #column wins
    if bo[0][0] == bo[1][0] and bo[1][0] == bo[2][0] and bo[0][0] != ' ':        
        return 10 if bo[0][0] == 'X' else -10
    if bo[0][1] == bo[1][1] and bo[1][1] == bo[2][1] and bo[0][1] != ' ': 
        return 10 if bo[0][1] == 'X' else -10
    if bo[0][2] == bo[1][2] and bo[1][2] == bo[2][2] and bo[0][2] != ' ':
        return 10 if bo[0][2] == 'X' else -10

    #diagonal wins
    if bo[0][0] == bo[1][1] and bo[1][1] == bo[2][2] and bo[0][0] != ' ':
        return 10 if bo[0][0] == 'X' else -10
    if bo[0][2] == bo[1][1] and bo[1][1] == bo[2][0] and bo[0][2] != ' ':      
        return 10 if bo[0][2] == 'X' else -10
    return 0

def TicTacToe():
    board = []
    board.append([' '] * 3)
    board.append([' '] * 3)
    board.append([' '] * 3)
    depth = 9
    randX = random.randint(0, 8)
    leftover = list(range(0, randX)) + list(range(randX + 1, 9))
    randO = random.choice(leftover)
    #print(randX, randO)
    #board[randX//3][randX % 3] = 'X'
    #board[randO//3][randO % 3] = 'O'

    while depth > 0 and checkWin(board) == 0:
        num = int(input("Next move: "))
        if (num in range(0, 9) and board[num//3][num % 3] == ' '): 
            board[num//3][num % 3] = 'X'
            if (checkWin(board)):
                redraw(board)
                break;
            depth -= 1
            temp_board = copy.deepcopy(board)
            bestMove = minvalue(temp_board, 0, float("-inf"), float("inf"))
            board[bestMove//3][bestMove % 3] = 'O'
            redraw(board)
            depth -= 1   
            
        else :
            print("Invalid Move.")

    print("You win") if checkWin(board) == 10 else print("Tied") if checkWin(board) == 0 else print("You Lose")
        

def maxvalue(board, depth, alpha, beta):
    moves = generatePossibleMoves(board)
    scores = []
    v = float("-inf")
    if len(moves) == 0 or checkWin(board) != 0:
        return checkWin(board)
    for move in moves:
        temp_board = copy.deepcopy(board)
        temp_board[move//3][move%3] = 'X'
        v = max(v, minvalue(temp_board, depth + 1, -1, -1))
        if v >= beta:
            return v
        alpha = max(alpha, v)
    return v

def minvalue(board, depth, alpha, beta):
    moves = generatePossibleMoves(board)
    v = float("inf")
    best = [-1, v]
    if len(moves) == 0 or checkWin(board) != 0:
        return checkWin(board)
    for move in moves:
        temp_board = copy.deepcopy(board)
        temp_board[move//3][move%3] = 'O'
        temp = v
        v = min(v, maxvalue(temp_board, depth + 1, -1, -1))
        if temp != v:
            best[0] = move
            best[1] = v
        if v <= alpha:
            return v
        beta = min(beta, v)
    if depth == 0:
        return best[0]
    else:
        return best[1]
    
    
def generatePossibleMoves(board):
    moves = []
    for x in range(0, 9):
        if board[x//3][x % 3] == ' ':
            moves.append(x)
    return moves
    

TicTacToe()
