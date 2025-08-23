from collections import namedtuple

# Used for specifying width and height in number of pixels
# or number of cells within a grid.
Size = namedtuple("Size", ["width", "height"])

# Resolution of the screen in number of pixels.
screen_resolution = (1920, 1080)

# Scaling constant h (0.0 < h < 1.0) that controls the rate of scale decrease.
h = 0.5
