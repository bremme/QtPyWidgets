#!/usr/bin/env python
# -*- coding: utf-8 -*-

# import modules
import os
import json
from types import SimpleNamespace
# import third-party modules
from qtpy.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings
from qtpy.QtWidgets import QSizePolicy
from qtpy.QtGui import QDesktopServices
from qtpy.QtCore import QObject, QUrl, QSize, Slot, Signal

# from PyQt5.QtWebKitWidgets import QWebView as QWebEngineView
# from PyQt5.QtWebKit import QWebSettings as QWebEngineSettings
# from PyQt5.QtWidgets import QSizePolicy
# from PyQt5.QtCore import QUrl, QSize, pyqtSlot as Slot, pyqtSignal as Signal


class GoogleMapsLatLngBounds(QObject):

    def __init__(self, south, west, north, east, parent=None):
        super().__init__(parent)
        self.south = south
        self.west = west
        self.north = north
        self.east = east

    def update(self, *args):
        self.south = args[0]
        self.west = args[1]
        self.north = args[2]
        self.east = args[3]

    def updateJSON(self, boundsJSONString):
        for key, value in json.loads(boundsJSONString):
            setattr(self, key, value)

    def toJS(self):
        public_dict = {
            k: v for k, v in self.__dict__.items() if not k.startswith("_")}
        return public_dict


class GoogleMapsMouseEvent(QObject):

    def __init__(self, lat, lng, pixel_x, pixel_y, ea_x, ea_y,  parent=None):
        super().__init__(parent)
        self.latLng = GoogleMapsLatLng(lat, lng, self)
        self.pixel = GoogleMapsPoint(pixel_x, pixel_y, self)
        self.ea = GoogleMapsPoint(ea_x, ea_y, self)

    @staticmethod
    def fromJSON(mouseEventJSONtring):
        data = json.loads(mouseEventJSONtring)
        return GoogleMapsMouseEvent(
            data["latLng"]["lat"], data["latLng"]["lng"],
            data["pixel"]["x"], data["pixel"]["y"],
            data["ea"]["x"], data["ea"]["y"],
        )

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


class GoogleMapsPoint(QObject):

    def __init__(self, x, y, parent=None):
        super().__init__(parent)
        self.x = x
        self.y = y

    def toJS(self):
        public_dict = {
            k: v for k, v in self.__dict__.items() if not k.startswith("_")}
        return public_dict


class GoogleMapsLatLng(QObject):

    def __init__(self, lat, lng, parent=None):
        super().__init__(parent)
        self.lat = lat
        self.lng = lng

    def updateJSON(self, latLngJSONString):
        for key, value in json.loads(latLngJSONString):
            setattr(self, key, value)

    def update(self, lat, lng):
        self.lat = lat
        self.lng = lng

    def toJS(self):
        public_dict = {
            k: v for k, v in self.__dict__.items() if not k.startswith("_")}
        return public_dict


