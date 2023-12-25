from ab import *


def checkWin(board):
    rows, cols = len(board), len(board[0])

    for row in range(rows):
        if all(board[row][col] != whoMoveNowBig(bgf) for col in range(cols)) and all(
                board[row][col] != ' ' for col in range(cols)):
            return whoMoveNowBig(bgf)

    for col in range(cols):
        if all(board[row][col] == whoMoveNowBig(bgf) for row in range(rows)) and all(
                board[row][col] != ' ' for col in range(cols)):
            return whoMoveNowBig(bgf)

    # Проверяем диагонали
    if all(board[i][i] == whoMoveNowBig(bgf) for i in range(min(rows, cols))) and all(
            board[row][col] != ' ' for col in range(cols)):
        return whoMoveNowBig(bgf)

    if all(board[i][cols - 1 - i] == whoMoveNowBig(bgf) for i in range(min(rows, cols))) and all(
            board[row][col] != ' ' for col in range(cols)):
        return whoMoveNowBig(bgf)

    return None


def whoMoveNowBig(bfg):
    boardArray = [bfg.field[i][j].getField() for i in range(3) for j in range(3)]
    countO = 0
    countX = 0
    for i in boardArray:
        for j in i:
            for row in j:
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


def checkPosBig(board):
    pos = evaluate(board, 'X') + evaluate(board, '0')
    if evaluate(board, 'X') == 9 and whoMoveNowBig(bgf) == '0':
        pos = 10
    if evaluate(board, '0') == -9 and whoMoveNowBig(bgf) == 'X':
        pos = -10
    if evaluate(board, 'X') == 8 and evaluate(board, '0') == -8:
        if whoMoveNowBig(bgf) == 'X':
            pos = 8
            if evaluate(board, '0') == -10: pos = 10
        elif whoMoveNowBig(bgf) == '0':
            pos = -8
            if evaluate(board, 'X') == 10: pos = -10
    # #print(whoMoveNowBig(bgf))
    if whoMoveNowBig(bgf) == 'X' and evaluate(board, '0') == -9: pos = -10
    if whoMoveNowBig(bgf) == '0' and evaluate(board, 'X') == 9: pos = 10
    if whoMoveNowBig(bgf) == 'X' and abs(evaluate(board, '0', whoMoveNowBig(bgf))) == 9: pos = -10
    if whoMoveNowBig(bgf) == '0' and abs(evaluate(board, 'X', whoMoveNowBig(bgf))) == 9: pos = 10

    return pos


class BigGameField:
    def __init__(self):
        self.field = [[SmallGameField() for _ in range(3)] for _ in range(3)]

    def print_field(self, x, y):
        self.field[x][y].print_field()

    def move(self, big_field_indices, small_field_indices, symbol):
        x, y = big_field_indices
        small_field = self.field[x][y]
        small_field.move(small_field_indices, symbol)

    def printAllField(self):
        for w in range(3):
            for x in range(3):
                for y in range(3):
                    for z in range(3):
                        cell = self.field[w][y].field[x][z]
                        if cell.isKrest:
                            print('[ X ]', end=' ')
                        elif cell.isNol:
                            print('[ 0 ]', end=' ')
                        else:
                            print('[   ]', end=' ')

                        if z != 2:
                            print(" ", end=' ')
                    if y != 2:
                        print(" * ", end=' ')
                print()
            if w != 2:
                print()
        print()


class SmallGameField:
    def __init__(self):
        self.field = [[Cell() for _ in range(3)] for _ in range(3)]

    def printField(self):
        for row in self.field:
            for cell in row:
                cell.print()
            print()

    def getField(self):
        return [[self.field[i][j].getCell() for j in range(3)] for i in range(3)]

    def move(self, indices, symbol):
        i, j = indices
        cell = self.field[i][j]
        if symbol == 'X':
            cell.isKrest = True
            cell.isNone = False
        elif symbol == '0':
            cell.isNol = True
            cell.isNone = False


class Cell:
    def __init__(self):
        self.isKrest = False
        self.isNol = False
        self.isNone = True

    def getCell(self):
        if self.isKrest: return 'X'
        if self.isNol: return '0'
        if self.isNone: return ' '

    def print(self):
        if self.isKrest:
            print('[ X ]', end='')
        elif self.isNol:
            print('[ 0 ]', end='')
        else:
            print('[   ]', end='')


def to_ternary(n):
    result = ""
    while n > 0:
        remainder = n % 3
        result = str(remainder) + result
        n = n // 3
    return result if result else "0"


def find_max_indexes(arr):
    if not arr:
        return []

    max_value = max(arr)
    indexes = [index for index, value in enumerate(arr) if value == max_value]

    return indexes


import random


def arrayOfMaxIndex(arr):
    return sorted(range(len(arr)), key=lambda k: arr[k], reverse=True)


def find_random_max_index(arr):
    indexes = find_max_indexes(arr)
    if not indexes:
        return None

    random_index = random.choice(indexes)
    return random_index


