def outputFinalCodes(filename):
    '''
    This is a general function that will output codes.
    filename: input filename.
    '''
    if checkFileError(filename):
        return(9)
    with open(filename, encoding = 'ascii') as file:
        # find first non blank line to check for X Y and Z
        for line in nonblank_lines(file):
            if checkInvalidFile(line, True):
                return(8)
            X, Y, Z = [int(i) for i in line.split()]
            if checkIllegalGame(X, Y, Z):
                return(7)
            break
        # initialise empty grid history for player 1 and player 2
        gridHistP1 = []
        gridHistP2 = []
        # initialise empty height history for both players. It is used
        # to check for illegal row and grow grid history for both players.
        hgtHistBoth = {}
        move = 1
        for line in nonblank_lines(file):
            if checkInvalidFile(line, False):
                return(8)
            curWid = [int(i) for i in line.split()][0]
            # Check for illegal column
            if checkIllegaColumn(curWid, X):
                return(6)
            # grow the height history 'hgtHistBoth' by taking into the width
            # of the current grid.
            growhgtHistBoth(hgtHistBoth, curWid)
            if checkIllegalRow(hgtHistBoth[curWid], Y):
                return(5)
            # player 1 plays.
            if move % 2:
                # grow the grid history of player 1 by including the current grid.
                gridHistP1.append((curWid, hgtHistBoth[curWid]))
                if checkWin(curWid, hgtHistBoth[curWid], X, Y, Z, gridHist = gridHistP1):
                    if checkIllegalContinue(file):
                        return(4)
                    return(1)
            # player 2 plays
            else:
                # grow the grid history of player 2 by including the current grid.
                gridHistP2.append((curWid, hgtHistBoth[curWid]))
                if checkWin(curWid, hgtHistBoth[curWid], X, Y, Z, gridHist = gridHistP2):
                    if checkIllegalContinue(file):
                        return(4)
                    return(2)
            move += 1

    file.close()
    if checkDraw(gridHistP1, gridHistP2, X, Y):
        return(0)
    if checkIncomplete(gridHistP1, gridHistP2, X, Y):
        return(3)

def checkWin(x, y, X, Y, Z, gridHist):
    '''
    check for win in respect of four types of winning combinations.
    x: width of the current grid.
    y: height of the current grid.
    X: width of the frame.
    Y: height of the frame.
    Z: minimum number of counters to win,
    gridHist: the grid history of a certain player.
    '''
    # check for matching vertical winning combination
    vertWinCombin = [(x, y - i) for i in range(Z) if i < y + 1]
    if all(elem in gridHist for elem in vertWinCombin):
        return(True)
    # check for matching horizontal winning combination
    for j in range(Z - x + 1, X - x + 2):
        horiWinCombin = [(x + i, y) for i in range(-Z + j, j)]
        if all(elem in gridHist for elem in horiWinCombin):
            return(True)
    # check for matching main diaganol winning combination
    for j in range(max(Z - x, Z - y) + 1, min(X - x, Y - y) + 2):
        mainDiagWinCombin = [(x + i, y + i) for i in range(-Z + j, j)]
        if all(elem in gridHist for elem in mainDiagWinCombin):
            return(True)
    # check for matching anti-diaganol winning combination
    for j in range(max(Z - x + 1, Z - Y + y), min(X- x + 2, y + 1)):
        antiDiagWinCombin = [(x + i, y - i) for i in range(-Z + j, j)]
        if all(elem in gridHist for elem in antiDiagWinCombin):
            return(True)
    return(False)

def checkDraw(gridHist1, gridHist2, X, Y):
    '''
    check for draw. If draw, return True, else return False.
    Note that all game checking functions should be called
    except for Incomplete before calling this function.
    gridHist1: grid history of player 1.
    gridHist2: grid history of player 2.
    X: width of the frame.
    Y: height of the frame.
    '''
    if len(gridHist1) + len(gridHist2) == X*Y:
        return(True)
    return(False)

def checkIncomplete(gridHist1, gridHist2, X, Y):
    '''
    check for incomplete. If incomplete, return True, else return False.
    Note that all game checkings should be called before calling this function.
    gridHist1: grid history of player 1.
    gridHist2: grid history of player 2.
    X: width of the frame.
    Y: height of the frame.
    '''
    if len(gridHist1) + len(gridHist2) < X*Y:
        return(True)
    return(False)

def checkIllegalContinue(f):
    '''
    check for illegal continue by stripping off empty lines after winning move.
    If illegal, return True, else return False.
    f: file object.
    '''
    for line in nonblank_lines(f):
        if line:
            return(True)
    return(False)

def checkIllegalRow(y, Y):
    '''
    check for illegal row. If illegal, return True, else return False.
    y: height of the current grid.
    Y: height of the frame.
    '''
    if y > Y:
        return(True)
    return(False)

def checkIllegaColumn(x, X):
    '''
    check for illegal column. If illegal, return True, else return False.
    x: width of the current grid.
    X: width of the frame.
    '''
    if x > X or x < 0:
        return(True)
    return(False)

def checkIllegalGame(X, Y, Z):
    '''
    check for illegal game. If illegal, return True, else return False.
    X: width of the frame.
    Y: height of the frame.
    Z: minimum counters to win.
    '''
    if X < Z and Y < Z:
        return(True)
    return(False)

def checkInvalidFile(l, first):
    '''
    check for invalid file for both the first row and all the following rows.
    Note that if there are not exactly three numbers in the first row, it is
    a file error. For all the following rows, if there is more than one number
    in the following row, it is also a file error.
    l: line string in the file object.
    first: boolean value. True if it is first line in the file object. False
    otherwise.
    '''
    if first:
        try:
            X, Y, Z = [int(i) for i in l.split()]
        except:
            return(True)
    else:
        try:
            curCol = [int(i) for i in l.split()]
        except:
            return(True)
    # if there are more than one number in a row, the file is invalid.
        if len(curCol) > 1:
            return(True)
    return(False)

def checkFileError(filename):
    '''
    check for file error. If illegal, return True, else return False.
    filename: input filename.
    '''
    try:
        open(filename, 'rt', encoding = 'ascii')
    except:
        return(True)
    return(False)

def growhgtHistBoth(hgtStore, wid):
    '''
    grow the height history for all grids.
    hgtStore: a directionary mapping width to height of all grids.
    wid: width of the current grid.
    '''
    if wid in hgtStore:
        hgtStore[wid] += 1
    else:
        hgtStore[wid] = 1

def nonblank_lines(f):
    '''
    Clean data by stripping off whitespace/empty line. It returns line generator.
    f: a file object.
    '''
    for l in f:
        if l.rstrip():
            yield l

# The following code deals with the customised output when given incorrect parameters
import sys
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("connectz.py: Provide one input file")
    else:
        print(outputFinalCodes(sys.argv[1]))
        sys.exit(1)
