
from PyQt5 import QtCore
from PyQt5.QtWidgets import QSizePolicy, QDialog, QLabel
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog
from PyQt5.QtGui import QPainter

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as Canvas
from matplotlib.figure import Figure

from matplotlib import rcParams
rcParams['font.size'] = 9


class MatplotlibWidget(Canvas):

    """ QWidget containing a matplotlib figure.

    Inherits from PyQt5.QtGui.QWidget
    and matplotlib.backend_bases.FigureCanvasBase

    Options: option_name (default_value)
    -------
    parent (None): parent widget
    title (''): figure title
    xlabel (''): X-axis label
    ylabel (''): Y-axis label
    xlim (None): X-axis limits ([min, max])
    ylim (None): Y-axis limits ([min, max])
    xscale ('linear'): X-axis scale
    yscale ('linear'): Y-axis scale
    width (4): width in inches
    height (3): height in inches
    dpi (100): resolution in dpi
    hold (False): if False, figure will be cleared each time plot is called
        axes.hold deprecated, clear axes/figure to remove "hold"

    Widget attributes:
    -----------------
    figure: instance of matplotlib.figure.Figure
    axes: figure axes

    Example:
    -------
    self.widget = MatplotlibWidget(self, yscale='log', hold=True)
    from numpy import linspace
    x = linspace(-10, 10)
    self.widget.axes.plot(x, x**2)
    self.widget.axes.plot(x, x**3)
    """
    def __init__(self, parent=None, title='', xlabel='', ylabel='',
                 xlim=None, ylim=None, xscale='linear', yscale='linear',
                 width=16, height=12, dpi=100, hold=False):

        self.figure = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.figure.add_subplot(111)
        self.axes.set_title(title)
        self.axes.set_xlabel(xlabel)
        self.axes.set_ylabel(ylabel)
        if xscale is not None:
            self.axes.set_xscale(xscale)
        if yscale is not None:
            self.axes.set_yscale(yscale)
        if xlim is not None:
            self.axes.set_xlim(*xlim)
        if ylim is not None:
            self.axes.set_ylim(*ylim)
        #  axes.hold deprecated, clear axes/figure to remove "hold"
        # self.axes.hold(hold)

        Canvas.__init__(self, self.figure)
        self.setParent(parent)

        Canvas.setSizePolicy(self, QSizePolicy.Expanding,
                             QSizePolicy.Expanding)
        Canvas.updateGeometry(self)

    def goPrinter(self):
        """
        prints the self.mpl widget, better to make a utility function
        and pass in self.mpl??
        """
        printer = QPrinter()

        printer.Letter
        printer.HighResolution
        printer.Color
        # 9feb2019, works ok without parent
        anotherWidget = QPrintDialog(printer)
        if(anotherWidget.exec_() == QDialog.Accepted):
            p = self.grab()
            printLabel = QLabel()
            printLabel.setPixmap(p)
            painter = QPainter(printer)
            rect = painter.viewport()
            size = printLabel.pixmap().size()
            size.scale(rect.size(), QtCore.Qt.KeepAspectRatio)
            painter.setViewport(rect.x(), rect.y(),
                                size.width(), size.height())
            painter.setWindow(printLabel.pixmap().rect())
            painter.drawPixmap(0, 0, printLabel.pixmap())
            del painter


# ===========================================================================
#   Example
# ===========================================================================
if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QMainWindow, QApplication
    from numpy import linspace

    class ApplicationWindow(QMainWindow):
        def __init__(self):
            QMainWindow.__init__(self)
            self.mplwidget = MatplotlibWidget(self, title='Example',
                                              xlabel='Linear scale',
                                              ylabel='Linear scale',
                                              hold=True, yscale='linear')
            self.mplwidget.setFocus()
            self.setCentralWidget(self.mplwidget)

            self.axes = self.mplwidget.axes

            # make the first two plots
            x = linspace(-10, 10)
            self.axes.plot(x, x * 2)
            self.axes.plot(x, x)

            # this will clear the axes (hold deprecated)
            # self.axes.clear()

            # make a third plot on second set of y axes.
            self.twinx = self.axes.twinx()
            self.twinx.plot(x, x**2)

    app = QApplication(sys.argv)
    win = ApplicationWindow()
    win.show()
    sys.exit(app.exec_())
