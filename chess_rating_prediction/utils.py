import pandas as pd
import numpy as np
import chess
import chess.engine 
import chess.pgn
from stockfish import Stockfish

import chess
import chess.engine

def compute_blunders_and_best(moves, engine, time_limit=0.01, blunder_threshold=200):
    """
    Compute number of blunders and best moves for White and Black.
    Expects UCI format moves (e.g. "e2e4 e7e5 g1f3 b8c6").
    Returns (white_best_moves, black_best_moves, white_blunders, black_blunders).
    """
    board = chess.Board()

    white_blunders = black_blunders = 0
    white_best_moves = black_best_moves = 0

    for move in moves.split():
        try:
            player = board.turn  # True = White, False = Black

            # evaluate current position
            info = engine.analyse(board, chess.engine.Limit(time=time_limit))
            if "pv" not in info:
                continue
            best_move = info["pv"][0]
            best_score = info["score"].pov(player)

            # play actual move
            move_obj = chess.Move.from_uci(move)
            if move_obj not in board.legal_moves:
                continue
            board.push(move_obj)

            # evaluate new position
            new_info = engine.analyse(board, chess.engine.Limit(time=time_limit))
            new_score = new_info["score"].pov(player)

            # convert scores (centipawns, mate → 10000)
            best_cp = best_score.score(mate_score=10000)
            new_cp = new_score.score(mate_score=10000)

            diff = best_cp - new_cp

            # check blunder
            if diff is not None and diff >= blunder_threshold:
                if player:  # White moved
                    white_blunders += 1
                else:       # Black moved
                    black_blunders += 1

            # check best move
            if move_obj == best_move:
                if player:
                    white_best_moves += 1
                else:
                    black_best_moves += 1

        except Exception:
            continue

    return white_best_moves, black_best_moves, white_blunders, black_blunders








def Pgn_to_Dataframe(path):
    """
        This function parses through the PGN file and converts it into pandas data frame to be used later 
    """
    pgn = open("games.pgn")
    # Parse all games into DataFrame rows
    games = []
    max_games = 2000
    while len(games) < max_games:
        game = chess.pgn.read_game(pgn)
        if game is None:
            break

        games.append({
            "white_rating": game.headers.get("WhiteElo"),
            "black_rating": game.headers.get("BlackElo"),
            "result": game.headers.get("Result"),
            "opening": game.headers.get("Opening"),
            "time_control": game.headers.get("TimeControl"),
            "moves": " ".join(str(move) for move in game.mainline_moves())
        })
    # Create DataFrame directly
    df = pd.DataFrame(games)
    df['num_moves'] = df['moves'].apply(lambda x: len(x.split())) # adding the game length column
    df.to_csv("games_dataset")



def parse_time_control(tc_str):

    """
        Parses a time control string and categorizes it into bullet, blitz, rapid, or classical.
    """
    # Split the string by '+'
    parts = tc_str.split("+")
    # Get the main time (always the first part)
    main_time = int(parts[0])
    # Check if there's an increment part
    if len(parts) > 1:
        inc_time = int(parts[1])
    else:
        # If no increment is present, set it to 0
        inc_time = 0
    if main_time <= 179:  # < 3 minutes
        category = "bullet"
    elif main_time <= 599:  # 3 to 10 minutes
        category = "blitz"
    elif main_time <= 3599:  # 10 to 60 minutes
        category = "rapid"
    else:  # > 60 minutes
        category = "classical"
    
    return category
  

def compute_acpl_per_player(moves: str, stockfish_path: str, time_limit=0.01):
    """
    Compute the ACPL separately for White and Black.
    :param moves: moves in SAN format separated by spaces, e.g. "e4 e5 Nf3 Nc6"
    :param stockfish_path: path to Stockfish engine executable
    :param time_limit: time in seconds for Stockfish to analyze each position
    :return: tuple (white_acpl, black_acpl)
    """
    board = chess.Board()
    move_list = moves.split()

    engine = chess.engine.SimpleEngine.popen_uci(stockfish_path)

    white_loss = 0
    black_loss = 0
    white_moves = 0
    black_moves = 0

    max_loss = 300  # Cap maximum centipawn loss to avoid skew from big blunders or mate scores

    for move in move_list:
        player = board.turn  # player to move BEFORE the move

        info_before = engine.analyse(board, chess.engine.Limit(time=time_limit))
        score_before = info_before["score"].pov(player).score(mate_score=10000)

        board.push_san(move)

        info_after = engine.analyse(board, chess.engine.Limit(time=time_limit))
        score_after = info_after["score"].pov(player).score(mate_score=10000)

        if score_before is not None and score_after is not None:
            loss = score_before - score_after
            loss = min(abs(loss), max_loss)

            if player == chess.WHITE:
                white_loss += loss
                white_moves += 1
            else:
                black_loss += loss
                black_moves += 1
       

    engine.quit()

    white_acpl = white_loss / white_moves if white_moves else 0
    black_acpl = black_loss / black_moves if black_moves else 0

    return white_acpl, black_acpl


def encode_chess_result(result_string):
    """
    Encodes a chess result string into numerical values for White and Black.
    
    Args:
        result_string (str): '1-0', '0-1', or '1/2-1/2'
    
    Returns:
        tuple: (white_score, black_score)
    """
    if result_string == '1-0':       # White wins
        return 1.0,0.0
    elif result_string == '0-1':     # Black wins
        return 0.0, 1.0
    elif result_string == '1/2-1/2': # Draw
        return 0.5, 0.5
















