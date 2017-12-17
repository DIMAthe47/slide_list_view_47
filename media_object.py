import random

import math
from PIL import Image
from PyQt5.QtGui import QPixmap, QColor
from PyQt5.QtWidgets import QMessageBox
import itertools

from tiled_pixmap import TiledPixmap


class MediaObject(object):
    def __init__(self, text, pilimg_or_pixmap, data):
        self.text = text
        self.pilimg_or_pixmap = pilimg_or_pixmap
        self.data = data


def default_media_object_extractor(source):
    return MediaObject(source, None, "default data")


def imagefilepath_to_media_object(filepath):
    pilimg = Image.open(filepath)
    return MediaObject(filepath, pilimg, "default data")


def chop(length, n_chops):
    regular_chop_length = math.ceil(length / n_chops)
    chops = [regular_chop_length * i for i in range(n_chops)]
    offsets = [min((length - i * regular_chop_length, regular_chop_length)) for i in range(n_chops)]
    return chops, offsets


def repeat_each_n_times(iterable, n):
    repeated_iter = zip(*[iter(iterable) for i in range(n)])
    return itertools.chain.from_iterable(repeated_iter)


def tile_rect(width, height, columns, rows):
    x_poses, widths = chop(width, columns)
    y_poses, heights = chop(height, rows)
    x_iter = itertools.cycle(x_poses)
    width_iter = itertools.cycle(widths)
    y_iter = repeat_each_n_times(y_poses, columns)
    height_iter = repeat_each_n_times(heights, columns)
    tiles_rects = list(zip(x_iter, y_iter, width_iter, height_iter))
    return tiles_rects


def chess_positions(columns, rows):
    return [(i, j) for i in range(rows) for j in range(columns) if (i + j) % 2 != 0]


def random_qcolor(alpha):
    return QColor(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), alpha)


def imagefilepath_to_media_object_with_masked_tiles(filepath, columns=7, rows=7):
    pilimg = Image.open(filepath)
    masked_tile_rects = tile_rect(pilimg.width, pilimg.height, columns, rows)
    chess_positions_ = chess_positions(columns, rows)
    chess_tile_rects = [masked_tile_rects[i * columns + j] for i in range(rows) for j in range(columns) if
                        (i, j) in chess_positions_]
    # qcolors = [random_qcolor(128) for i in range(columns * rows)]
    qcolors = [QColor(0, 255, 0, 128) for i in range(columns * rows)]
    pixmap = TiledPixmap(filepath, chess_tile_rects, qcolors)
    return MediaObject(filepath, pixmap, "default data")


def imagefilepath_to_media_object_with_pixmap(filepath):
    pixmap = QPixmap(filepath)
    return MediaObject(filepath, pixmap, "default data")


def default_data_consumer(data):
    QMessageBox.information(None, "default_data_consumer", str(data))


media_object_extractors = {
    "filepath": default_media_object_extractor,
    "filepath+pilimg": imagefilepath_to_media_object,
    "filepath+pixmap": imagefilepath_to_media_object_with_pixmap,
    "filepath+masked_tiles_pixmap": imagefilepath_to_media_object_with_masked_tiles,
}
