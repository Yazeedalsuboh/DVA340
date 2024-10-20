#!/usr/bin/python           # This is server.py file

import socket  # Import socket module
import numpy as np
import time
from multiprocessing.pool import ThreadPool
import os


def receive(socket):
    msg = ''.encode()  # type: str

    try:
        data = socket.recv(1024)  # type: object
        msg += data
    except:
        pass
    return msg.decode()


def send(socket, msg):
    socket.sendall(msg.encode())


# VARIABLES
playerName = 'Yazeed_AlSuboh'
host = '127.0.0.1'
port = 30000  # Reserve a port for your service.
s = socket.socket()  # Create a socket object
pool = ThreadPool(processes=1)
gameEnd = False
MAX_RESPONSE_TIME = 5

print('The player: ' + playerName + ' starts!')
s.connect((host, port))
print('The player: ' + playerName + ' connected!')

while not gameEnd:

    asyncResult = pool.apply_async(receive, (s,))
    startTime = time.time()
    currentTime = 0
    received = 0
    data = []
    while received == 0 and currentTime < MAX_RESPONSE_TIME:
        if asyncResult.ready():
            data = asyncResult.get()
            received = 1
        currentTime = time.time() - startTime

    if received == 0:
        print('No response in ' + str(MAX_RESPONSE_TIME) + ' sec')
        gameEnd = 1

    if data == 'N':
        send(s, playerName)

    if data == 'E':
        gameEnd = 1

    if len(data) > 1:

        # Read the board and player turn
        board = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        playerTurn = int(data[0])
        i = 0
        j = 1
        while i <= 13:
            board[i] = int(data[j]) * 10 + int(data[j + 1])
            i += 1
            j += 2

        # Using your intelligent bot, assign a move to "move"
        #
        # example: move = '1';  Possible moves from '1' to '6' if the game's rules allows those moves.
        # TODO: Change this
        ################
        board = {'pit_index': 0,'board': board, 'captured': False, 'free turn': False}
        minAgent = [0, 6]
        maxAgent = [7, 13]

        def minmax(board, depth, is_maximizing_player):
            if depth == 0:
                return evaluate_board(board), None

            if is_maximizing_player:
                max_score = float('-inf')
                best_move = None
                available_moves = get_available_moves(board, maxAgent)
                if len(available_moves) == 1:  # Only one possible move
                    return evaluate_board(available_moves[0]), available_moves[0]
                for move in available_moves:
                    score, _ = minmax(move, depth - 1, False)
                    if score > max_score:
                        max_score = score
                        best_move = move
                return max_score, best_move
            else:
                min_score = float('inf')
                best_move = None
                available_moves = get_available_moves(board, minAgent)
                for move in available_moves:
                    score, _ = minmax(move, depth - 1, True)
                    if score < min_score:
                        min_score = score
                        best_move = move
                return min_score, best_move

        def get_available_moves(board, agent):
            start_index, store_index = agent
            board_length = 13
            available_moves = []

            for pit_index in range(start_index, store_index):

                move_record = {'pit_index': pit_index, 'board': [], 'xboard': board['board'], 'captured': False, 'free turn': False}
                new_board = board['board'][:]
                num_stones = new_board[pit_index]
                if num_stones != 0:
                    current_pit = pit_index

                    new_board[pit_index] = 0
                    for i in range(num_stones):
                        current_pit = (current_pit + 1) % (board_length+1)
                        new_board[current_pit] += 1

                    if new_board[current_pit] == 1 and current_pit != store_index:
                        move_record['captured'] = True
                        new_board[store_index] += new_board[board_length-1-current_pit] + new_board[current_pit]
                        new_board[board_length-1-current_pit] = new_board[current_pit] = 0
                    
                    if current_pit == agent[1]:
                        move_record['free turn'] = True

                    move_record['board'] = new_board
                    available_moves.append(move_record)

            return available_moves
                        
        def evaluate_board(move):
            score = 0
            maxPits = move['board'][maxAgent[0]:maxAgent[1]+1]
            minPits = move['board'][minAgent[0]:minAgent[1]+1]

            stones_in_left_pit = maxPits[-2]
            stones_in_pit = sum(maxPits[:-1])
            non_empty_pits = sum(1 for pit in maxPits[:-1] if pit != 0)
            new_stones_in_store = maxPits[-1]-move['xboard'][-1]
            new_stones_in_opponent_store = -(minPits[-1] - move['xboard'][6])
            free_turn = 1 if move['free turn'] else 0
            captured = 1 if move['captured'] else 0
            store_difference = maxPits[-1] - minPits[-1]

            heuristics = [stones_in_left_pit, stones_in_pit, non_empty_pits, new_stones_in_store, new_stones_in_opponent_store, free_turn, captured, store_difference]

            for h in heuristics:
                score += h
            return score

        best_move = minmax(board, 3, True)

        move = str(best_move[1]['pit_index'] - 6)
        send(s, move)