""" """
class Cell: # Todo: change name because each element of grid as well as tile is now called a cell.
    """ """
    def __init__(
        self,
        tile_set: set,
        tile_weights: dict,
        color_mapping: dict,
    ) -> None:
        """ """
        # Todo: possible with just one variable?
        self.options = tile_set
        self.collapsed = False
        self.tile = None
        self.superposition_tile = None
        self.compute_superposition_tile(
            tile_weights=tile_weights,
            color_mapping=color_mapping,
        )

    def __repr__(self):
        return f"{self.collapsed}"
    
    def compute_superposition_tile(
        self, 
        tile_weights: dict[tuple[tuple[str]], float], 
        color_mapping: dict[str, tuple[int, int, int]]
    ) -> list[list[tuple[int, int, int]]]:
        color_mapping = {v: k for k, v in color_mapping.items()}
        rgb_matrix = [[(0, 0, 0)] * len(row) for row in next(iter(self.options)).value]
        
        for tile in self.options:
            if tile in tile_weights.keys():
                weight = tile_weights[tile]
                for i, tile_row in enumerate(tile.value):
                    for j, tile_cell in enumerate(tile_row):
                        r, g, b = color_mapping[tile_cell]
                        r_sum, g_sum, b_sum = rgb_matrix[i][j]
                        
                        r_sum += r * weight
                        g_sum += g * weight
                        b_sum += b * weight
                        
                        rgb_matrix[i][j] = (r_sum, g_sum, b_sum)
        
        # Divide each element by the total weight for each cell
        total_weight = sum(tile_weights[tile] for tile in self.options if tile in tile_weights)
        
        for i in range(len(rgb_matrix)):
            for j in range(len(rgb_matrix[i])):
                r_sum, g_sum, b_sum = rgb_matrix[i][j]
                r_avg = r_sum / total_weight
                g_avg = g_sum / total_weight
                b_avg = b_sum / total_weight
                rgb_matrix[i][j] = (r_avg, g_avg, b_avg)
        
        self.superposition_tile = rgb_matrix
