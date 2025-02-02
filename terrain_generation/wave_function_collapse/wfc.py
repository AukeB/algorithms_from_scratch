import random as rd
import time
from collections import Counter, defaultdict
from tile import Tile
from cell import Cell
from visualize import WFCVisualizer
from constants import Size, directions

class WaveFunctionCollapse:
    """ """
    def __init__(
        self,
        bitmap: list[list[str]],
        grid_dimensions: Size,
        tile_dimensions: Size,
        color_mapping: dict,
    ) -> None:
        """ """
        self.bitmap = bitmap
        self.bitmap_dimensions = Size(len(self.bitmap[0]), len(self.bitmap))
        self.grid_dimensions = grid_dimensions
        self.tile_dimensions = tile_dimensions
        self.color_mapping = color_mapping
        self._check_tile_and_bitmap_dimensions()
        self.tile_weights, self.all_tiles = self.compute_tiles_and_weights()
        self.tile_set = set(self.tile_weights.keys())
        self.neighbors = self.compute_neighbors()
        self.grid = self.initialize_grid()

        self.wfc_visualizer = WFCVisualizer(
            grid_dimensions=self.grid_dimensions,
            tile_dimensions=tile_dimensions,
            color_mapping=self.color_mapping,
        )

        # #self.wfc_visualizer.show_tiles(self.all_tiles)
        # #self.wfc_visualizer.show_tiles(self.tile_weights)
        # self.wfc_visualizer.show_neighbors(self.neighbors)
        # To do: make a sort of test environment within pygame with buttons
        # something like: self.wfc_visualizer.test_environment()

    def _check_tile_and_bitmap_dimensions(self):
        min_bitmap_dim = min(self.bitmap_dimensions.width, self.bitmap_dimensions.height)
        if (
            self.tile_dimensions.width > min_bitmap_dim
            or self.tile_dimensions.height > min_bitmap_dim
        ):
            raise ValueError(
                f"tile_size ({self.tile_size}) must be smaller than or equal to the "
                f"minimum dimension of the bitmap (width: {self.bitmap_dimensions.width}, "
                f"height: {self.bitmap_dimensions.height})"
            )

    def _extract_tile(self, x, y):
        """ """
        tile = tuple(
            tuple(
                self.bitmap[(y + i) % self.bitmap_dimensions.height][
                    (x + j) % self.bitmap_dimensions.width
                ]
                for j in range(self.tile_dimensions.width)
            )
            for i in range(self.tile_dimensions.height)
        )

        return Tile(tile)

    def compute_tiles_and_weights(self) -> tuple[dict, list[list]]:
        """Computes the weights of unique tiles and stores all tiles in a 2D list."""
        tile_count = Counter()
        total_occurrences = self.bitmap_dimensions.height * self.bitmap_dimensions.width
        all_tiles = []

        for y in range(self.bitmap_dimensions.height):
            for x in range(self.bitmap_dimensions.width):
                tile: Tile = self._extract_tile(x, y)
                tile_count[tile] += 1
                all_tiles.append(tile)
        
        tile_weights = {tile: count / total_occurrences for tile, count in tile_count.items()}
        return tile_weights, all_tiles

    def compute_neighbors(
        self,
    ) -> defaultdict:
        """ """
        neighbors = defaultdict(lambda: defaultdict(set))

        for tile in self.tile_set:
            for other_tile in self.tile_set:
                if tile.up == other_tile.flip_vertically(other_tile.down):
                    neighbors[tile]["up"].add(other_tile)
                if tile.down == other_tile.flip_vertically(other_tile.up):
                    neighbors[tile]["down"].add(other_tile)
                if tile.left == other_tile.flip_horizontally(other_tile.right):
                    neighbors[tile]["left"].add(other_tile)
                if tile.right == other_tile.flip_horizontally(other_tile.left):
                    neighbors[tile]["right"].add(other_tile)

        return neighbors
    
    def initialize_grid(
        self,
    ) -> list[list[str]]:
        """ """
        grid = [
            [Cell(self.tile_set.copy(), self.tile_weights, self.color_mapping) for _ in range(self.grid_dimensions.width)] for _ in range(self.grid_dimensions.height)
        ]
        return grid

    def propagate(
        self,
        y: int,
        x: int,
    ) -> None:
        """ """
        for direction, (dy, dx) in directions.items():
            ny, nx = y + dy, x + dx
            if (
                0 <= nx < self.grid_dimensions.width
                and 0 <= ny < self.grid_dimensions.height
                and self.grid[ny][nx].collapsed == False
            ):
                valid_tiles = self.neighbors.get(self.grid[y][x].tile, {}).get(direction, set())
                self.grid[ny][nx].options &= valid_tiles
                self.grid[ny][nx].compute_superposition_tile(
                    tile_weights=self.tile_weights,
                    color_mapping=self.color_mapping,
                )
                
                if len(self.grid[ny][nx].options) == 0:
                    self.wfc_visualizer.visualize(self.grid)
                    time.sleep(50)
    
    def collapse_cell(
        self,
        y: int,
        x: int,
        tile: tuple
    ) -> None:
        """ """
        self.grid[y][x].options = []
        self.grid[y][x].collapsed = True
        self.grid[y][x].tile = tile
        self.grid[y][x].superposition_tile = None

    def collapse_grid(
        self,
    ) -> None:
        """ """
        while True:
            min_entropy = float("inf")
            min_cells = []

            for cell_y in range(self.grid_dimensions.width):
                for cell_x in range(self.grid_dimensions.height):
                    if not self.grid[cell_y][cell_x].collapsed:
                        options = self.grid[cell_y][cell_x].options
                        if len(options) < min_entropy:
                            min_entropy = len(options)
                            min_cells = [(cell_y, cell_x)]
                        elif len(options) == min_entropy:
                            min_cells.append((cell_y, cell_x))

            if not min_cells:
                time.sleep(3)
                break

            min_cell = rd.choice(min_cells)

            # Collapse the wave function
            y, x = min_cell
            choices = list(self.grid[y][x].options)
            weights = [self.tile_weights[tile] for tile in choices]
            chosen_tile = rd.choices(choices, weights)[0]
            self.collapse_cell(y, x, chosen_tile)
            self.propagate(y, x)

            self.wfc_visualizer.visualize(self.grid)
