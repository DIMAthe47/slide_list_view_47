from PIL import Image
from PyQt5.QtGui import QPixmap, QColor
from PyQt5.QtWidgets import QMessageBox

from tiled_pixmap import TiledPixmap, tile_rect, chess_positions


class MediaObject(object):
    def __init__(self, text, pilimg_or_pixmap, data):
        self.text = text
        self.pilimg_or_pixmap = pilimg_or_pixmap
        self.data = data


def default_media_object_extractor(source):
    return source
    # return MediaObject(source, None, "default data")


def imagefilepath_to_media_object(filepath):
    pilimg = Image.open(filepath)
    return MediaObject(filepath, pilimg, "default data")


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
    # "filepath+pilimg": imagefilepath_to_media_object,
    # "filepath+pixmap": imagefilepath_to_media_object_with_pixmap,
    # "filepath+masked_tiles_pixmap": imagefilepath_to_media_object_with_masked_tiles,
}
