#!/usr/bin/env python
# -*- coding: utf-8 -*-

# import modules
import sys
import os
# import third-party modules
from qtpy.QtWidgets import QApplication, QMainWindow
from qtpy.QtCore import Slot
from qtpy import uic
# add library root path
sys.path.append(os.path.join(
    os.path.abspath(os.path.dirname(__file__)),
    os.path.pardir, os.path.pardir, os.path.pardir
))
from QtPyWidgets.maps.googlemaps import (   # noqa: E402
    QtGoogleMapsView, GoogleMapsLatLngBounds, GoogleMapsLatLng,
    GoogleMapsMouseEvent
)

API_KEY = os.environ["GMAPS_API_KEY"]

class Application(QApplication):

    def __init__(self, argv):
        super().__init__(argv)
        self.window = MainWindow()
        self.window.show()


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        # wire up the userinterface
        self._setup_ui()
        # wire up the signals and slots
        self._connect_slots_signals()

    def _setup_ui(self):
        # build UI pfile path
        ui_file_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "mainwindow.ui"
        )
        # load the UI
        uic.loadUi(ui_file_path, self)
        dummyWebView = self.dummyWebView
        self.horizontalLayout.removeWidget(dummyWebView)
        self.dummyWebView.close()
        self.googlemaps = QtGoogleMapsView(apiKey=API_KEY, parent=self)
        self.rootHorizontalLayout.insertWidget(1, self.googlemaps)
        # set a window title
        self.setWindowTitle("Qt Designer Google maps")
        # set values to amplitude and frequency spinboxes
        # self.sineAmplitudeSpinBox.setValue(self.sinewave_settings.amplitude)
        # self.sineFrequencySpinBox.setValue(self.sinewave_settings.frequency)

    def _connect_slots_signals(self):
        self.addMarkerButton.clicked.connect(self._addMarker)
        # mouse events
        self.googlemaps.mousemove.connect(self._mouseMove)
        # bounds
        self.googlemaps.boundsChanged.connect(self._boundsChanged)
        # center
        self.googlemaps.centerChanged[GoogleMapsLatLng].connect(
            self._centerChanged
        )
        # zoom
        self.googlemaps.zoomChanged.connect(self.mapZoom.setValue)
        # map type id
        self.googlemaps.mapTypeIdChanged.connect(self._mapTypeIdChanged)
        self.googlemaps.headingChanged.connect(self.heading.setValue)
        self.googlemaps.tiltChanged.connect(self.tilt.setValue)
        # controls
        self.selectMapTypeId.currentIndexChanged[str].connect(
            self.googlemaps.setMapTypeId)
        self.rotateClockWiseBtn.clicked.connect(self.rotateClockWise)
        self.rotateCounterClockWiseBtn.clicked.connect(
            self.rotateCounterClockWise)
        self.increaseZoomBtn.clicked.connect(self.increaseZoom)
        self.decreaseZoomBtn.clicked.connect(self.decreaseZoom)

    @Slot(GoogleMapsMouseEvent)
    def _mouseMove(self, mouseEvent):
        self.mousePosLat.setValue(mouseEvent.latLng.lat)
        self.mousePosLng.setValue(mouseEvent.latLng.lng)
        self.mousePosX.setValue(mouseEvent.pixel.x)
        self.mousePosY.setValue(mouseEvent.pixel.y)
        self.mousePosEax.setValue(mouseEvent.ea.x)
        self.mousePosEay.setValue(mouseEvent.ea.y)

    @Slot(GoogleMapsLatLngBounds)
    def _boundsChanged(self, bounds):
        self.boundsWest.setValue(bounds.west)
        self.boundsEast.setValue(bounds.east)
        self.boundsNorth.setValue(bounds.north)
        self.boundsSouth.setValue(bounds.south)

    @Slot(GoogleMapsLatLng)
    def _centerChanged(self, center):
        self.centerLat.setValue(center.lat)
        self.centerLng.setValue(center.lng)

    @Slot(str)
    def _mapTypeIdChanged(self, mapTypeId):
        mapTypeDict = {
            "roadmap": 0, "terrain": 1, "satellite": 2, "hybrid": 3
        }
        self.mapTypeId.setText(mapTypeId)
        self.selectMapTypeId.setCurrentIndex(mapTypeDict.get(mapTypeId, 0))

    @Slot()
    def _addMarker(self):
        lat = self.latitudeSpinBox.value()
        lon = self.longitudeSpinBox.value()
        title = self.markerTitle.text()
        self.googlemaps.addMarker(lat, lon, title)

    @Slot()
    def rotateClockWise(self):
        self.googlemaps.setHeading(self.googlemaps.heading + 90)

    @Slot()
    def rotateCounterClockWise(self):
        self.googlemaps.setHeading(self.googlemaps.heading - 90)

    @Slot()
    def increaseZoom(self):
        self.googlemaps.setZoom(self.googlemaps.zoom + 1)

    @Slot()
    def decreaseZoom(self):
        self.googlemaps.setZoom(self.googlemaps.zoom - 1)


def main():
    # create the application
    app = Application(sys.argv)
    # start the Qt main loop execution
    sys.exit(app.exec_())


if __name__ == '__main__':
    # execute the main function
    main()
