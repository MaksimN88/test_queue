import sys
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QCheckBox,
    QHBoxLayout,
    QVBoxLayout,
)
from PySide6.QtCore import Signal


class Track(QWidget):

    track_signal = Signal(list)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.initializeUI()

    def initializeUI(self):
        self.setWindowTitle("Track")
        self.setUpTrack()

    def setUpTrack(self):

        self.track_process_list = []

        self.track_cboxs = [QCheckBox(f"Track {i}") for i in range(1, 11)]

        center_box = QVBoxLayout()
        for cbox in self.track_cboxs:
            center_box.addWidget(cbox)

        self.launch_button = QPushButton("Launch")
        self.launch_button.clicked.connect(self.launchUp)

        center_box.addWidget(self.launch_button)

        main_box = QHBoxLayout()
        main_box.addLayout(center_box)

        self.setLayout(main_box)

    def launchUp(self):

        for cbox in self.track_cboxs:
            if cbox.isChecked():
                ind1 = self.track_cboxs.index(cbox)
                self.track_process_list.append(ind1)

        self.track_signal.emit(
            self.track_process_list,
        )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Track()
    window.show()
    sys.exit(app.exec())