class GoogleMapsMapOptions(QObject):
    """
    See: https://developers.google.com/maps/documentation/javascript/reference#MapOptions
    """

    __attributes = [
        "backgroundColor", "center", "clickableIcons", "disableDefaultUI",
        "disableDoucleClickZoom", "draggable", "draggableCursor",
        "draggingCursor", "fullscreenControl", "fullscreenControlOptions",
        "gestureHandling", "heading", "keyboardShortcuts", "mapTypeControl",
        "mapTypeControlOptions", "mapTypeId", "maxZoom", "minZoom",
        "noClear", "panControl", "panControlOptions", "rotateControl",
        "rotateControlOptions", "scaleControl", "scaleControlOptions",
        "scrollwheel", "streetView", "streetViewControl",
        "streetViewControlOptions", "styles", "tilt", "zoom", "zoomControl",
        "zoomControlOptions"
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


class QtGoogleMapsView(QWebEngineView):
    """Google Maps View using the QtWebKit bridge
    https://doc.qt.io/qt-4.8/qtwebkit-bridge.html
    """

    # Signals
    webViewReady = Signal()
    boundsChanged = Signal(GoogleMapsLatLngBounds)
    centerChanged = Signal([float, float], [GoogleMapsLatLng])
    click = Signal(GoogleMapsMouseEvent)
    doubleClick = Signal(GoogleMapsMouseEvent)
    drag = Signal()
    dragend = Signal()
    dragstart = Signal()
    headingChanged = Signal(int)
    idle = Signal()
    mapTypeIdChanged = Signal(str)
    mousemove = Signal(GoogleMapsMouseEvent)
    mouseout = Signal(GoogleMapsMouseEvent)
    mouseover = Signal(GoogleMapsMouseEvent)
    projectionChanged = Signal()
    resize = Signal(SimpleNamespace)
    rightclick = Signal(GoogleMapsMouseEvent)
    tilesloaded = Signal()
    tiltChanged = Signal(float)
    zoomChanged = Signal(int)

    jsObjectName = "googleMapsView"

    def __init__(
        self, apiKey,
        lat=0, lng=0, zoom=4, heading=0, tilt=0, clickableIcons=True, mapTypeId="terrain",
        parent=None
    ):
        super().__init__(parent)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.updateGeometry()
        self.setMinimumSize(QSize(640, 480))
        self.settings().setAttribute(
            QWebEngineSettings.DeveloperExtrasEnabled, True)
        self.settings().setAttribute(
            QWebEngineSettings.JavascriptEnabled, True)
        self.settings().setAttribute(
            QWebEngineSettings.LocalContentCanAccessRemoteUrls, True)
        self.settings().setAttribute(
            QWebEngineSettings.LocalContentCanAccessFileUrls, True)

        self.linkClicked.connect(QDesktopServices.openUrl)

        self.mainFrame.addToJavaScriptWindowObject("qtwebview", self)
        url_path = os.path.join(
            os.path.abspath(os.path.dirname(__file__)),
            "index.html"
        )
        url = QUrl("file://{}".format(url_path))
        self.setUrl(url)
        self.loadFinished.connect(self._pageLoadFinished)
        self.webViewReady.connect(self._webViewReady)

        # properties
        self._apiKey = apiKey
        self._bounds = GoogleMapsLatLngBounds(0, 0, 0, 0)
        self._center = GoogleMapsLatLng(lat, lng)
        self._clickableIcons = clickableIcons
        self._zoom = zoom
        self._heading = heading
        self._tilt = tilt
        self._mapTypeId = mapTypeId
        #
        self._markers = []
        self._markerIdCounter = 0

    @property
    def mainFrame(self):
        return self.page().mainFrame()

    @Slot(bool)
    def _pageLoadFinished(self, state):
        self.mainFrame.addToJavaScriptWindowObject("qtwebview", self)
        options = GoogleMapsMapOptions(
            center=self._center, zoom=self._zoom, mapTypeId=self._mapTypeId,
            heading=self._heading, tilt=self._tilt
        )
        self._callJS("init", options, self._apiKey)

    @Slot()
    def _webViewReady(self):
        print("Webview is ready")
        # wait till ready
        self.addMarker(10, 10, "10 - 10")
        self.setMapTypeId("satellite")
        self.setCenter(30, 40)

    @property
    def bounds(self):
        return self._bounds

    @bounds.setter
    def bounds(self, *args):
        self.setBounds(*args)

    @Slot(float, float, float, float)
    @Slot(GoogleMapsLatLngBounds)
    def setBounds(self, *args):
        if len(args) == 1:
            self._callJS(
                ".map.setBounds",
                args[0].south, args[0].west, args[0].north, args[0].east
            )
        else:
            self._callJS(
                ".map.setBounds", args[0], args[1], args[2], args[3]
            )

    @Slot(float, float, float, float)
    def _boundsChanged(self, south, west, north, east):
        print("_boundsChanged", south, west, north, east)
        self._bounds.update(south, west, north, east)
        self.boundsChanged.emit(self._bounds)

    @property
    def center(self):
        return self._center

    @center.setter
    def center(self, *args):
        self.setCenter(*args)

    @Slot(float, float)
    @Slot(GoogleMapsLatLng)
    def setCenter(self, *args):
        if len(args) == 1:
            self._callJS(
                "map.setCenter", {"lat": args[0].lat, "lng": args[0].lng}
            )
        else:
            self._callJS(
                "map.setCenter", {"lat": args[0], "lng": args[1]}
            )

    @Slot(float, float)
    def _centerChanged(self, lat, lng):
        print("_centerChanged", lat, lng)
        self._center.update(lat, lng)
        self.centerChanged.emit(lat, lng)
        self.centerChanged[GoogleMapsLatLng].emit(self._center)

    @property
    def clickableIcons(self):
        return self._clickableIcons

    @clickableIcons.setter
    def clickableIcons(self, clickableIcons):
        self.setClickableIcons(clickableIcons)

    @Slot(bool)
    def setClickableIcons(self, clickableIcons):
        self._callJS("setClickableIcons", clickableIcons)
        self._clickableIcons = clickableIcons

    @Slot(str)
    def _click(self, mouse_event_json_string):
        print("_click:", mouse_event_json_string)
        mouseEvent = GoogleMapsMouseEvent.fromJSON(mouse_event_json_string)
        self.click.emit(mouseEvent)

    @Slot(str)
    def _doubleClick(self, mouse_event_json_string):
        print("_doubleClick:", mouse_event_json_string)
        mouseEvent = GoogleMapsMouseEvent.fromJSON(mouse_event_json_string)
        self.doubleClick.emit(mouseEvent)

    @Slot()
    def _drag(self):
        print("_drag")
        self.drag.emit()

    @Slot()
    def _dragend(self):
        print("_dragend")
        self.dragend.emit()

    @Slot()
    def _dragstart(self):
        print("_dragstart")
        self.dragstart.emit()

    @property
    def heading(self):
        return self._heading

    @heading.setter
    def heading(self, heading):
        self.setHeading(heading)

    @Slot(int)
    def setHeading(self, heading):
        self._callJS("map.setHeading", heading)

    @Slot(int)
    def _headingChanged(self, heading):
        self._heading = heading
        print("_headingChanged", heading)
        self.headingChanged.emit(heading)

    @Slot()
    def _idle(self):
        print("_idle")
        self.idle.emit()

    @property
    def mapTypeId(self):
        return self._mapTypeId

    @mapTypeId.setter
    def mapTypeId(self, mapTypeId):
        self.setMapTypeId(mapTypeId)

    @Slot(str)
    def setMapTypeId(self, map_type):
        self._callJS("map.setMapTypeId", map_type)

    @Slot(str)
    def _mapTypeIdChanged(self, mapTypeId):
        print("_mapTypeIdChanged", mapTypeId)
        self._mapTypeId = mapTypeId
        self.mapTypeIdChanged.emit(mapTypeId)

    @Slot(float, float)
    @Slot(GoogleMapsPoint)
    def panBy(self, *args):
        if len(args) == 1:
            self._callJS("map.panBy", args[0])
        elif len(args) == 2:
            self._callJS("map.panBy", GoogleMapsPoint(args[0], args[1]))

    @Slot(str)
    def _mousemove(self, mouse_event_json_string):
        # print("_mousemove", mouse_event_json_string)
        mouseEvent = GoogleMapsMouseEvent.fromJSON(mouse_event_json_string)
        self.mousemove.emit(mouseEvent)

    @Slot(str)
    def _mouseout(self, mouse_event_json_string):
        print("_mouseout", mouse_event_json_string)
        mouseEvent = GoogleMapsMouseEvent.fromJSON(mouse_event_json_string)
        self.mouseout.emit(mouseEvent)

    @Slot(str)
    def _mouseover(self, mouse_event_json_string):
        print("_mouseover", mouse_event_json_string)
        mouseEvent = GoogleMapsMouseEvent.fromJSON(mouse_event_json_string)
        self.mouseover.emit(mouseEvent)

    @Slot()
    def _projectionChanged(self):
        print("_projectionChanged")
        self.projectionChanged.emit()

    @Slot(str)
    def _resize(self, event_json_string):
        print("_resize", event_json_string)
        self.resize.emit(self.jsonToNamespace(event_json_string))

    @Slot(str)
    def _rightclick(self, mouse_event_json_string):
        print("_rightclick:", mouse_event_json_string)
        mouseEvent = GoogleMapsMouseEvent.fromJSON(mouse_event_json_string)
        self.rightclick.emit(mouseEvent)

    @Slot()
    def _tilesloaded(self):
        print("_tilesloaded")
        self.tilesloaded.emit()

    @property
    def tilt(self):
        return self._tilt

    @tilt.setter
    def tilt(self, tilt):
        self.setTilt(tilt)

    @Slot(int)
    def setTilt(self, tilt):
        self._callJS("map.setTilt", tilt)

    @Slot(float)
    def _tiltChanged(self, tilt):
        self._tilt = tilt
        print("_tiltChanged", tilt)
        self.tiltChanged.emit(tilt)

    @property
    def zoom(self):
        return self._zoom

    @zoom.setter
    def zoom(self, zoom):
        self.setZoom(zoom)

    @Slot(int)
    def setZoom(self, zoom):
        print("setZoom", zoom)
        self._callJS("map.setZoom", zoom)

    @Slot(int)
    def _zoomChanged(self, zoom):
        print("_zoomChanged", zoom)
        self._zoom = zoom
        self.zoomChanged.emit(zoom)

    def _callJS(self, method, *arguments):
        jsString = "{}.{}({:s})".format(
            self.jsObjectName, method, self.toJSargs(*arguments)
        )
        print("_callJS", jsString)
        return self.mainFrame.evaluateJavaScript(jsString)

    @staticmethod
    def jsonToNamespace(jsonstring):
        if jsonstring == "":
            return None
        return json.loads(
            jsonstring, object_hook=lambda d: SimpleNamespace(**d)
        )

    @classmethod
    def toJSargs(cls, *args):
        str_list = []
        for arg in args:
            try:
                str_list.append("{}".format(arg.toJS()))
            except AttributeError:
                if type(arg) is str:
                    str_list.append("'{}'".format(arg))
                elif type(arg) is list:
                    str_list.append(cls.toJSargs(*arg))
                else:
                    str_list.append("{}".format(arg))
        jsArgs = ", ".join(str_list)
        print("jsArgs", jsArgs)
        return jsArgs

    @property
    def apiKey(self):
        return self._apiKey

    @apiKey.setter
    def apiKey(self, apiKey):
        self.setApiKey(apiKey)

    @Slot(str)
    def setApiKey(self, apiKey):
        self._apiKey = apiKey
        self._callJS("setApiKey", apiKey)

    @Slot(float, float, str)
    def addMarker(self, latitude, longitude, title):
        from .marker import GoogleMapsMarkerOptions, GoogleMapsMarker
        options = GoogleMapsMarkerOptions(
            position=GoogleMapsLatLng(lat=latitude, lng=longitude),
            title=title
        )

        def callJS(markerId, methodName, *arguments):
            return self._callJS(
                "markers[{}].{}".format(markerId, methodName),
                *arguments
            )

        marker = GoogleMapsMarker(
            markerOptions=options, googlemap=self,
            markerId=self._markerIdCounter, callJS=callJS
        )

        self.mainFrame.addToJavaScriptWindowObject(
            "qtmarker{}".format(self._markerIdCounter), marker
        )
        self._callJS("addMarker", self._markerIdCounter, marker.options)

        # self._markers[self._markerIdCounter] = marker
        self._markers.append(marker)
        self._markerIdCounter += 1

    @Slot()
    def addRectangle(self, options):
        self.mainFrame.evaluateJavaScript(

        )
