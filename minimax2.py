# minimax2.py is a minimax file specifically for connect 4
# 1/17/18
__author__ = 'Christos Polzak'

from connect4 import *
import copy, random

def getOpen(board, turn): # gets available play options
    spaces = []
    for k in [3,4,2,5,1,6,0]:
        tup = isOpen(board,k)
        if tup[0]:
            spaces.append((k,tup[1]))
    return spaces

def heuristic(board): # evaluates the state of a passed in board based on the number of 2-stacks and 3-stacks of each player
    t1threes = []
    t2threes = []
    t1twos = []
    t2twos = []
    for a in range(7):
        for b in range(0,5):
            if board[a][-b] != 0:
                if board[a][-b+1] == 0 and board[a][-b] == board[a][-b-1]:
                    if b < 5 and board[a][-b-2] == board[a][-b]:
                        t1threes.append((a,7-b)) if board[a][-b] == 1 else t2threes.append((a,7-b))
                    else:
                        t1twos.append((a,7-b)) if board[a][-b] == 1 else t2twos.append((a,7-b))
    slices = []
    for c in range(6):
        null1 = []
        for d in range(7):
            null1.append((board[d][c],(d,c)))
        slices.append(null1)
    for e in range(3):
        null2 = []
        null3 = []
        null4 = []
        null5 = []
        for f in range(4+e):
            null2.append((board[3-e+f][5-f],(3-e+f,5-f)))
            null3.append((board[3+e-f][5-f],(3+e-f,5-f)))
            null4.append((board[f][3+e-f],(f,3+3-f)))
            null5.append((board[6-f][3+e-f],(6-f,3+e-f)))
        slices.append(null2)
        slices.append(null3)
        slices.append(null4)
        slices.append(null5)
    for slice in slices:
        g = 0
        while g < len(slice) - 3:
            null6 = [0,0,0]
            zero = None
            for h in range(4):
                null6[slice[g+h][0]] += 1
                if slice[g+h][0] == 0:
                    zero = slice[g+h][1], h
            if null6 == [1,3,0]:
                g += zero[1]
                if not (zero[0] in t1threes):
                    t1threes.append(zero[0])
            if null6 == [1,0,3]:
                g += zero[1]
                if not (zero[0] in t2threes):
                    t2threes.append(zero[0])
            if null6 == [2,2,0]:
                g += zero[1]
                if not (zero[0] in t1twos):
                    t1twos.append(zero[0])
            if null6 == [2,0,2]:
                g += zero[1]
                if not (zero[0] in t2twos):
                    t2twos.append(zero[0])
            g += 1
    return (len(t1threes) - len(t2threes)) * 100 + (len(t1twos) - len(t2twos)) * 10


def minimax(board, depth, turn, spc, LOW, HIGH, rd): # minimax. determines computer move.
    myScores = []
    alpha = LOW
    beta = HIGH
    if endcheck(board, spc[0], spc[1])[0]:
        return ((turn * -9) + (depth * turn)) * 1000
    if depth > (6 + rd//14):
        return heuristic(board)
    for op in getOpen(board, turn):
        newBoard = copy.deepcopy(board)
        newBoard[op[0]][op[1]] = turn
        opScore = minimax(newBoard,depth+1,-turn,op,alpha,beta,rd)
        if myScores == [] or (opScore > myScores[0][1] and turn == 1) or (opScore < myScores[0][1] and turn == -1):
            myScores = [(op,opScore)]
        elif opScore == myScores[0][1]:
            myScores.append((op,opScore))
        if turn == 1:
            if myScores[0][1] > alpha:
                alpha = myScores[0][1]
            if alpha > beta:
                return alpha
        else:
            if myScores[0][1] < beta:
                beta = myScores[0][1]
            if alpha > beta:
                return beta
    if depth < 1:
        print(myScores) # << honestly i'm super proud of this so feel free to reactivate this and see how it's evaluating scores
        move = random.choice(myScores)
        print(['null','Red','Blue'][turn] + '\'s turn [0-6]:', move[0][0])
        return move[0], move[1]
    else:
        return random.choice(myScores)[1]


# EMPTY BOARD FOR TESTS
#[[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [-1, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]]
#testboard = [[-1, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0], [1, 1, 1, 0, 0, 0], [-1, 1, 0, 0, 0, 0], [-1, 0, 0, 0, 0, 0], [-1, 0, 0, 0, 0, 0]]
#print(heuristic(testboard))