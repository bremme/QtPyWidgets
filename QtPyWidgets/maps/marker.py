#!/usr/bin/env python
# -*- coding: utf-8 -*-
from qtpy.QtCore import QObject, Slot, Signal


class GoogleMapsMarkerOptions(QObject):

    __attributes = [
        "anchorPoint", "animation", "clickable", "crossOnDrag", "cursor",
        "draggable", "icon", "label", "map", "opacity", "optimized",
        "place", "position", "shape", "title", "visible", "zIndex"
    ]

    def __init__(self, **kwargs):
        if "parent" not in kwargs:
            parent = None
        super().__init__(parent)

        for key, value in kwargs.items():
            if key not in self.__attributes:
                raise ValueError("{} is not a valid keyword argument".format(
                    key
                ))
            setattr(self, key, value)

    def toJS(self):
        public_dict = {
            k: v for k, v in self.__dict__.items() if not k.startswith("_")}
        json_data_dict = {}
        for k, v in public_dict.items():
            if hasattr(v, "toJS"):
                json_data_dict[k] = v.toJS()
            else:
                json_data_dict[k] = v
        return json_data_dict


class GoogleMapsMarker(QObject):

    click = Signal()

    def __init__(self, markerOptions, googlemap, markerId=None, callJS=None):
        super().__init__(parent=googlemap)
        self.map = googlemap
        self.options = markerOptions
        self.id = markerId
        self.callJS = callJS

    @Slot()
    def _click(self):
        print("Marker clicked")
        self.click.emit()
