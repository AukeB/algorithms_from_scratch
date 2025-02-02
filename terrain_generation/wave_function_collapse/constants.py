from collections import namedtuple

Size = namedtuple("Size", ["width", "height"])
screen_resolution = (1920, 1080)
directions = {
    "up": (-1, 0),
    "down": (1, 0),
    "left": (0, -1),
    "right": (0, 1),
}
