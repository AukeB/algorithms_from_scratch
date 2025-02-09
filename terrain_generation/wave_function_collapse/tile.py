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