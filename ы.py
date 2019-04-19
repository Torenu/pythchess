WHITE = 1
BLACK = 2


def opponent(color):
    """Функция для вычисления цвета противника"""
    if color == WHITE:
        return BLACK
    else:
        return WHITE


def print_board(board):
    """Распечатать доску в текстовом виде"""
    print('     +----+----+----+----+----+----+----+----+')
    for row in range(7, -1, -1):
        print(' ', row + 1, end='  ')
        for col in range(8):
            print('|', board.cell(row, col), end=' ')
        print('|')
        print('     +----+----+----+----+----+----+----+----+')
    print(end='        ')
    for col in range(8):
        print(chr(col + 97), end='    ')
    print()


def correct_coords(row, col):
    """Функция проверяет, что координаты (row, col) лежат
    внутри доски"""
    return 0 <= row < 8 and 0 <= col < 8


class Board:
    """Класс шахматной доски"""
    def __init__(self):
        self.color = WHITE
        self.field = []
        for row in range(8):
            self.field.append([None] * 8)
        self.field[0] = [
            Rook(WHITE), Knight(WHITE), Bishop(WHITE), Queen(WHITE),
            King(WHITE), Bishop(WHITE), Knight(WHITE), Rook(WHITE)
        ]
        self.field[1] = [
            Pawn(WHITE), Pawn(WHITE), Pawn(WHITE), Pawn(WHITE),
            Pawn(WHITE), Pawn(WHITE), Pawn(WHITE), Pawn(WHITE)
        ]
        self.field[6] = [
            Pawn(BLACK), Pawn(BLACK), Pawn(BLACK), Pawn(BLACK),
            Pawn(BLACK), Pawn(BLACK), Pawn(BLACK), Pawn(BLACK)
        ]
        self.field[7] = [
            Rook(BLACK), Knight(BLACK), Bishop(BLACK), Queen(BLACK),
            King(BLACK), Bishop(BLACK), Knight(BLACK), Rook(BLACK)
        ]

    def current_player_color(self):
        return self.color

    def cell(self, row, col):
        """Возвращает строку из двух символов. Если в клетке (row, col)
        находится фигура, символы цвета и фигуры. Если клетка пуста,
        то два пробела."""
        piece = self.field[row][col]
        if piece is None:
            return '  '
        color = piece.color
        c = 'w' if color == WHITE else 'b'
        return c + piece.char()

    def get_piece(self, row, col):
        if correct_coords(row, col):
            return self.field[row][col]
        else:
            return None

    def move_piece(self, row, col, row1, col1):
        """Переместить фигуру из точки (row, col) в точку (row1, col1).
        Если перемещение возможно, метод выполнит его и вернёт True.
        Если нет --- вернёт False"""

        piece = self.field[row][col]
        if piece is None:
            return False
        if piece.color != self.color:
            return False
        if piece.can_move(self, row, col, row1, col1):
            self.field[row][col] = None  # Снять фигуру.
            self.field[row1][col1] = piece  # Поставить на новое место.
            self.color = opponent(self.color)
            return True
        return False

    def is_under_attack(self, row, col, color):
        """Проверяет, находится ли фигура под атакой"""
        for y in range(8):
            for x in range(8):
                if self.field[y][x]:
                    if color == self.field[y][x].color:
                        if self.field[y][x].can_move(self, y, x, row, col):
                            return True
        return False


class Piece:
    """Универсальный класс шахматной фигуры, от которого будем наследовать другие классы фигур"""
    def __init__(self, color):
        self.color = color

    def get_color(self):
        return self.color


class Rook(Piece):
    """Класс ладьи"""
    def char(self):
        return 'R'

    def can_move(self, board, row, col, row1, col1):
        if row < 0 or row > 7 or col < 0 or col > 7:
            return False
        elif row == row1 and col == col1:
            return False
        elif row == row1:
            if col > col1:
                a = [board.get_piece(row, i) for i in range(col1 + 1, col)]
            else:
                a = [board.get_piece(row, i) for i in range(col + 1, col1)]
            if all(not i for i in a):
                if not board.get_piece(row1, col1):
                    return True
                if board.get_piece(row1, col1).color == opponent(self.color):
                    return True
        elif col == col1:
            if row > row1:
                a = [board.get_piece(i, col) for i in range(row1 + 1, row)]
            else:
                a = [board.get_piece(i, col) for i in range(row + 1, row1)]
            if all(not i for i in a):
                if not board.get_piece(row1, col1):
                    return True
                if board.get_piece(row1, col1).color == opponent(self.color):
                    return True
        return False


