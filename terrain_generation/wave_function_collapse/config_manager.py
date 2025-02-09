""" """
import yaml
from pathlib import Path
from typing import Dict, List, Literal
from pydantic import BaseModel, Field


class BitmapConfig(BaseModel):
    dimensions: List[int] = Field(..., min_items=2, max_items=2)


class PngBitmapConfig(BaseModel):
    export: bool
    cell_size: int
    default_background_color: List[int] = Field(..., min_items=3, max_items=3)


class ConfigCoreSchema(BaseModel):
    screen_resolution: List[int] = Field(..., min_items=2, max_items=2)
    directions: Dict[str, List[int]]
    mode_model: Literal['overlapping', 'simple-tiled', 'even-simpler-tiled']
    mode_boundary_conditions: Literal['wrap_around', 'clamping', 'mirroring', 'noise']
    paths: Dict[str, str]
    bitmaps: Dict[str, BitmapConfig]
    png_bitmap: PngBitmapConfig


class ConfigRuntimeSchema(BaseModel):
    file_name: str
    grid_dim: int
    tile_dim: int


class ConfigManager:
    def __init__(self, config_core_relative_path: str, config_runtime_relative_path: str):
        self.config_core_relative_path = config_core_relative_path
        self.config_runtime_relative_path = config_runtime_relative_path

    def read_configs(self):
        if not Path(self.config_core_relative_path).exists():
            raise FileNotFoundError(f"Config core file not found: {self.config_core_relative_path}")
        
        with open(self.config_core_relative_path, 'r', encoding='utf-8') as file:
            config_core = yaml.safe_load(file)
        
        if not Path(self.config_runtime_relative_path).exists():
            raise FileNotFoundError(f"Config runtime file not found: {self.config_runtime_relative_path}")
        
        with open(self.config_runtime_relative_path, 'r', encoding='utf-8') as file:
            config_runtime = yaml.safe_load(file)
        
        config_core = ConfigCoreSchema(**config_core).dict()
        config_runtime = ConfigRuntimeSchema(**config_runtime).dict()
        
        return config_core, config_runtime
