#!/usr/bin/env python
# -*- coding: utf-8 -*-

# import modules
from qtpy.QtWidgets import QWidget, QSizePolicy, QVBoxLayout
from qtpy.QtCore import QSize, Signal, Slot
from matplotlib.figure import Figure
from matplotlib.backend_bases import (
    Event, MouseEvent, PickEvent, DrawEvent, KeyEvent, ResizeEvent, CloseEvent
)
from qtpy import API
if API in ['pyqt5', 'pyside2']:
    from matplotlib.backends.backend_qt5agg import (
        FigureCanvasQTAgg as FigureCanvas,
        NavigationToolbar2QT as NavigationToolbar
    )
else:
    from matplotlib.backends.backend_qt4agg import (
        FigureCanvasQTAgg as FigureCanvas,
        NavigationToolbar2QT as NavigationToolbar
    )


class QtMplCanvas(FigureCanvas):

    def __init__(self, parent=None):
        self.fig = Figure(facecolor="none")
        self.axes = self.fig.add_subplot(111)
        super(QtMplCanvas, self).__init__(self.fig)
        self.setParent(parent)
        self.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Expanding
        )
        self.updateGeometry()
        self.setMinimumSize(QSize(300, 300))


class QtMplWidget(QWidget):
    """
    """
    # Create the Qt Signals (wrappers)
    buttonPressed = Signal(MouseEvent, name="buttonPressed")
    buttonReleased = Signal(MouseEvent, name="buttonReleased")
    canvasRedrawn = Signal(DrawEvent, name="canvasRedrawn")
    keyPressed = Signal(KeyEvent, name="keyPressed")
    keyReleased = Signal(KeyEvent, name="keyReleased")
    mouseMotion = Signal(MouseEvent, name="mouseMotion")
    artistPicked = Signal(PickEvent, name="artistPicked")
    figureResized = Signal(ResizeEvent, name="figureResized")
    mouseScrolled = Signal(MouseEvent, name="mouseScrolled")
    figureEntered = Signal(Event, name="figureEntered")
    figureLeft = Signal(Event, name="figureLeft")
    axesEntered = Signal(MouseEvent, name="axesEntered")
    axesLeft = Signal(MouseEvent, name="axesLeft")
    figureClosed = Signal(CloseEvent, name="figureClosed")
    # new Qt signals
    toolbarMoved = Signal(str, name="toolbarMoved")
    toolbarShown = Signal(bool, name="toolbarShown")

    def __init__(self, toolbar=True, toolbarPosition="top", parent=None):
        super(QtMplWidget, self).__init__(parent)
        self.toolbarPosition = toolbarPosition
        self.__setup_ui(toolbar)
        self.__wrap_mpl_signals()

    def __setup_ui(self, toolbar):
        """Setup the matplotlib widget UI elements
        """
        self.canvas = QtMplCanvas(self)
        self.fig = self.canvas.fig
        self.axes = self.canvas.axes
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.canvas)
        if toolbar is True:
            self.showToolbar()
        else:
            self.toolbar = None

    def __wrap_mpl_signals(self):
        """Wrap the mpl_connect events in Qt signals.
        """
        self.__buttonPressedCid = self.canvas.mpl_connect(
            "button_press_event", self.buttonPressed.emit
        )
        self.__buttonReleasedCid = self.canvas.mpl_connect(
            "button_release_event", self.buttonReleased.emit
        )
        self.__canvasRedrawnCid = self.canvas.mpl_connect(
            "draw_event", self.canvasRedrawn.emit
        )
        self.__keyPressedCid = self.canvas.mpl_connect(
            "key_press_event", self.keyPressed.emit
        )
        self.__keyReleasedCid = self.canvas.mpl_connect(
            "key_released_event", self.keyReleased.emit
        )
        self.__mouseMotionCid = self.canvas.mpl_connect(
            "motion_notify_event", self.mouseMotion.emit
        )
        self.pickCid = self.canvas.mpl_connect(
            "pick_event", self.artistPicked.emit
        )
        self.__figureResizedCid = self.canvas.mpl_connect(
            "resize_event", self.figureResized.emit
        )
        self.__mouseScrolledCid = self.canvas.mpl_connect(
            "scroll_event", self.mouseScrolled.emit
        )
        self.__figureEnteredCid = self.canvas.mpl_connect(
            "figure_enter_event", self.figureEntered.emit
        )
        self.__figureLeftCid = self.canvas.mpl_connect(
            "figure_leave_event", self.figureLeft.emit
        )
        self.__axesEnteredCid = self.canvas.mpl_connect(
            "axes_enter_event", self.axesEntered.emit
        )
        self.__axesLeftCid = self.canvas.mpl_connect(
            "axes_leave_event", self.axesLeft.emit
        )
        self.__figureClosedCid = self.canvas.mpl_connect(
            "close_event", self.figureClosed.emit
        )

    @property
    def toolbarPosition(self):
        return self.toolbarPosition

    @toolbarPosition.setter
    def toolbarPosition(self, position):
        if position not in ["top", "bottom"]:
            raise ValueError("Toolbar position can only be 'top' or 'bottom'")
        self.toolbarPosition = position

    @Slot(bool)
    def showToolbar(self, show):
        if self.toolbar is None:
            self.moveToolbar(self.toolbarPosition)
        self.toolbar.setVisible(show)
        self.toolbarShown.emit(show)

    @Slot(str)
    def moveToolbar(self, position):
        self.toolbarPosition = position
        # if no toolbar, add it
        if self.toolbar is None:
            self.toolbar = NavigationToolbar(
                self.canvas, self, coordinates=True
            )
        else:
            self.layout.removeWidget(self.toolbar)
        if position == "top":
            self.layout.insertWidget(0, self.toolbar)
        else:
            self.layout.addWidget(self.toolbar)
        self.toolbarMoved.emit(self.toolbarPosition)

    @Slot()
    @Slot(bool)
    def clearAxes(self, draw=True):
        self.axes.clear()
        if draw:
            self.canvas.draw()
