def evaluate(board, player, bigPlayer=None):
    rows, cols = len(board), len(board[0])
    result = 0

    # Проверяем горизонтальные линии
    for row in range(rows):
        if all(board[row][col] == player or board[row][col] == ' ' for col in range(cols)):
            result += 1

    # Проверяем вертикальные линии
    for col in range(cols):
        if all(board[row][col] == player or board[row][col] == ' ' for row in range(rows)):
            result += 1

    # Проверяем диагонали
    if all(board[i][i] == player or board[i][i] == ' ' for i in range(min(rows, cols))):
        result += 1

    if all(board[i][cols - 1 - i] == player or board[i][cols - 1 - i] == ' ' for i in range(min(rows, cols))):
        result += 1

    sumOfSymbolG = [0, 0]
    sumOfSymbolV = [0, 0]
    sumOfSymbolD1 = [0, 0]
    sumOfSymbolD2 = [0, 0]

    for i in range(3):
        row_count = sum(int(board[i][j] == player) for j in range(
            3))  # проверяем суммы одинаковых крестиков или ноликов в линии, если таких 2, значит игрок может победить следующим ходом и его оценка хода максимальна
        col_count = sum(int(board[j][i] == player) for j in range(3))
        diag1_count = sum(int(board[i][i] == player) for i in range(3))
        diag2_count = sum(int(board[i][2 - i] == player) for i in range(3))

        if row_count > sumOfSymbolG[0]:
            sumOfSymbolG = [row_count, sum(int(board[i][j] == ' ') for j in range(3))]

        if col_count > sumOfSymbolV[0]:
            sumOfSymbolV = [col_count, sum(int(board[j][i] == ' ') for j in range(3))]

        if diag1_count > sumOfSymbolD1[0]:
            sumOfSymbolD1 = [diag1_count, sum(int(board[i][i] == ' ') for i in range(3))]

        if diag2_count > sumOfSymbolD2[0]:
            sumOfSymbolD2 = [diag2_count, sum(int(board[i][2 - i] == ' ') for i in range(3))]

    if sumOfSymbolG == [2, 1] or sumOfSymbolV == [2, 1] or sumOfSymbolD1 == [2, 1] or sumOfSymbolD2 == [2,
                                                                                                        1] and bigPlayer is not None and bigPlayer != player: result = 9
    if player == '0': result *= -1
    return result


def possible_moves(board):
    # Возвращает список доступных ходов
    return [(i, j) for i in range(3) for j in range(3) if board[i][j] == ' ']


def make_move(board, move, player):
    # Выполнение хода для минмаксинга
    new_board = [row.copy() for row in board]
    new_board[move[0]][move[1]] = player
    return new_board


def is_winner(board, player):
    # Проверка выигрышных комбинаций по горизонтали, вертикали и диагоналям
    for i in range(3):
        if all(board[i][j] == player for j in range(3)) or \
                all(board[j][i] == player for j in range(3)):
            return True
    if all(board[i][i] == player for i in range(3)) or \
            all(board[i][2 - i] == player for i in range(3)):
        return True
    return False


def is_board_full(board):
    # Проверка, заполнена ли доска
    return all(cell != ' ' for row in board for cell in row)


def alpha_beta(board, depth, alpha, beta, maximizing_player):
    if depth == 0 or is_winner(board, 'X') or is_winner(board, 'O') or is_board_full(board):
        return checkPos(board), None  # Теперь возвращаем и ход, и его оценку

    best_move = None
    if maximizing_player:
        best_value = float('-inf')
        for move in possible_moves(board):
            value, _ = alpha_beta(make_move(board, move, 'X'), depth - 1, alpha, beta, False)
            if value > best_value:
                best_value = value
                best_move = move
            alpha = max(alpha, best_value)
            if beta <= alpha:
                break  # отсечение
        return best_value, best_move
    else:
        best_value = float('inf')
        for move in possible_moves(board):
            value, _ = alpha_beta(make_move(board, move, 'O'), depth - 1, alpha, beta, True)
            if value < best_value:
                best_value = value
                best_move = move
            beta = min(beta, best_value)
            if beta <= alpha:
                break  # отсечение
        return best_value, best_move


def checkPos(board):
    pos = evaluate(board, 'X') + evaluate(board, '0')
    if evaluate(board, 'X') == 10 and evaluate(board, '0') == -10:
        if whoMoveNow(board) == 'X':
            pos = 10
        elif whoMoveNow(board) == '0':
            pos = -10
    if evaluate(board, 'X') == 8 and evaluate(board, '0') == -8:
        if whoMoveNow(board) == 'X':
            pos = 8
        elif whoMoveNow(board) == '0':
            pos = -8

    for i in range(3):
        if all(board[i][j] == '0' for j in range(3)) or \
                all(board[j][i] == '0' for j in range(3)):
            pos = -11
        if all(board[i][j] == 'X' for j in range(3)) or \
                all(board[j][i] == 'X' for j in range(3)):
            pos = 11

    if all(board[i][i] == '0' for i in range(3)) or \
            all(board[i][2 - i] == '0' for i in range(3)):
        pos = -11
    if all(board[i][i] == 'X' for i in range(3)) or \
            all(board[i][2 - i] == 'X' for i in range(3)):
        pos = 11



    return pos



def whoMoveNow(board):
    countX = 0
    countO = 0
    for row in board:
        for col in row:
            if col == 'X':
                countX += 1
            elif col == '0':
                countO += 1
    if countX == countO:
        result = 'X'
    else:
        result = '0'
    return result


board = [[' ', ' ', ' '],
         [' ', ' ', ' '],
         [' ', ' ', ' ']]

depth = 9
_, best_move = alpha_beta(board, depth, float('-inf'), float('inf'), False)
if is_winner(board, 'X'):
    print('X is win')
elif is_winner(board, '0'):
    print('0 is win')
elif is_board_full(board):
    print('board is full')
else:
    print("Лучший ход для X:", best_move)
    print(checkPos(board))
