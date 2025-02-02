""" """
class Cell:
    """ """
    def __init__(
        self,
        tile_set: set,
    ) -> None:
        """ """
        # Todo: possible with just one variable?
        self.options = tile_set
        self.collapsed = False
        self.tile = None

    def __repr__(self):
        return f"{self.collapsed}"