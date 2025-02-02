""" """

import math
import pygame as pg
import random as rd
from constants import Size, screen_resolution
from tile import Tile


class WFCVisualizer:
    """ """

    def __init__(
        self,
        grid_dimensions,
        tile_dimensions,
        color_mapping: dict[tuple[int, int, int], str],
        screen_resolution: tuple[int, int] = screen_resolution,
        margin_size: int = 20,
    ) -> None:
        """ """
        pg.init()

        self.screen_size = Size(screen_resolution[0], screen_resolution[1])
        self.grid_dimensions = grid_dimensions
        self.tile_dimensions = tile_dimensions
        self.margin_size = margin_size
        self.color_mapping = {v: k for k, v in color_mapping.items()}
        self.tile_size, self.cell_size = self._compute_tile_and_cell_size()

        self.screen = pg.display.set_mode((self.screen_size.width, self.screen_size.height))

    def _compute_tile_and_cell_size(
        self,
        inner_margin: int = 0,
        square_grid: bool = True,
    ) -> tuple[int, int]:
        """ """
        tile_size = Size(
            int((self.screen_size.height - 2 * self.margin_size) / self.grid_dimensions.height)
            if square_grid
            else int((self.screen_size.width - 2 * self.margin_size) / self.grid_dimensions.width),
            int((self.screen_size.height - 2 * self.margin_size) / self.grid_dimensions.height),
        )

        cell_size = Size(
            int((tile_size.width - inner_margin) / self.tile_dimensions.width),
            int((tile_size.height - inner_margin) / self.tile_dimensions.height),
        )

        return tile_size, cell_size

    def _compute_tile_position(self, row_tile_idx, col_tile_idx):
        x = self.margin_size + col_tile_idx * self.tile_size.width
        y = self.margin_size + row_tile_idx * self.tile_size.height
        return x, y

    def _draw_tile(self, tile, x, y):
        if tile is None:
            # Todo: Handle cells in superposition: Add the entropy grid as function argument and take average of rgb values.
            pass
        else:
            for cell_row_idx in range(self.tile_dimensions.height):
                for cell_col_idx in range(self.tile_dimensions.width):
                    cell_value = self.color_mapping[tile.value[cell_col_idx][cell_row_idx]]
                    cell_rect = pg.Rect(
                        x + cell_row_idx * self.cell_size.width,
                        y + cell_col_idx * self.cell_size.height,
                        self.cell_size.width,
                        self.cell_size.height,
                    )
                    pg.draw.rect(self.screen, cell_value, cell_rect)

    def visualize(self, grid, entropy_grid):
        """ """
        pg.font.init()
        font = pg.font.SysFont("Arial", 12)
        self.screen.fill((0, 0, 0))

        for row_tile_idx in range(self.grid_dimensions.height):
            for col_tile_idx in range(self.grid_dimensions.width):
                x, y = self._compute_tile_position(row_tile_idx, col_tile_idx)
                tile_value = grid[row_tile_idx][col_tile_idx]
                self._draw_tile(tile_value, x, y)
                entropy_value = font.render(
                    str(len(entropy_grid[row_tile_idx][col_tile_idx])),
                    True,
                    (255, 255, 255),
                )
                self.screen.blit(
                    entropy_value, (x, y)
                )  # Todo: clear screen when entropy_value has changed for (x, y)

        pg.display.flip()
    
    def test_visualize(self, grid, cell_size=30):
        # Define the window size based on grid size and cell size
        rows = len(grid)
        cols = len(grid[0])
        width = cols * cell_size
        height = rows * cell_size

        # Create the screen
        self.screen.fill((255, 255, 255))  # Fill the screen with white color

        # Draw the grid
        for y, row in enumerate(grid):
            for x, cell in enumerate(row):
                color = self.color_mapping.get(cell, (255, 255, 255))  # Default to white if not found
                pg.draw.rect(self.screen, color, (x * cell_size, y * cell_size, cell_size, cell_size))

        # Update the display
        pg.display.flip()

    def show_tiles(self, tiles):
        # todo: show tile weight next to or in the tile.
        if isinstance(tiles, dict):
            tiles = list(tiles.keys())

        next_square_number = math.ceil(math.sqrt(len(tiles)))
        self.grid_dimensions = Size(next_square_number, next_square_number)
        self.tile_size, self.cell_size = self._compute_tile_and_cell_size(inner_margin=3)

        for row_tile_idx in range(self.grid_dimensions.height):
            for col_tile_idx in range(self.grid_dimensions.width):
                x, y = self._compute_tile_position(row_tile_idx, col_tile_idx)
                index = row_tile_idx * self.grid_dimensions.height + col_tile_idx
                tile_value = tiles[index] if index < len(tiles) else None
                self._draw_tile(tile_value, x, y)

        pg.display.flip()

        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    break

    def show_neighbors(
        self,
        neighbors: dict,
    ) -> None:
        """ """
        pg.font.init()
        font = pg.font.SysFont("Arial", 36)
        grid_height = 7

        self.screen.fill((255, 255, 255))

        key_to_check = rd.choice(list(neighbors.keys()))
        key_to_check = Tile((('A', 'A', 'A'), ('B', 'B', 'B'), ('C', 'C', 'C')))

        grid_height = max(
            (len(value) for value in neighbors[key_to_check].values() if len(value) > grid_height),
            default=grid_height,
        )
        self.grid_dimensions = Size(
            self.screen_size.width // (self.screen_size.height // grid_height),
            grid_height,
        )
        self.tile_size, self.cell_size = self._compute_tile_and_cell_size(inner_margin=3)

        # Draw center tile.
        x, y = self._compute_tile_position((self.grid_dimensions.height - 1) / 2, 0)
        self._draw_tile(key_to_check, x, y)

        # Draw directions.
        for i, direction in enumerate(neighbors[key_to_check].keys()):
            x, y = self._compute_tile_position(i * 2 + (1 / 3), 2)
            text = font.render(direction.capitalize(), True, (0, 0, 0))
            self.screen.blit(text, (x, y))

            for j, neighbor_tile in enumerate(neighbors[key_to_check][direction]):
                x, y = self._compute_tile_position(i * 2, 4 + j)
                try:
                    self._draw_tile(neighbor_tile, x, y)
                except:
                    pass

        pg.display.flip()

        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    break
