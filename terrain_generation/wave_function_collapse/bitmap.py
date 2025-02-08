import os
import logging
from openpyxl import load_workbook
from PIL import Image
from collections import namedtuple

Size = namedtuple("Size", ["width", "height"])


class BitmapUtils:
    """ """

    def __init__(
        self,
        output_file_path_bitmap_images="terrain_generation/wave_function_collapse/bitmaps/",
    ) -> None:
        """ """
        self.output_file_path_bitmap_images = output_file_path_bitmap_images

    def _obtain_bitmap_size(
        self,
        sheet,
        default_background_color: str = "00000000",
    ) -> tuple[int, int]:
        """Find the first column and row with None values in the given sheet."""
        first_column_with_none = None
        first_row_with_none = None

        # Access the first row
        for col_idx, cell in enumerate(sheet[1], start=1):
            background_color = cell.fill.start_color.index
            if background_color == default_background_color:
                first_column_with_none = col_idx - 1
                break

        # Access the first column
        for row_idx, cell in enumerate(sheet["A"], start=1):
            background_color = cell.fill.start_color.index
            if background_color == default_background_color:
                first_row_with_none = row_idx - 1
                break

        return first_column_with_none, first_row_with_none

    def _hex_to_rgb(self, color_hex):
        """ """
        r = int(color_hex[0:2], 16)
        g = int(color_hex[2:4], 16)
        b = int(color_hex[4:6], 16)

        return (r, g, b)

    def _export_bitmap_as_png(
        self,
        bitmap: list[list[tuple[int, int, int]]],
        file_name: str,
        cell_size: int = 30,
    ) -> None:
        """ """
        bitmap_dimensions = Size(len(bitmap), len(bitmap[0]))
        img_width = cell_size * bitmap_dimensions.width
        img_height = cell_size * bitmap_dimensions.height

        img = Image.new("RGB", (img_width, img_height), color=(255, 255, 255))

        for y, row in enumerate(bitmap):
            for x, color in enumerate(row):
                for dx in range(cell_size):
                    for dy in range(cell_size):
                        img.putpixel((x * cell_size + dx, y * cell_size + dy), color)

        image_filename = self.output_file_path_bitmap_images + file_name.split(".")[0] + ".png"
        img.save(image_filename, "PNG")

        logging.info(f"Bitmap exported as {image_filename}")

    def read_bitmap_from_excel(
        self,
        file_name: str,
        relative_dir_path: str = "bitmaps",
        export_as_png: bool = True,
    ) -> tuple[list[list[str]], list[list[str]]]:
        """ """
        relative_file_path = os.path.join(relative_dir_path, file_name)

        # This assumes the bitmap is always on the first tab of the excel file.
        sheet = load_workbook(relative_file_path).worksheets[0]
        size_width, size_height = self._obtain_bitmap_size(sheet=sheet)

        bitmap = []

        for row in sheet.iter_rows(
            min_row=1,
            max_row=size_width,
            min_col=1,
            max_col=size_height,
        ):
            bitmap_row = []

            for cell in row:
                color_hex = cell.fill.start_color.index
                color_rgb = self._hex_to_rgb(
                    color_hex=color_hex[2:]
                )  # First two elements contain transparency/alpha/opacity.
                bitmap_row.append(color_rgb)

            bitmap.append(bitmap_row)

        if export_as_png:
            self._export_bitmap_as_png(bitmap=bitmap, file_name=file_name)

        return bitmap

    def create_color_mapping(self, rgb_size):
        """ """
        color_mapping = {}
        current_char = "A"

        for row in rgb_size:
            for rgb in row:
                if rgb not in color_mapping:
                    color_mapping[rgb] = current_char
                    # Fails when the maximum number of codepoints within Unicode has been
                    # reached (somewhere at 1.1M), so that's fine.
                    current_char = chr(ord(current_char) + 1)

        return color_mapping

    def apply_color_mapping(self, rgb_size, color_mapping):
        """ """
        return [[color_mapping[rgb] for rgb in row] for row in rgb_size]
