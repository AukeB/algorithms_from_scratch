""" """


class Tile:
    """ """

    def __init__(
        self,
        tile: tuple[tuple[str]],
    ) -> None:
        """ """
        self.value = tile
        self.up = tile[:-1]
        self.down = tile[1:]
        self.right = tuple(row[1:] for row in tile)
        self.left = tuple(row[:-1] for row in tile)

    def __repr__(self):
        return f"{self.value}"

    def __hash__(self):
        return hash(self.value)

    def __eq__(self, other):
        return isinstance(other, Tile) and self.value == other.value

    def flip_horizontally(self, edge: tuple[tuple[str]]) -> tuple[tuple[str]]:
        """Flips an edge horizontally (reverses each row)."""
        return tuple(row[::-1] for row in edge)

    def flip_vertically(self, edge: tuple[tuple[str]]) -> tuple[tuple[str]]:
        """Flips an edge vertically (reverses the order of rows)."""
        return edge[::-1]
