# storing current game state, check valid moves, keep move log

import numpy as np

class GameState():
    def __init__(self):
        self.dimension = 8
        self.board = np.zeros([self.dimension, self.dimension])
        # 0 is empty space , -1 is black , 1 is red
        for i in range(2):
            for j in range(8):
                if (i % 2 == 0 and j % 2 == 0) or (i % 2 == 1 and j % 2 == 1):
                    self.board[i][j] = -1
                    self.board[i+6][j] = 1
        self.redToMove = True
        self.moveLog = []
        self.turn = 0

    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = 0
        self.board[move.destRow][move.destCol] = move.pieceMoved
        if move.pieceCapture[1] != -100:
            self.board[move.pieceCapture[0][0]][move.pieceCapture[0][1]] = 0
        self.checkPromote(move)
        self.moveLog.append(move)

    def checkPromote(self, move):
        if self.board[move.destRow][move.destCol] == 1 and move.destRow == 0:
            self.board[move.destRow][move.destCol] = 2
            self.redToMove = not self.redToMove
        elif self.board[move.destRow][move.destCol] == -1 and move.destRow == 7:
            self.board[move.destRow][move.destCol] = -2
            self.redToMove = not self.redToMove
        elif move.pieceCapture[1] == -100 or move.pieceCapture[1] == 0:
            self.redToMove = not self.redToMove
        elif move.pieceCapture != -100 and move.pieceCapture != 0 and not self.is_force_move(move.destRow, move.destCol, "BOOL"):
            self.redToMove = not self.redToMove

    def is_force_move(self, r, c, str):
        moves = []
        force_moves = []

        if abs(self.board[r][c]) == 1:
            self.getNormalMove(r, c, moves, force_moves)
        elif abs(self.board[r][c]) == 2:
            self.getBigMove(r, c, moves, force_moves)

        if str == "BOOL":
            return len(force_moves) != 0
        elif str == "MOVE":
            return force_moves

    def undoMove(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.destRow][move.destCol] = 0
            if move.pieceCapture[1] != -100 and move.pieceCapture[1] != 0:
                self.board[move.pieceCapture[0][0]][move.pieceCapture[0][1]] = move.pieceCapture[1]
            self.redToMove = move.player

    def getValidMove(self):
        moves = []
        force_moves = []

        if len(self.moveLog) != 0 and self.redToMove == self.moveLog[-1].player:
            return self.is_force_move(self.moveLog[-1].destRow, self.moveLog[-1].destCol, "MOVE")

        for r in range(self.dimension):
            for c in range(self.dimension):
                piece = self.board[r][c]
                if (self.redToMove and piece == 1) or (not self.redToMove and piece == -1):
                    self.getNormalMove(r, c, moves, force_moves)
                elif (self.redToMove and piece == 2) or (not self.redToMove and piece == -2):
                    self.getBigMove(r, c, moves, force_moves)

        if len(force_moves) != 0:
            return force_moves
        else:
            return moves

    def getNormalMove(self, r, c, moves, force_moves):
        allow_change = []
        d = int(self.board[r][c]) * -1
        for i in range(-2, 3):
              if i != 0 and c + i >= 0 and c + i < 8:
                   allow_change.append(i)
        for i in allow_change:
            if abs(i) == 1 and self.board[r+d][c+i] == 0:
                moves.append(Move((r, c), (r+d, c+i), self.board, self.redToMove))
            elif i == -2 and ((self.board[r][c] > 0 and self.board[r+d][c-1] < 0) or (self.board[r][c] < 0 and self.board[r+d][c-1] > 0)):
                if r+d+d >= 0 and r+d+d < 8 and self.board[r+d+d][c+i] == 0:
                        force_moves.append(Move((r, c), (r+d+d, c+i), self.board, self.redToMove))
            elif i == 2 and ((self.board[r][c] > 0 and self.board[r+d][c+1] < 0) or (self.board[r][c] < 0 and self.board[r+d][c+1] > 0)):
                if r+d+d >= 0 and r+d+d < 8 and self.board[r+d+d][c+i] == 0:
                        force_moves.append(Move((r, c), (r+d+d, c+i), self.board, self.redToMove))

    def getBigMove(self, r, c, moves, force_moves):
        direction = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        for d in direction:
            x = r + d[0]
            y = c + d[1]
            first_force = False
            while(x >= 0 and x < 8 and y >= 0 and y < 8):
                if not first_force:
                    if self.board[x][y] == 0:
                        moves.append(Move((r, c), (x, y), self.board, self.redToMove))
                    elif (self.board[r][c] > 0 and self.board[x][y] < 0) or (self.board[r][c] < 0 and self.board[x][y]):
                        if x+d[0] >= 0 and x+d[0] < 8 and y+d[1] >= 0 and y+d[1] < 8 and self.board[x+d[0]][y+d[1]] == 0:
                                force_moves.append(Move((r, c), (x+d[0], y+d[1]), self.board, self.redToMove))
                        first_force = True
                    else:
                        break
                else:
                    break
                x += d[0]
                y += d[1]

class Move():

    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startSq, destSq, board, player):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.destRow = destSq[0]
        self.destCol = destSq[1]
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.destRow * 10 + self.destCol
        self.moveDirection = (((self.destRow - self.startRow) // abs(self.destRow - self.startRow)), ((self.destCol - self.startCol) // abs(self.destCol - self.startCol)))
        self.moveDistance = abs(self.startRow - self.destRow)
        self.pieceMoved = board[self.startRow][self.startCol]
        if self.moveDistance > 1:
            self.pieceCapture = ((self.destRow - self.moveDirection[0], self.destCol - self.moveDirection[1]), board[self.destRow - self.moveDirection[0]][self.destCol - self.moveDirection[1]])
        else:
            self.pieceCapture = ((-100, -100), -100)
        self.player = player

    # compare class

    def __eq__(self,other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + " " + self.getRankFile(self.destRow, self.destCol)

    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]
