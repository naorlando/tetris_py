import pygame
import random
from constants import SCREEN_RESOLUTION, COLORS, BLOCKS,BACKGROUND_COLORS



class World:
    """Class that defines the world in which the agents will live.
    The world size is 300x600 by default and contains 20 rows by 10 colomns with a cell size of 30.
    """

    def __init__(self) -> None:
        self.rows = 20
        self.columns = 10
        self.cell_size = 30
        self.size = (self.columns * self.cell_size, self.rows * self.cell_size)

        self.grid = [[0 for _ in range(self.columns)] for _ in range(self.rows)]
        self.block_offset = [int(self.columns / 2 - 1), 0]
        self.grid[-1] = [1 for _ in range(self.columns)]
        self.grid[-1][0] = 0
        
        self.block = self.generate_block()
        self.next_block = self.generate_block()
    
    def move (self, x: int, y: int) -> None:
        """Method that moves the block in the grid.
        """
        self.block_offset[0] += x
        if self.detect_collision():
            self.block_offset[0] -= x

        self.block_offset[1] += y
        if self.detect_collision():
            self.block_offset[1] -= y
            self.fix_block()
            self.clear_rows()

            self.new_block()

    def fix_block (self) -> None:
        """Method that fixes the block in the grid when it reachs the bottom.
        """
        for i,block_row in enumerate(self.block):
            for j,block_element in enumerate(block_row):
                if block_element != 0:
                    self.grid[self.block_offset[1] + i][self.block_offset[0] + j] = block_element
        self.block_offset = [int(self.columns / 2 - 1), 0]
        
    def clear_rows (self) -> None:
        """Method that clears the rows that are full.
        """
        for i,row in enumerate(self.grid):
            if all(row):
                self.grid.pop(i)
                self.grid.insert(0, [0 for _ in range(self.columns)])

    def rotate (self) -> None:
        """Method that rotates the block in the grid.
        """
        before_state = self.block
        self.block = list(zip(*self.block[::-1]))
        if self.detect_collision():
            self.block = before_state

    def detect_collision (self) -> bool:
        #detect end of screen
        if self.block_offset[0] < 0 or self.block_offset[0] + len(self.block[0]) > self.columns:
            return True
        #Vertical collision
        if self.block_offset[1] + len(self.block) > self.rows:
            return True
        #Block collision
        for i,block_row in enumerate(self.block):
            for j,block_element in enumerate(block_row):
                if block_element != 0:
                    if self.grid[self.block_offset[1] + i][self.block_offset[0] + j] != 0:
                        return True
    
    def generate_block(self):
        """Genera un nuevo bloque con un color aleatorio."""
        block = random.choice(BLOCKS)
        color_index = random.randint(1, len(COLORS) - 1)
        return [[color_index if cell != 0 else 0 for cell in row] for row in block]

    def new_block(self):
        """Actualiza el bloque actual con el próximo bloque y genera un nuevo próximo bloque."""
        self.block = self.next_block
        self.next_block = self.generate_block()
        self.block_offset = [int(self.columns / 2 - 1), 0]


    def draw (self, screen: pygame.Surface) -> None:
        """Method that draws the grid on the middle of the screen.
        """
        for i in range(self.rows):
            for j in range(self.columns):
                pos = (
                    j * self.cell_size + SCREEN_RESOLUTION[0] / 2 - self.size[0] / 2,
                    i * self.cell_size + SCREEN_RESOLUTION[1] / 2 - self.size[1] / 2,
                    self.cell_size,
                    self.cell_size,
                    )
                pygame.draw.rect(
                    screen, 
                    COLORS[self.grid[i][j]], 
                    pos, 
                    1 if self.grid[i][j] == 0 else 0,
                )
        
        #Draw current block 
        for i,block_row in enumerate(self.block):
            for j,block_element in enumerate(block_row):
                pos = (
                    j * self.cell_size + SCREEN_RESOLUTION[0] / 2 - self.size[0] / 2 + self.block_offset[0] * self.cell_size,
                    i * self.cell_size + SCREEN_RESOLUTION[1] / 2 - self.size[1] / 2 + self.block_offset[1] * self.cell_size,
                    self.cell_size,
                    self.cell_size,
                    )
                if block_element != 0:
                    pygame.draw.rect(
                        screen, 
                        COLORS[block_element], 
                        pos, 
                        0,
                    )

        #Draw next block on the top right
        next_block_offset = [self.columns + 2, 2]
        for i,block_row in enumerate(self.next_block):
            for j,block_element in enumerate(block_row):
                pos = (
                    j * self.cell_size + SCREEN_RESOLUTION[0] / 2 - self.size[0] / 2 + next_block_offset[0] * self.cell_size,
                    i * self.cell_size + SCREEN_RESOLUTION[1] / 2 - self.size[1] / 2 + next_block_offset[1] * self.cell_size,
                    self.cell_size,
                    self.cell_size,
                    )
                if block_element != 0:
                    pygame.draw.rect(
                        screen, 
                        COLORS[block_element], 
                        pos, 
                        0,
                    )
