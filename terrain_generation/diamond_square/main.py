""" """

from diamond_square import DiamondSquare
from constants import Size, h


def main():
    n = 2
    grid_dim = 2 * n + 1
    grid_dimensions = Size(grid_dim, grid_dim)

    diamond_square = DiamondSquare(
        grid_dimensions=grid_dimensions,
        h=h,
    )

    diamond_square.execute()


if __name__ == "__main__":
    main()
