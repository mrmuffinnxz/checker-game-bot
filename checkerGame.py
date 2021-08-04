# main game file,user input, displaying

import pygame as pg
import checkerEngine
import random
import checkerAi

WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 60
IMAGES = {}

# initialize images
def loadImages():
    IMAGES[1] = pg.transform.scale(pg.image.load("pieces/red_piece.png"), (SQ_SIZE, SQ_SIZE))
    IMAGES[2] = pg.transform.scale(pg.image.load("pieces/big_red_piece.png"), (SQ_SIZE, SQ_SIZE))
    IMAGES[-1] = pg.transform.scale(pg.image.load("pieces/black_piece.png"), (SQ_SIZE, SQ_SIZE))
    IMAGES[-2] = pg.transform.scale(pg.image.load("pieces/big_black_piece.png"), (SQ_SIZE, SQ_SIZE))

# check display and command

def showValidMoves(validMoves):
    for m in validMoves:
        print(m.moveID)
    print("----------------------------")

def showTurn(is_red_turn):
    if is_red_turn:
        print("Red Turn!")
    else:
        print("Black Turn!")

# human input code

def humanMoves(running, playerClicks, gs, sqSelected, validMoves, moveMade):
    for e in pg.event.get():
        if e.type == pg.QUIT:
            running = False
        # mouse input
        elif e.type == pg.MOUSEBUTTONDOWN:
            location = pg.mouse.get_pos()
            col = location[0] // SQ_SIZE
            row = location[1] // SQ_SIZE
            if (len(playerClicks) == 0 and gs.board[row][col] == 0) or sqSelected == (row, col):
                sqSelected = ()
                playerClicks = []
            else:
                sqSelected = (row, col)
                playerClicks.append(sqSelected)
            if len(playerClicks) == 2:
                if playerClicks[0][0] != playerClicks[1][0] and playerClicks[0][1] != playerClicks[1][1]:
                    move = checkerEngine.Move(playerClicks[0], playerClicks[1], gs.board, gs.redToMove)
                    if move in validMoves:
                        print(move.getChessNotation())
                        gs.makeMove(move)
                        moveMade = True
                sqSelected = []
                playerClicks.clear()
        # key input
        elif e.type == pg.KEYDOWN:
            if e.key == pg.K_z:
                gs.undoMove()
                moveMade = True
                sqSelected = []
                playerClicks.clear()

# main driver, user input, update graphic
def main():
    pg.init()
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    clock = pg.time.Clock()
    screen.fill(pg.Color("white"))
    gs = checkerEngine.GameState()
    validMoves = gs.getValidMove()
    moveMade = False
    loadImages()
    running = True
    sqSelected = ()
    playerClicks = []
    showTurn(gs.redToMove)
    while running:
        if gs.redToMove:
            humanMoves(running, playerClicks, gs, sqSelected, validMoves, moveMade)
        else:
            move = checkerAi.mini_max_ai(gs.redToMove, gs)
            print(move.getChessNotation())
            gs.makeMove(move)
            moveMade = True

        if moveMade:
            validMoves = gs.getValidMove()
            showTurn(gs.redToMove)
            print("ValidMoves : " + str(len(validMoves)))
            moveMade = False

        if len(validMoves) == 0:
            if gs.redToMove:
                print("Black Win!")
            else:
                print("Red Win!")
            running = False

        drawGameState(screen, gs, playerClicks)
        clock.tick(MAX_FPS)
        pg.display.flip()

# graphic in current game state
def drawGameState(screen, gs, playerClicks):
    drawBoard(screen)
    drawPieces(screen, gs.board)
    drawSelectedPieces(screen, playerClicks)

def drawBoard(screen):
    colors = [pg.Color("white"), pg.Color("gray")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r+c) % 2)]
            pg.draw.rect(screen, color, pg.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != 0:
                screen.blit(IMAGES[piece], pg.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

def drawSelectedPieces(screen, playerClicks):
    for sq in playerClicks:
        pg.draw.rect(screen, pg.Color("green"), pg.Rect(sq[1]*SQ_SIZE, sq[0]*SQ_SIZE, SQ_SIZE, SQ_SIZE), 5)

if __name__ == "__main__":
    main()
