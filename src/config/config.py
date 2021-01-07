import cv2

# Pointer offsets
OFFSET_y = 66
OFFSET_x = 127

# image offsets
OFFSET_IMAGE_X = 250
OFFSET_IMAGE_Y = 200

# flags
CAMERA = [0, 1, 2, 3]
VIDEO_STARTED = False
PENCIL_STARTED = False
ERASE_FLAG = False
IS_SECONDWINDOW = True
SECOND_WINDOW_TRANSPARENT = True

CAP = None
PATH = None
CURSOR = None

BRUSH_SIZE = 6
CLEAR_SIZE = 20
DRAWING = False


COLORS = [
    # 17 undertones https://lospec.com/palette-list/17undertones
    '#000000', '#00ff00', '#414168', '#3a7fa7', '#35e3e3', '#8fd970', '#5ebb49',
    '#458352', '#dcd37b', '#ffd035', '#cc9245', '#a15c3e', '#a42f3b',
    '#f45b7a', '#c24998', '#81588d', '#bcb0c2', '#ffffff',
]


