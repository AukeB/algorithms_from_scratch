from collections import namedtuple
from pathlib import Path

Size = namedtuple("Size", ["width", "height"])
config_core_file_path = Path("terrain_generation/wave_function_collapse/configs/config_core.yaml")
config_runtime_file_path = Path(
    "terrain_generation/wave_function_collapse/configs/config_runtime.yaml"
)
