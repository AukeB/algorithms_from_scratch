# Wave Function Collapse

## General

## Definitions

- **Bitmap**: Your input image, that serves as the source image from which $NxN$ patters are extracted. A bitmap is a type of memory organization or image file format used to stored digital images. It consists of a rectangular grid of pixels, where each pixel reperesents a color or shade. This description sound similar to a 'normal' image. However, originally a bitmap reffered to a binary image, where each pixel was either black or white (1-bit per pixel), in that sense it really is a map of bits. It is often used referring to uncompressed, or minimally processed data. In practice, bitmap often refers to any raster image, meaning an image made of pixels rather than vectors. It can also store multiple bits per pixel (8-bit grayscale, 24-bit color or 32-bit with alpha layer).

- **Pattern/tile**: 

- **Neighbors**:

## Code variable descriptions

Notes:
- I have created a `named_tuple` object in the `constants.py`, called `Size`. file. This is used for variables that specify a width in height in terms of:
    1. Elements/cells within a grid or tile. Variables of this type contain the word `dimensions` in it, for example `grid_dimensions`.
    2. Number of pixels a tile or cell consists of. Variables of this type contain the word `size` in in, for example `tile_size`.
- The cells of which the grid consists are referred to as `grid_cell`, and the cells of which a tile consists are called `tile_cell`. A cell of a grid can be filled with a tile, so a grid cell can consist of several tile cells. 

| Variable name | Type | Type more elaborate | Dimensions | Description |
|---|---|---|---|---|
| `bitmap-dimensions`| `Size` | `Size[int, int]` | $mxn$ | The number of pixels your bitmap consists of, specified in width and height. |
| `grid_dimensions`| `Size` | `Size[int, int]` | $mxn$ | The number of grid elements/cells that grid consists of. In the code this is referred to as `grid_cell`. |
| `grid` | `list` | `list[list[GridCell]]` | $mxn$ | The grid. After the algorithm has completed, this will contain the collapsed cells and the generated pattern based on the bitmap input image. It is a 2D-list of objects of the `GridCell` class. |
| `tile_dimensions`| `Size` | `Size[int, int]` | $mxn$ | The number of elements/cells that a tile consists of. In the code this is referred to as `tile_cell` | 
| `all_tiles`| `list` | `list[tuple[tuple[str]]]` | - | A list of all the tiles extracted from the bitmap, so it probably contains duplicated values A tile is represented with a 2D-tuple of string values. | 
| `tile_weights`| `dict` | `dict[tupe[tuple[str]]: float]` | - | A dictionary where for each unique tile the weight is represented as a float value. All weights sum up to 1. | 
| `tile_set`| `set` | `set[tuple[tuple[str]]]` | - | The set of all unique tiles that were extracted from the bitmap. | 
| `neighbors`| `dict` | `dict[tuple[tuple[str]]: dict[str: set[tuple[tuple[str]]]]]` | - | This variable contains all the information about which tiles are allowed to go next to which tiles. It is a nested dictionary. The keys in the first dictonary are all the uniques tiles, so 2D-tuples of strings. Then, for each tile, there are 4 directions, 'top', 'bottom', 'left' and 'right'. For each of this 4 directions, the set of tiles is stored as values of the dictionary. These sets of tiles are the allowed neighbors for each direction. 
| `recursion_depth`|  |  | To be written later when it is implemented more efficiently. | 
| `variable`|  |  |  | 
| `variable`|  |  |  | 
| `variable`|  |  |  | 
| `variable`|  |  |  | 
| `variable`|  |  |  | 
| `variable`|  |  |  | 
| `variable`|  |  |  | 
| `variable`|  |  |  | 
| `variable`|  |  |  | 
| `variable`|  |  |  | 
neighbors[tile]["up"].add(other_tile)
## Algorithm

## Model versions

- The '**Even simpler tiled model**':
- The '**Simple tiled model**':
    - Predefined set of $NxN$ paterns/tifles.
    - Predefined adjacency rules for these patterns.
- The '**Overlapping model**:
    - No predefined patterns/tiles and no predefined adjacency rules.
    - Instead, these are extracted directly from the source input bitmap.
    - To make this version of the algorithm even more advanced, you can think about mirroring and rotating your patterns to expand your tileset. You can also determine the symmetry properties of your tileset to make this code more efficient if you want to implement that. If I at some point will code that, I will probably treat it as an additional feature once I've completed programming the algorithm without it.
k
## Resources

- The [original repository](https://github.com/mxgmn/WaveFunctionCollapse/tree/master) by [mxgmn](https://github.com/mxgmn). However, I don't think the algorithm description is formulated properly. I spend a lot of time trying to figure out what the adjacency rules precisely are for the constraint propagation, also for different versions of the algorithm. I think it could have been written more clearly. I also don't see the point of the quantum mechanics analogy. Introducing this makes it unnecessarily complex; for example, entropy is just a fancy word for the 'number of options' or 'number of possibilities' in the context of the wave function collapse algorithm. You can probably have a good discussion whether it is correct to use quantum mechanical terms in this context, but I think that's besides the point and also wrong. It is wrong because entropy in quantum mechanics or thermodynamics describes a different type of system; it is based on the physical arrangements of molecules on a microscopic level while still appearing the same on the macro level, while in the context of WFC it's just the number of options for a element in your variable that represents the grid. It is besides the point because code should be simple and easy to understand, and trying to explain the concepts related to your procedural generation algorithm (or however you want to describe it) in terms of quantum mechanical concepts, doesn't help with this. It does sound fancy though, and it grabs your attention, so I guess it's just good marketing.
- A [blog post](https://www.gridbugs.org/wave-function-collapse/). Haven't read it yet.
- This [blog post](https://robertheaton.com/2018/12/17/wavefunction-collapse-algorithm/) by Robert Heaton is a good one to start with. It explains the algorithm from a basic level and also introduced an even simpler version of the algorithm which makes it easier to understand the more advanced versions.
- [Model sysnthesis](https://paulmerrell.org/model-synthesis/) by Paul Merrell. A 3-dimensional application of the WFC algorithm.
