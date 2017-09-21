#!/usr/bin/env python
# -*- coding: utf-8 -*-

# import modules
import logging
# import third-party modules
from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtCore import pyqtSignal as Signal, pyqtSlot as Slot


class QtLogHandler(QTextEdit):

    messageAppended = Signal(int, str)

    defaultLevelColors = {
        logging.DEBUG: "#00aa00",       # green
        logging.INFO: "#0000ff",        # blue
        logging.WARNING: "#ffaa00",     # orange
        logging.ERROR: "#ff0000",       # red
        logging.CRITICAL: "#ff0000"     # red
    }

    def __init__(self, levelColor=None, parent=None):
        super().__init__(parent)
        if levelColor is None:
            self.levelColors = self.defaultLevelColors
        else:
            self.levelColors = levelColor
        self.handler = logging.Handler()
        self.handler.emit = self.emit
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.handler.setFormatter(formatter)

    def emit(self, record):
        print(self.handler.format(record))
        print(self.handler.formatter.formatTime(record))
        print(self.handler.formatter.formatMessage(record))
        self.appendLogMessage(
            record.levelno, record.levelname, record.getMessage()
        )

    @Slot(int, str, str)
    def appendLogMessage(self, level, levelString, msg):
        if level < self.handler.level:
            return
        level_color = self.levelColors.get(level, "#000000")
        p_style = ";".join([
            "margin:0px 0px 0px 0px", "-qt-block-indent:0", "text-indent:0px"
        ])
        span_style = ";".join([
            "font-weight:600", "color:{}".format(level_color)
        ])
        rich_text = """
            <p style="{:s}">
                <span style="{:s}">{:s}:</span>{:s}
            </p>
        """.format(p_style, span_style, levelString, msg)
        self.append(rich_text)
        self.messageAppended.emit(level, msg)
