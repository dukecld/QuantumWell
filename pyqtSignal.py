import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QPushButton, QLabel,
    QStackedWidget, QAction
)
from PyQt5.QtCore import pyqtSignal


# ---------------------------
# Stack Page A
# ---------------------------
class PageA(QWidget):
    # define a signal that sends a string
    parameters_changed = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        self.button = QPushButton("Send from Page A")
        self.button.clicked.connect(self.emit_signal)

        layout.addWidget(QLabel("Page A"))
        layout.addWidget(self.button)
        self.setLayout(layout)

    def emit_signal(self):
        value = "Data from Page A"
        self.parameters_changed.emit(value)


# ---------------------------
# Stack Page B
# ---------------------------
class PageB(QWidget):
    parameters_changed = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        self.button = QPushButton("Send from Page B")
        self.button.clicked.connect(self.emit_signal)

        layout.addWidget(QLabel("Page B"))
        layout.addWidget(self.button)
        self.setLayout(layout)

    def emit_signal(self):
        value = "Data from Page B"
        self.parameters_changed.emit(value)


# ---------------------------
# Main Window
# ---------------------------
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Stacked Widget Signal Example")

        # central widget
        central = QWidget()
        layout = QVBoxLayout()

        # label to show received data
        self.output_label = QLabel("Waiting for data...")
        layout.addWidget(self.output_label)

        # stacked widget
        self.stack = QStackedWidget()
        layout.addWidget(self.stack)

        central.setLayout(layout)
        self.setCentralWidget(central)

        # create pages
        self.page_a = PageA()
        self.page_b = PageB()

        self.stack.addWidget(self.page_a)
        self.stack.addWidget(self.page_b)

        # connect signals from pages → main window
        self.page_a.parameters_changed.connect(self.handle_parameters)
        self.page_b.parameters_changed.connect(self.handle_parameters)

        # menu to switch pages
        menu = self.menuBar().addMenu("Pages")

        action_a = QAction("Page A", self)
        action_b = QAction("Page B", self)

        action_a.triggered.connect(lambda: self.stack.setCurrentWidget(self.page_a))
        action_b.triggered.connect(lambda: self.stack.setCurrentWidget(self.page_b))

        menu.addAction(action_a)
        menu.addAction(action_b)

    # slot that receives signals
    def handle_parameters(self, value):
        self.output_label.setText(f"Received: {value}")


# ---------------------------
# Run app
# ---------------------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.resize(400, 300)
    window.show()
    sys.exit(app.exec_())