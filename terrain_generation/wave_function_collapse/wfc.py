import random as rd
import copy
import time
from collections import Counter, defaultdict
from tile import Tile
from visualize import WFCVisualizer
from constants import Size


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
        self.grid = [
            [None for _ in range(grid_dimensions.width)] for _ in range(grid_dimensions.height)
        ]
        self._check_tile_and_bitmap_dimensions()
        self.tile_weights = self.compute_tile_weights()
        self.tile_set = set(self.tile_weights.keys())
        self.adjacency = self.compute_neighbors()
        self.entropy_grid = self.initialize_entropy()

        self.directions = {
            "up": (-1, 0),
            "down": (1, 0),
            "left": (0, -1),
            "right": (0, 1),
        }

        self.wfc_visualizer = WFCVisualizer(
            grid_dimensions=self.grid_dimensions,
            tile_dimensions=tile_dimensions,
            color_mapping=color_mapping,
        )

        # self.wfc_visualizer.show_unique_tiles(self.tile_weights)
        # self.wfc_visualizer.show_adjacency(self.adjacency)

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

    def compute_tile_weights(
        self,
    ) -> None:
        """ """
        tile_count = Counter()
        total_occurrences = self.bitmap_dimensions.height * self.bitmap_dimensions.width

        for y in range(self.bitmap_dimensions.height):
            for x in range(self.bitmap_dimensions.width):
                tile: Tile = self._extract_tile(x, y)
                tile_count[tile] += 1

        tile_weights = {tile: count / total_occurrences for tile, count in tile_count.items()}
        return tile_weights

    def compute_neighbors(
        self,
    ) -> defaultdict:
        """ """
        adjacency = defaultdict(lambda: defaultdict(set))

        for tile in self.tile_set:
            for other_tile in self.tile_set:
                if tile.up == other_tile.down:
                    adjacency[tile]["up"].add(other_tile)
                if tile.down == other_tile.up:
                    adjacency[tile]["down"].add(other_tile)
                if tile.left == other_tile.right:
                    adjacency[tile]["left"].add(other_tile)
                if tile.right == other_tile.left:
                    adjacency[tile]["right"].add(other_tile)

        return adjacency

    def initialize_entropy(
        self,
    ) -> list[list[str]]:
        """ """
        # Initially, every tile is in a superposition of all posssible tile values.
        entropy = [
            [copy.deepcopy(self.tile_set) for _ in range(self.grid_dimensions.width)]
            for _ in range(self.grid_dimensions.height)
        ]
        return entropy

    def propagate(
        self,
        y: int,
        x: int,
        tile: str,
    ) -> None:
        """ """
        for direction, (dy, dx) in self.directions.items():
            ny, nx = y + dy, x + dx
            if (
                0 <= nx < self.grid_dimensions.width
                and 0 <= ny < self.grid_dimensions.height
                and self.grid[ny][nx] is None
            ):
                valid_tiles = self.adjacency.get(tile, {}).get(direction, set())
                self.entropy_grid[ny][nx] &= valid_tiles
                if len(self.entropy_grid[ny][nx]) == 0:
                    self.wfc_visualizer.visualize(self.grid, self.entropy_grid)
                    time.sleep(50)

    def collapse(
        self,
    ) -> None:
        """ """
        while True:
            min_entropy = float("inf")
            min_cell = None

            for y in range(self.grid_dimensions.width):
                for x in range(self.grid_dimensions.height):
                    if self.grid[y][x] is None:
                        options = self.entropy_grid[y][x]

                        if len(options) < min_entropy:
                            min_entropy = len(options)
                            min_cell = (y, x)

            if min_cell is None:  # Necessary?
                break

            # Collapse the wave function
            y, x = min_cell
            choices = list(self.entropy_grid[y][x])
            weights = [self.tile_weights[tile] for tile in choices]
            chosen_tile = rd.choices(choices, weights)[0]
            self.grid[y][x] = chosen_tile
            self.propagate(y, x, chosen_tile)

            self.wfc_visualizer.visualize(self.grid, self.entropy_grid)
            # time.sleep(0.2)
