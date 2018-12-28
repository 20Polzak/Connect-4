# connect4.py is a text-based Connect 4 game
# 1/17/18
__author__ = 'Christos Polzak'

import minimax2

def buildboard(): #creates the board
    board = []
    global userPick
    userPick = ['\033[37m ','\033[31m●','\033[35m●','\033[36m●']
    for k in range(7):
        board.append([])
        for i in range(6):
            board[k].append(0)
    return board

def printboard(board): # prints the board after every turn
    global userPick
    for i in range(6):
        for k in range(7):
            print('\033[37;4m|',end='')
            print(userPick[board[k][-(i+1)]],end='') #0-th item in each column is the bottom; array organized as columns with slots
        print('\033[37;4m|')
    print('\033[0;37;0m 0 1 2 3 4 5 6')

def endcheck(board, c, r): # checking win
    if c == r == -1:
        return (False,None)
    for k in range(4):
        try:
            if (board[c-k][r] == board[c-k+1][r] == board[c-k+2][r] == board[c-k+3][r]) and (c - k >= 0): # horizontal (L->R)
                for j in range(4):
                    board[c-k+j][r] *= 2
                return (True,board[c][r]//2)
        except:
            pass
    if r > 2 and (board[c][r] == board[c][r-1] == board[c][r-2] == board[c][r-3]): # vertical
        for j in range(4):
            board[c][r-j] *= 2
        return (True,board[c][r]//2)
    for i in range(4):
        try:
            if (board[c-i][r-i] == board[c-i+1][r-i+1] == board[c-i+2][r-i+2] == board[c-i+3][r-i+3]) and (r-i >= 0) and (c-i >= 0): # diagonal /
                for j in range(4):
                    board[c-i+j][r-i+j] *= 2
                return (True,board[c][r]//2)
        except:
            pass
        try:
            if (board[c-i][r+i] == board[c-i+1][r+i-1] == board[c-i+2][r+i-2] == board[c-i+3][r+i-3])  and (c-i >= 0) and (r+i-3 >= 0): # diagonal \
                for j in range(4):
                    board[c-i+j][r+i-j] *= 2
                return (True,board[c][r]//2)
        except:
            pass
    # if board full
    for k in range(7):
        if 0 in board[k]:
            return (False, None)
    return (True,0)

def isOpen(board, c): # checks if slot is open
    for k in range(6):
        if board[c][k] == 0:
            return (True, k)
    return (False, None)

def comp(board,turn,rd): # computer's move
    return minimax2.minimax(board, 0, turn, (-1,-1),-1000000000,100000000,rd)

def play(mode): # gameplay function
    while True:
        board = buildboard()
        printboard(board)
        uIn = -10
        movState = False,-10
        if mode == 3 or mode == 4:
            turn = -1
        else:
            turn = 1
        gameWon = False
        cc = -1
        rr = -1
        rd = 0
        while not gameWon:
            rd += 1
            if (turn == 1 or mode == 1) and mode != 4:
                uIn = None
                while uIn not in ['0','1','2','3','4','5','6']:
                    uIn = input(['null','Red','Blue'][turn] + '\'s turn [0-6]:')
                    if uIn == 'pb':
                        print(board)
                uIn = int(uIn)
                movState = isOpen(board,uIn)
                if movState[0]:
                    board[uIn][movState[1]] = turn
                    cc = uIn
                    rr = movState[1]
                    turn *= -1
                else:
                    print('Invalid play.')
            else:
                if board == [[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]]:
                    cc, rr = 3, 0
                    print('Blue\'s turn [0-6]: 3')
                else:
                    print('Thinking...')
                    cc, rr = comp(board,turn,rd)[0]
                board[cc][rr] = turn
                turn *= -1
            printboard(board)
            gameWon,winslot = endcheck(board,cc,rr)
        print(['Draw.','\033[31mRed wins.\033[37m','\033[36mBlue wins.\033[37m'][winslot])
        printboard(board)
        return

def entry(): # introduces game, determines play mode
    while True:
        mode = -3
        print("Welcome to Connect 4. Please select a mode.\n1 = 2-player mode\n2 = VS computer [player first]\n3 = VS computer [computer first]\n4 = computer plays itself [BUGTEST]")
        while mode not in [1,2,3,4]:
            try:
                mode = int(input('Mode:'))
            except:
                pass
        play(mode)
        if not 'y' in input('Play again?').lower():
            break



if __name__ == '__main__': # entry point
    entry()