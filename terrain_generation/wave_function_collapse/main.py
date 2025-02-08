""" """

from bitmap import BitmapUtils
from wfc import WaveFunctionCollapse
from constants import Size

bitmap_utils = BitmapUtils()


def main():
    bitmap = bitmap_utils.read_bitmap_from_excel(
        relative_dir_path="terrain_generation/wave_function_collapse/bitmaps",
        file_name="mountains.xlsx",
        export_as_png=True,
    )

    color_mapping = bitmap_utils.create_color_mapping(rgb_size=bitmap)
    bitmap = bitmap_utils.apply_color_mapping(rgb_size=bitmap, color_mapping=color_mapping)

    grid_dim = 40
    tile_dim = 3

    grid_dimensions = Size(grid_dim, grid_dim)
    tile_dimensions = Size(tile_dim, tile_dim)

    for _ in range(10):
        wfc = WaveFunctionCollapse(
            bitmap=bitmap,
            grid_dimensions=grid_dimensions,
            tile_dimensions=tile_dimensions,
            color_mapping=color_mapping,
        )

        wfc.collapse_grid()


if __name__ == "__main__":
    main()
