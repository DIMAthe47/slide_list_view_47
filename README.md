# media_objects_47

Simplest pyqt implementation of [ListView](http://doc.qt.io/qt-5/qlistview.html) with flavour of [media object](https://getbootstrap.com/docs/4.0/layout/media-object)
from bootstrap.

Screenshot of media objects widget:

![screenshot](/media_objects_screen.png)

### Use
Object of type [MediaObject](https://github.com/DIMAthe47/media_objects_47/blob/master/media_object.py) contains image, text, data.

To use [MediaObjectsListView](https://github.com/DIMAthe47/media_objects_47/blob/master/media_object_list_view.py) you need to 
[setModel](http://doc.qt.io/qt-5/qabstractitemview.html#setModel) [MediaObjectsListModel](https://github.com/DIMAthe47/media_objects_47/blob/master/media_object_list_model.py)
to it populated with list of
[MediaObject](https://github.com/DIMAthe47/media_objects_47/blob/master/media_object.py).


### Predefined actions
- MediaObject from filepath

  List of MediaObject can come from anywhere, but often
  use case is when MediaObject is representation of file in filesystem. So there is predefined [OnLoadMediaObjectsAction](https://github.com/DIMAthe47/media_objects_47/blob/master/media_object_action.py)
  for which you just need to pass custom function that builds MediaObject from filepath:
  ```
  media_object_extractor(filepath:str)->MediaObject
  ```
- Selection

  [OnLoadMediaObjectsAction](https://github.com/DIMAthe47/media_objects_47/blob/master/media_object_action.py) serves for getting data
  of selected MediaObject`s.
  To use it you need to pass it custom function:
  ```
  data_consumer(data:any)
  ```

### Features:
- fixed size icon or icon with proportion of view size
- [TiledPixmap](https://github.com/DIMAthe47/media_objects_47/blob/master/tiled_pixmap.py) class can be used to slice
  pixmap into tiles with their own colors. These tiles can serve as masks for regions on entire image

Screenshot demonstrating proportion-sized icons (0.5 of width and 0.25 of height) and tiled pixmap in chess style:

![screenshot](/tiled_pixmap_screenshot.png)
