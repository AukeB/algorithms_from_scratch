""" """

class WaterRipples():
    def __init__(
        self,
        number_of_columns: int = 200,
        number_of_rows: int = 200,
        damping: float = 0.9,
    ) -> None:
        """ """
        self.number_of_columns = number_of_columns
        self.number_of_rows = number_of_rows
        self.damping = damping