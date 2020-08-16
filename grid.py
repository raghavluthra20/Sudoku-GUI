import pygame
import time
from settings import *
import solver

pygame.init()

clock = pygame.time.Clock()


class Grid:
    def __init__(self, rows, cols, game):
        self.rows = rows
        self.cols = cols
        self.game = game
        self.board = self.game.board
        self.lockedCells = []
        self.cube_list = [[Cube(i, j, CELLSIZE, CELLSIZE, self.game, self) for i in range(self.rows)] for j in range(self.cols)]
        for row in self.cube_list:
            for cube in row:
                if cube.value != 0:
                    self.lockedCells.append(cube)

    def draw_grid(self):
        for row in self.cube_list:
            for cube in row:
                cube.draw(self.game.window)

    def update(self):   # called in main update
        for row in self.cube_list:
            for cube in row:
                cube.update()

    def solve_grid(self, bo):
        self.game.draw()
        self.board = bo
        find = solver.find_empty(bo)
        if not find:
            return True
        else:
            row, col = find

        for i in range(1, 10):
            clock.tick(90)
            # Updating Screen
            self.board = bo
            self.game.draw()
            self.game.update()
            if solver.valid(bo, i, (row, col)):
                bo[row][col] = i
                self.cube_list[row][col].border = True
                self.cube_list[row][col].border_col = GREEN

                if self.solve_grid(bo):
                    return True

                bo[row][col] = 0    # backtrack
                self.cube_list[find[0]][find[1]].border = True
                self.cube_list[row][col].border_col = RED
                self.board = bo

        return False

    def reset(self):
        for row in self.cube_list:
            for cube in row:
                cube.selected = False
                cube.user_val = None
                cube.border = False
        self.game.selected = False

    def reset_sel(self):
        for row in self.cube_list:
            for cube in row:
                cube.selected = False


class Cube:
    def __init__(self, row, col, width, height, game, grid):
        self.row_id = row
        self.col_id = col
        self.width = width
        self.height = height
        self.grid = grid
        self.highlighted = False
        self.game = game
        self.image = pygame.Surface((width, height))
        self.rect = self.image.get_rect()
        self.font = pygame.font.SysFont("arial", CELLSIZE//2)
        self.value = self.grid.board[self.col_id][self.row_id]
        self.user_val = None
        self.selected = False
        self.border = False
        self.border_col = GREEN
        self.font_color = GREY

    def draw(self, window):
        # pygame.draw.rect(window, color, self.rect, 1)
        # Border
        if self.border:
            self.drawSelection(window, (self.row_id, self.col_id), border=3, color=self.border_col)
        # Selection
        if self.selected and self.game.playing:
            self.image.fill(LIGHTBLUE)
            window.blit(self.image, self.rect)
        # Highlight when hover
        if self.highlighted and self.game.playing:
            self.drawSelection(window, (self.row_id, self.col_id), border=4)
        # drawing cell value
        if self.game.playing:
            if self.value != 0:
                if self in self.grid.lockedCells:
                    self.draw_text(window, str(self.value), [self.rect.x, self.rect.y], BLACK)
                else:
                    self.draw_text(window, str(self.value), [self.rect.x, self.rect.y], self.font_color)
        else:
            if self.value != 0:
                self.draw_text(window, str(self.value), [self.rect.x, self.rect.y], BLACK)

    def update(self):
        # when auto solve, change values to original
        if not self.game.playing:
            self.value = self.grid.board[self.col_id][self.row_id]
        self.rect.topleft = (self.row_id * CELLSIZE + GRIDPOS[0], self.col_id * CELLSIZE + GRIDPOS[1])
        # Highlight
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos) and self not in self.game.grid.lockedCells:
            self.highlighted = True
        else:
            self.highlighted = False

    def drawSelection(self, window, pos, border=0, color=LIGHTBLUE):
        """helper function for highlighting cells when hover over them
        """
        rect = (pos[0]*CELLSIZE + GRIDPOS[0], pos[1]*CELLSIZE + GRIDPOS[1], CELLSIZE, CELLSIZE)
        pygame.draw.rect(window, color, rect, border)

    def draw_text(self, window, text, pos, color):
        font = self.font.render(text, True, color)
        fontWidth = font.get_width()
        fontHeight = font.get_height()
        pos[0] += (CELLSIZE - fontWidth) // 2
        pos[1] += (CELLSIZE - fontHeight) // 2
        window.blit(font, pos)
