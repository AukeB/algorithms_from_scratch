""" """

import random as rd
import math
from constants import Size


class DiamondSquare:
    """ """

    def __init__(
        self,
        grid_dimensions: Size,
        h: float,
    ) -> None:
        self.grid_dimensions = grid_dimensions
        self.h = h
        self.corner_names = ["top_left", "top_right", "bottom_left", "bottom_right"]
        self.diamond_directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        self.square_directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        self.grid = [
            [None for _ in range(grid_dimensions.width)] for _ in range(grid_dimensions.height)
        ]

        self.corner_values = self.determine_corner_values(mode="one_value", value=10)

    def determine_corner_values(self, mode: str, value: int) -> dict[str, float]:
        """ """
        if mode == "one_value":
            if not isinstance(value, (int, float)):
                raise TypeError(
                    f"Expected 'value' to be of type int or float when mode is 'one_value', but got {type(value).__name__}."
                )
            return {key: value for key in self.corner_names}

    def initialise_corners(
        self,
    ) -> None:
        """ """
        if not self.corner_values:
            raise ValueError("Corners can not be initialised. Corners values have not been set yet")

        self.grid[0][0] = self.corner_values[self.corner_names[0]]
        self.grid[0][-1] = self.corner_values[self.corner_names[1]]
        self.grid[-1][0] = self.corner_values[self.corner_names[2]]
        self.grid[-1][-1] = self.corner_values[self.corner_names[3]]

    def exists_grid_element(
        self,
        x: int,
        y: int,
    ) -> bool:
        """ """
        exists = 0 <= y < self.grid_dimensions.height and 0 <= x < self.grid_dimensions.width
        return exists

    def are_grid_elements_not_none(self, list_of_tuples):
        """ """
        return all(self.grid[y][x] is not None for x, y in list_of_tuples)

    def find_valid_directions(self, x: int, y: int, directions: list[tuple[int, int]]) -> bool:
        """ """
        valid_directions = []

        for dx, dy in self.diamond_directions:
            if self.exists_grid_element(x=x + dx, y=y + dy):
                valid_directions.append((dx, dy))

        return valid_directions

    def determine_if_midpoint(
        self,
        x: int,
        y: int,
        directions,
    ) -> bool:
        """ """
        valid_directions = self.find_valid_directions(x, y, directions)

        neighbor_coordinates = [
            (x + x_direction, y + y_direction) for (x_direction, y_direction) in valid_directions
        ]

        if self.are_grid_elements_not_none(neighbor_coordinates):
            return neighbor_coordinates

        while not self.are_grid_elements_not_none(neighbor_coordinates):
            neighbor_coordinates = [
                (
                    neighbor_coordinates[index][0] + x_direction,
                    neighbor_coordinates[index][1] + y_direction,
                )
                for index, (x_direction, y_direction) in enumerate(valid_directions)
            ]
            for y, x in neighbor_coordinates:
                if self.exists_grid_element(x, y):
                    return False

            if self.are_grid_elements_not_none(neighbor_coordinates):
                return neighbor_coordinates

        # neighbor_found = False

        # for x_direction, y_direction in directions:
        #     x_new, y_new = x + x_direction, y + y_direction
        #     if not self.exists_grid_element(x_new, y_new):
        #         continue

        #     neighbor_found = False
        #     while self.exists_grid_element(x_new, y_new):
        #         if self.grid[y_new][x_new]:
        #             neighbor_found = True

        #         x_new, y_new = x_new + x_direction, y_new + y_direction

        #     if not neighbor_found:
        #         break

        # return neighbor_found
        return False

    def obtain_coordinate_pairs(
        self,
        step_name: str,
    ) -> set[tuple[int, int]]:
        """ """
        if step_name not in ["diamond", "square"]:
            raise ValueError(f"Invalid step_name '{step_name}'. Expected 'diamond' or 'square'.")

        coordinates = set()
        directions = self.diamond_directions if step_name == "diamond" else self.square_directions

        for y in range(self.grid_dimensions.height):
            for x in range(self.grid_dimensions.width):
                if self.grid[y][x] is not None:
                    continue

                if self.determine_if_midpoint(x, y, directions):
                    coordinates.add((x, y))

        return coordinates

    def set_values(self, midpoint_coordinates_and_values: dict[tuple, float]) -> None:
        for midpoint_coordinates, midpoint_value in midpoint_coordinates_and_values.items():
            x, y = midpoint_coordinates[0], midpoint_coordinates[1]
            self.grid[x][y] = midpoint_value + self.obtain_random_value()

    def obtain_random_value(
        self,
        iteration: int = 1,
    ) -> float:
        """
        Generate a random value adjusted by a scale constant that decreases with each iteration.

        Args:
            iteration (int): The current iteration number.

        Returns:
            float: A random value scaled by the factor 2^(-iteration * h).
        """
        if not (0.0 <= self.h <= 1.0):
            raise ValueError("Parameter 'h' must be between 0.0 and 1.0.")

        random_value = rd.uniform(-1, 1)
        scale_constant = math.pow(2, -iteration * self.h)
        return random_value * scale_constant

    def perform_diamond_step(
        self,
    ) -> None:
        """ """
        self.obtain_coordinate_pairs(step_name="diamond")

    def execute(
        self,
    ):
        """ """
        self.initialise_corners()

        for row in self.grid:
            print(row)

        self.perform_diamond_step()
        # print()

        # for row in self.grid:
        #     print(row)

        # self.perform_square_step()
