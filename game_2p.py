from chess_engine import *
from graphics import *

# Управление:
# Левая кнопка мыши - выбрать первую клетку хода
# Правая кнопка мыши - выбрать вторую клетку хода
# Средняя кнопка мыши - Выполнить ход


def draw_pieces(image_field):
    for x in range(8):
        for y in range(8):
            if board.field[y][x]:
                image_field[y][x] = Image(Point(x * 100 + 50, 700 - y * 100 + 50), board.cell(y, x) + '.png')
                image_field[y][x].draw(win)


def undraw_pieces(image_field):
    for x in range(8):
        for y in range(8):
            if image_field[y][x]:
                image_field[y][x].undraw()


def firstpoint(event):
    if event.y < 800 and event.x < 800:
        current_move[0][0] = 7 - event.y // 100
        current_move[0][1] = event.x // 100
    a = '-'
    if current_move[0] != [-1, -1]:
        a = chr(current_move[0][1] + 97) + str(current_move[0][0] + 1) + a
    if current_move[1] != [-1, -1]:
        a = a + chr(current_move[1][1] + 97)+ str(current_move[1][0] + 1)
    txt[4].setText(a)


def secondpoint(event):
    current_move[1][0] = 7 - event.y // 100
    current_move[1][1] = event.x // 100
    a = '-'
    if current_move[0] != [-1, -1]:
        a = chr(current_move[0][1] + 97) + str(current_move[0][0] + 1) + a
    if current_move[1] != [-1, -1]:
        a = a + chr(current_move[1][1] + 97)+ str(current_move[1][0] + 1)
    txt[4].setText(a)


def chess_move(event):
    txt[2].undraw()
    if board.move_piece(*current_move[0], *current_move[1]):
        txt[2].undraw()
        undraw_pieces(image_field)
        draw_pieces(image_field)
        txt[opponent(board.color) - 1].undraw()
        txt[board.color - 1].draw(win)
        current_move.pop(0)
        current_move.pop(0)
        current_move.append([-1, -1])
        current_move.append([-1, -1])
        txt[4].setText('-')
    else:
        txt[2].draw(win)
    if not board.check_mate():
        win.unbind('<Button-1>')
        win.unbind('<Button-2>')
        win.unbind('<Button-3>')
        for i in txt:
            i.undraw()
        if board.color == WHITE:
            txt[5].draw(win)
        else:
            txt[6].draw(win)


board = Board()

win = GraphWin('Шахматы v1.0', 1100, 850)

for x in range(8):
    for y in range(8):
        rect = Rectangle(Point(x * 100, y * 100), Point(x * 100 + 100, y * 100 + 100))
        if (x + y) % 2 == 0:
            rect.setFill(color_rgb(181, 136, 99))
        else:
            rect.setFill(color_rgb(240, 217, 181))
        rect.draw(win)

txt = []

for i in range(7, -1, -1):
    txt.append(Text(Point(810, 100 * i + 50), i + 1))

for i in range(8):
    txt.append(Text(Point(100 * i + 50, 812), chr(i + 97)))

for i in txt:
    i.draw(win)

txt = []

txt.append(Text(Point(950, 50), 'Ход белых'))
txt[0].setSize(20)
txt[0].draw(win)

txt.append(Text(Point(950, 50), 'Ход чёрных'))
txt[1].setSize(20)

txt.append(Text(Point(950, 800), 'Некорректный ход!'))
txt[2].setTextColor('red')
txt[2].setSize(20)

txt.append(Text(Point(950, 200), 'Текущий ход:'))
txt[3].setSize(20)
txt[3].draw(win)

txt.append(Text(Point(950, 250), '-'))
txt[4].setSize(20)
txt[4].draw(win)

txt.append(Text(Point(950, 400), 'Игра окончена,\nпобедили чёрные'))
txt[5].setSize(25)

txt.append(Text(Point(950, 400), 'Игра окончена,\nпобедили белые'))
txt[6].setSize(25)

image_field = [([None] * 8) for i in range(8)]

draw_pieces(image_field)

current_move = [[-1, -1], [-1, -1]]

win.bind('<Button-1>', firstpoint)
win.bind('<Button-2>', chess_move)
win.bind('<Button-3>', secondpoint)

win.getMouse()
win.close()
