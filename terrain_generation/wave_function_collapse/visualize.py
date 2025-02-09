""" """

import math
import time
import pygame as pg
import random as rd
from constants import Size
from tile import Tile


class WFCVisualizer:
    """ """

    def __init__(
        self,
        config: dict,
        grid_dimensions,
        tile_dimensions,
        color_mapping: dict[tuple[int, int, int], str],
        margin_size: int = 20,
    ) -> None:
        """ """
        pg.init()
        self.config = config
        self.screen_size = Size(
            self.config["screen_resolution"][0], self.config["screen_resolution"][1]
        )
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
        y = self.margin_size + row_tile_idx * self.tile_size.height
        x = self.margin_size + col_tile_idx * self.tile_size.width
        return y, x

    def draw_tile(self, cell, y, x):
        """ """
        if cell.tile is None:
            cell_value = cell.superposition_tile[1][1]
        else:
            cell_value = self.color_mapping[cell.tile.value[1][1]]

        cell_rect = pg.Rect(
            x,
            y,
            self.tile_size.width,
            self.tile_size.height,
        )

        pg.draw.rect(self.screen, cell_value, cell_rect)

        """
        for cell_row_idx in range(self.tile_dimensions.height):
            for cell_col_idx in range(self.tile_dimensions.width):
                if cell.tile is None:
                    cell_value = cell.superposition_tile[cell_col_idx][cell_row_idx]
                else:
                    cell_value = self.color_mapping[cell.tile.value[cell_col_idx][cell_row_idx]]

                cell_rect = pg.Rect(
                    x + cell_row_idx * self.cell_size.width,
                    y + cell_col_idx * self.cell_size.height,
                    self.cell_size.width,
                    self.cell_size.height,
                )
                pg.draw.rect(self.screen, cell_value, cell_rect)
        """

    def visualize(self, grid):
        """ """
        pg.font.init()
        font = pg.font.SysFont("Arial", 12)
        self.screen.fill((0, 0, 0))

        for row_tile_idx in range(self.grid_dimensions.height):
            for col_tile_idx in range(self.grid_dimensions.width):
                y_pixel, x_pixel = self._compute_tile_position(row_tile_idx, col_tile_idx)
                tile = grid[row_tile_idx][col_tile_idx]
                self.draw_tile(tile, y_pixel, x_pixel)
                # entropy_value = font.render(
                #     str(len(grid[row_tile_idx][col_tile_idx].options)),
                #     True,
                #     (255, 255, 255),
                # )
                # self.screen.blit(
                #     entropy_value, (x_pixel, y_pixel)
                # )
        # time.sleep(0.1)
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
        key_to_check = Tile((("A", "A", "A"), ("B", "B", "B"), ("C", "C", "C")))

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
        self.draw_tile(key_to_check, x, y)

        # Draw directions.
        for i, direction in enumerate(neighbors[key_to_check].keys()):
            x, y = self._compute_tile_position(i * 2 + (1 / 3), 2)
            text = font.render(direction.capitalize(), True, (0, 0, 0))
            self.screen.blit(text, (y, x))

            for j, neighbor_tile in enumerate(neighbors[key_to_check][direction]):
                x, y = self._compute_tile_position(i * 2, 4 + j)
                try:
                    self.draw_tile(neighbor_tile, x, y)
                except:
                    pass

        pg.display.flip()

        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    break