class Pawn(Piece):
    """Класс пешки"""
    def char(self):
        return 'P'

    def can_move(self, board, row, col, row1, col1):
        if row < 0 or row > 7 or col < 0 or col > 7:
            return False
        if self.color == WHITE:
            if col == col1:
                if row == 1 and row1 == 3 and board.get_piece(3, col1) is None and \
                        board.get_piece(2, col1) is None:
                    return True
                if row1 == row + 1 and board.get_piece(row1, col) is None:
                    return True
            if abs(col - col1) == 1 and board.get_piece(row1, col1) and row1 - row == 1:
                if opponent(self.color) == board.get_piece(row1, col1).color:
                    return True
        else:
            if col == col1:
                if row == 6 and row1 == 4 and board.get_piece(4, col1) is None and \
                        board.get_piece(5, col1) is None:
                    return True
                if row == row1 + 1 and board.get_piece(row1, col) is None:
                    return True
            if abs(col - col1) == 1 and board.get_piece(row1, col1) and row - row1 == 1:
                if opponent(self.color) == board.get_piece(row1, col1).color:
                    return True
        return False


class Knight(Piece):
    """Класс коня"""
    def char(self):
        return 'N'

    def can_move(self, board, row, col, row1, col1):
        if row < 0 or row > 7 or col < 0 or col > 7:
            return False
        if sorted([abs(row - row1), abs(col - col1)]) == [1, 2]:
            if board.get_piece(row1, col1) is None:
                return True
            if opponent(self.color) == board.get_piece(row1, col1).color:
                return True
        return False


class King(Piece):
    """Класс короля"""
    def char(self):
        return 'K'

    def can_move(self, board, row, col, row1, col1):
        if row < 0 or row > 7 or col < 0 or col > 7:
            return False
        if row == row1 and col == col1:
            return False
        if abs(row - row1) <= 1 and abs(col - col1) <= 1:
            if board.get_piece(row1, col1) is None:
                oldfield = [[k for k in i] for i in board.field]
                board.field[row][col], board.field[row1][col1] = None, King(self.color)
                if board.is_under_attack(row1, col1, opponent(self.color)):
                    board.field = oldfield
                    return False
                board.field = oldfield
                return True
            if opponent(self.color) == board.get_piece(row1, col1).color:
                oldfield = [[k for k in i] for i in board.field]
                board.field[row][col], board.field[row1][col1] = None, King(self.color)
                if board.is_under_attack(row1, col1, opponent(self.color)):
                    board.field = oldfield
                    return False
                board.field = oldfield
                return True
        return False


class Queen(Piece):
    """Класс ферзя"""
    def char(self):
        return 'Q'

    def can_move(self, board, row, col, row1, col1):
        if row < 0 or row > 7 or col < 0 or col > 7:
            return False
        elif row == row1 and col == col1:
            return False
        elif abs(row - row1) == abs(col - col1):
            xabs = (col1 - col) // abs(col1 - col)
            yabs = (row1 - row) // abs(row1 - row)
            xrange = list(range(col, col1, xabs))[1:]
            yrange = list(range(row, row1, yabs))[1:]
            a = [board.get_piece(yrange[i], xrange[i]) for i in range(len(xrange))]
            if all(not i for i in a):
                if not board.get_piece(row1, col1):
                    return True
                if board.get_piece(row1, col1).color == opponent(self.color):
                    return True
        elif row == row1:
            if col > col1:
                a = [board.get_piece(row, i) for i in range(col1 + 1, col)]
            else:
                a = [board.get_piece(row, i) for i in range(col + 1, col1)]
            if all(not i for i in a):
                if not board.get_piece(row1, col1):
                    return True
                if board.get_piece(row1, col1).color == opponent(self.color):
                    return True
        elif col == col1:
            if row > row1:
                a = [board.get_piece(i, col) for i in range(row1 + 1, row)]
            else:
                a = [board.get_piece(i, col) for i in range(row + 1, row1)]
            if all(not i for i in a):
                if not board.get_piece(row1, col1):
                    return True
                if board.get_piece(row1, col1).color == opponent(self.color):
                    return True
        return False


class Bishop(Piece):
    """Класс слона"""
    def char(self):
        return 'B'

    def can_move(self, board, row, col, row1, col1):
        if row < 0 or row > 7 or col < 0 or col > 7:
            return False
        elif row == row1 and col == col1:
            return False
        elif abs(row - row1) == abs(col - col1):
            xabs = (col1 - col) // abs(col1 - col)
            yabs = (row1 - row) // abs(row1 - row)
            xrange = list(range(col, col1, xabs))[1:]
            yrange = list(range(row, row1, yabs))[1:]
            a = [board.get_piece(yrange[i], xrange[i]) for i in range(len(xrange))]
            if all(not i for i in a):
                if not board.get_piece(row1, col1):
                    return True
                if board.get_piece(row1, col1).color == opponent(self.color):
                    return True
        return False


def main():
    board = Board()
    board.field = [([None] * 8) for _ in range(8)]
    queen = King(BLACK)
    r0, c0 = 4, 5
    board.field[r0][c0] = queen
    board.field[2][5] = Queen(WHITE)

    for row in range(7, -1, -1):
        for col in range(8):
            if queen.can_move(board, r0, c0, row, col):
                print('x', end='')
            else:
                cell = board.cell(row, col)[1]
                cell = cell if cell != ' ' else '-'
                print(cell, end='')
        print()
    print_board(board)

if __name__ == "__main__":
    main()
