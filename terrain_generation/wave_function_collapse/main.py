""" """

from bitmap import BitmapUtils
from wfc import WaveFunctionCollapse
from config_manager import ConfigManager
from constants import Size, config_core_file_path, config_runtime_file_path




def main():
    # Read configs
    config_manager = ConfigManager(
        config_core_relative_path=config_core_file_path,
        config_runtime_relative_path=config_runtime_file_path,
    )

    config_core, config_runtime = config_manager.read_configs()

    # Read bitmap
    bitmap_utils = BitmapUtils(config=config_core, file_name=config_runtime['file_name'])
    bitmap = bitmap_utils.read_bitmap_from_excel()
    color_mapping = bitmap_utils.create_color_mapping(bitmap=bitmap)
    bitmap = bitmap_utils.apply_color_mapping(bitmap=bitmap, color_mapping=color_mapping)

    grid_dimensions: Size[int, int] = Size(config_runtime['grid_dim'], config_runtime['grid_dim'])
    tile_dimensions: Size[int, int] = Size(config_runtime['tile_dim'], config_runtime['tile_dim'])

    # for _ in range(10):
    #     wfc = WaveFunctionCollapse(
    #         bitmap=bitmap,
    #         grid_dimensions=grid_dimensions,
    #         tile_dimensions=tile_dimensions,
    #         color_mapping=color_mapping,
    #     )

    #     wfc.collapse_grid()


if __name__ == "__main__":
    main()
