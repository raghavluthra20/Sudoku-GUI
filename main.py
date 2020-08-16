import pygame
import time
import sys
from settings import *
from grid import *

pygame.init()


class Game:
    def __init__(self, width, height, bo):
        self.window=pygame.display.set_mode((width, height))
        pygame.display.set_caption("Sudoku")
        self.width=width
        self.height=height
        self.board=bo
        self.running=True
        self.grid=Grid(9, 9, self)
        self.selected=None
        self.mousePos=None
        self.playing=True
        self.cross=1

    def run(self):
        self.events()
        self.update()
        self.draw()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running=False
            # Selection
            if event.type == pygame.MOUSEBUTTONDOWN:
                selected=self.mouseOnGrid()
                if selected:
                    self.selected=selected
                else:
                    self.selected=False
                # print(self.selected)
            if event.type == pygame.KEYDOWN:
                # Auto solve
                if event.key == pygame.K_SPACE:
                    self.playing=False
                    self.grid.reset()
                    self.grid.solve_grid(self.grid.board)
                    pygame.time.wait(250)
                    self.grid.reset()
                # User presses a number
                if self.selected:
                    pos=[self.selected[1], self.selected[0]]
                    cube=self.grid.cube_list[pos[0]][pos[1]]
                    if self.isInt(event.unicode):
                        cube.font_color=GREY
                        cube.value=int(event.unicode)
                    if event.key == pygame.K_RETURN:
                        if self.valid(cube.value, pos):
                            cube.font_color=BLACK
                        else:
                            cube.value=0
                            self.cross += 1
                            self.draw_cross()

    def update(self):
        self.mousePos=pygame.mouse.get_pos()
        self.grid.update()
        if self.selected == False:
            self.grid.reset_sel()

        # Cell Selection
        for ridx, row in enumerate(self.grid.cube_list):
            for cidx, cube in enumerate(row):
                if self.selected:
                    if ridx == self.selected[1] and cidx == self.selected[0]:
                        self.grid.cube_list[ridx][cidx].selected=True
                    else:
                        self.grid.cube_list[ridx][cidx].selected=False

    def draw(self):
        self.window.fill(WHITE)
        self.shadeLockedCells()
        self.grid.draw_grid()
        self.draw_lines()

        pygame.display.update()

    # Helper Functions

    def draw_lines(self):
        for x, y in enumerate(range(10)):
            if x % 3 != 0:   # y%3 will also != 0 when this is true
                pygame.draw.line(self.window, BLACK, (x*CELLSIZE + GRIDPOS[0], GRIDPOS[1]), (GRIDPOS[0] + x*CELLSIZE, GRIDPOS[1] + 450))
                pygame.draw.line(self.window, BLACK, (GRIDPOS[0], y*CELLSIZE + GRIDPOS[1]), (GRIDPOS[0] + 450, y*CELLSIZE + GRIDPOS[1]))
            else:
                pygame.draw.line(self.window, BLACK, (x*CELLSIZE + GRIDPOS[0], GRIDPOS[1]), (GRIDPOS[0] + x*CELLSIZE, GRIDPOS[1] + 450), 2)
                pygame.draw.line(self.window, BLACK, (GRIDPOS[0], y*CELLSIZE + GRIDPOS[1]), (GRIDPOS[0] + 450, y*CELLSIZE + GRIDPOS[1]), 2)

    def mouseOnGrid(self):
        if GRIDPOS[0] < self.mousePos[0] < GRIDPOS[0] + GRIDSIZE:
            if GRIDPOS[1] < self.mousePos[1] < GRIDPOS[1] + GRIDSIZE:
                coords=((self.mousePos[0] - GRIDPOS[0]) // CELLSIZE, (self.mousePos[1] - GRIDPOS[1]) // CELLSIZE)
                if self.grid.cube_list[coords[1]][coords[0]] not in self.grid.lockedCells:
                    return coords
        return False

    def shadeLockedCells(self):
        for cube in self.grid.lockedCells:
            cube.drawSelection(self.window, [cube.row_id, cube.col_id], color=LOCKEDCELLCOLOR)

    def isInt(self, val):
        try:
            int(val)
            return True
        except:
            return False

    def valid(self, val, pos):
        # row
        for col, cube in enumerate(self.grid.cube_list[pos[0]]):
            if cube.value == val and col != pos[1] and cube.value != 0:
                return False
        # col
        for row in range(len(self.grid.cube_list)):
            if self.grid.cube_list[row][pos[1]].value == val and pos[0] != row and self.grid.cube_list[row][pos[1]].value != 0:
                return False
        # box
        box_x = pos[1] // 3
        box_y = pos[0] // 3
        for i in range(box_y*3, box_y*3 + 3):
            for j in range(box_x*3, box_x*3 + 3):
                if self.grid.cube_list[i][j].value == val and i != pos[0] and j != pos[1] and self.grid.cube_list[i][j].value != 0:
                    return False
        return True

    def draw_cross(self):
        pass


g=Game(HEIGHT, WIDTH, BOARD)

while g.running:
    g.run()

pygame.quit()
sys.exit()
