""" """
class Cell:
    """ """
    def __init__(
        self,
        tile_set: set,
    ) -> None:
        """ """
        self.options = tile_set
        self.collapsed = False