if __name__ == "__main__":
    winFlag=0
    bgf = BigGameField()
    depth = 5
    actCount = 0
    countMiss = 0
    board = bgf.field[1][1].getField()  # первый ход пк
    _, best_move = alpha_beta(board, depth, float('-inf'), float('inf'), False)
    lastMove = [1, 1]
    bgf.move(lastMove, best_move, 'X')
    lastMove = best_move
    bgf.printAllField()
    a = [checkPosBig(k) for k in [bgf.field[i][j].getField() for i in range(3) for j in range(3)]]
    print(whoMoveNowBig(bgf), " - ", a)
    # b = [alpha_beta(h, depth, float('-inf'), float('inf'), False) for h in
    # [bgf.field[i][j].getField() for i in range(3) for j in range(3)]]
    # print(whoMoveNowBig(bgf), " - ", b)

    if int(to_ternary(a.index(max(a)))) < 10:  # переводим самую выгодную позицию в индекс
        buf = [0, to_ternary(a.index(max(a)))]
    else:
        buf = [int(to_ternary(a.index(max(a)))) // 10, int(to_ternary(a.index(max(a)))) % 10]
    print('index', buf)


    while all(a) != 10:
        print(lastMove)
        playerInput = input().split(',')  # записываем ходи игрока
        playerInput = [int(playerInput[0]), int(playerInput[1])]
        while bgf.field[int(lastMove[0])][int(lastMove[1])].getField()[playerInput[0]][
            playerInput[1]] != ' ':  # если ячейка уже занята - перезаписываем
            print(playerInput, lastMove, bgf.field[int(lastMove[0])][int(lastMove[1])].getField())
            print('error')
            playerInput = input().split(',')
            playerInput = [int(playerInput[0]), int(playerInput[1])]
        actBoard = bgf.field[lastMove[0]][lastMove[1]].getField()
        print(actBoard)
        for i in range(3):
            for j in range(3):
                if actBoard[i][j] == ' ': countMiss += 1
                if actBoard[i][j] == whoMoveNowBig(bgf):
                    actCount += 1
                    if actCount == 2 and countMiss == 1:
                        print('this board winner G')
                        winFlag=1
                        #assert ('this board was win on G by ', whoMoveNowBig(bgf))


            countMiss = 0
            actCount = 0

        for i in range(3):
            for j in range(3):
                if actBoard[j][i] == ' ': countMiss += 1
                if actBoard[j][i] == whoMoveNowBig(bgf):
                    actCount += 1
                    if actCount == 2:
                        print('this board winner V')
                        winFlag = 1
                        #assert ('this board was win on V by ', whoMoveNowBig(bgf))
            countMiss = 0
            actCount = 0

        bgf.move([lastMove[0], lastMove[1]], playerInput, '0')  # выполняем ход игрока
        lastMove = playerInput  # помечаем ход игрока для выбора ячейки для следующего хода пк
        bgf.printAllField()

        a = [checkPosBig(k) for k in [bgf.field[i][j].getField() for i in range(3) for j in range(3)]]
        print(whoMoveNowBig(bgf), " - ", a)  # лучшие ходы пк

        k = 0
        mi = int(to_ternary(arrayOfMaxIndex(a)[k]))  # переводим лучший ход в индекс матрицы


        print(mi)
        if mi < 10:
            buf = [0, mi]
        else:
            buf = [mi // 10, mi % 10]
            print('index', buf)

        board = bgf.field[buf[0]][buf[1]].getField()
        _, best_move = alpha_beta(board, depth, float('-inf'), float('inf'), False)
        while bgf.field[int(lastMove[0])][int(lastMove[1])].getField()[buf[0]][
            buf[1]] != ' ':  # выбираем свободную ячейку лучшего хода
            k += 1
            mi = int(to_ternary(arrayOfMaxIndex(a)[k]))
            if mi < 10:
                buf = [0, mi]
            else:
                buf = [mi // 10, mi % 10]

        actBoard = bgf.field[lastMove[0]][lastMove[1]].getField()
        print(actBoard)
        for i in range(3):
            for j in range(3):
                if actBoard[i][j] == ' ': countMiss += 1
                if actBoard[i][j] == whoMoveNowBig(bgf):
                    actCount += 1
                    if actCount == 2 and countMiss == 1:
                        print('this board winner G')
                        winFlag = 1
                        #assert('this board was win on G by ', whoMoveNowBig(bgf))


            countMiss = 0
            actCount = 0

        for i in range(3):
            for j in range(3):
                if actBoard[j][i] == ' ': countMiss += 1
                if actBoard[j][i] == whoMoveNowBig(bgf):
                    actCount += 1
                    if actCount == 2:
                        print('this board winner V')
                        winFlag = 1
                        #assert ('this board was win on V by ', whoMoveNowBig(bgf))


            countMiss = 0
            actCount = 0

        bgf.move(lastMove, [buf[0], buf[1]], 'X')
        lastMove = buf
        bgf.printAllField()
        if winFlag == 1:
            break
        a = [checkPosBig(k) for k in [bgf.field[i][j].getField() for i in range(3) for j in range(3)]]
        print(whoMoveNowBig(bgf), " - ", a)
