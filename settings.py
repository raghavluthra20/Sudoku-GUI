WIDTH = 600
HEIGHT = 600
CELLSIZE = 50
GRIDPOS = [75, 100]
GRIDSIZE = CELLSIZE * 9 + 9

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 50, 0)
GREEN = (0, 255, 0)
LIGHTBLUE = (96, 216, 232)
LOCKEDCELLCOLOR = (189, 189, 189)
GREY = (130, 130, 130)

BOARD1 = [[0 for i in range(9)] for i in range(9)]
BOARD2 = [
    [0, 0, 0, 2, 6, 0, 0, 0, 1],
    [6, 8, 0, 0, 7, 0, 0, 9, 0],
    [1, 9, 0, 0, 0, 4, 5, 0, 0],
    [8, 2, 0, 0, 0, 0, 0, 4, 0],
    [0, 0, 4, 6, 0, 2, 9, 0, 0],
    [0, 5, 0, 0, 0, 3, 0, 2, 8],
    [0, 0, 0, 3, 0, 0, 0, 7, 4],
    [0, 4, 0, 0, 5, 0, 0, 3, 6],
    [7, 0, 3, 0, 1, 8, 0, 0, 0]
]
BOARD = BOARD2
