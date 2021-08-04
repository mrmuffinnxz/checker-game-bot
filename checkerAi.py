import random

def mini_max_ai(player, gs):
    valid_moves = gs.getValidMove()
    moves_score = [-100000] * len(valid_moves)
    for i in range(len(valid_moves)):
        gs.makeMove(valid_moves[i])
        moves_score[i] = get_move_score(player, gs, 1)
        gs.undoMove()
    max_score = max(moves_score)
    max_score_move = [valid_moves[i] for i, j in enumerate(moves_score) if j == max_score]
    print(moves_score)
    return random.choice(max_score_move)

def get_move_score(player, gs, depth):
    print("Loading... : " + str(depth))
    valid_moves = gs.getValidMove()
    max_depth = 3

    if len(valid_moves) == 0:
        if gs.redToMove == player:
            return -10000
        else:
            return 10000
    if depth == max_depth:
        return evaluation_score(player, gs)

    if gs.redToMove == player:
        min_score = 50000
        for m in valid_moves:
            gs.makeMove(m)
            score = get_move_score(player, gs, depth + 1)
            gs.undoMove()
            min_score = min(min_score, score)
        return min_score
    else:
        max_score = -50000
        for m in valid_moves:
            gs.makeMove(m)
            score = get_move_score(player, gs, depth + 1)
            gs.undoMove()
            max_score = max(max_score, score)
        return max_score

def evaluation_score(is_player_red, gs):
    SR = 0
    SB = 0
    for r in gs.board:
        for c in r:
            if c == 1:
                SR += 1
            elif c == -1:
                SB += 1
            elif c == 2:
                SR += 3
            elif c == -2:
                SB += 3
    if is_player_red == True:
        return SR - SB
    else:
        return SB - SR
