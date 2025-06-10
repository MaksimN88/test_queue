import sys
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QGroupBox,
    QHBoxLayout,
    QVBoxLayout,
)
from PySide6.QtCore import (
    Qt,
    Signal,
)
from PySide6.QtGui import QMouseEvent
from track import Track


class Slot(QWidget):

    slot_signal = Signal(list)

    def __init__(self, num_slot=None, **kwargs):
        super().__init__(**kwargs)
        self.num_slot = num_slot
        self.track = Track()
        self.track.track_signal.connect(self.forwarding)
        self.initializeUI()

    def initializeUI(self):
        self.setWindowTitle("Slot")
        self.setUpSlot()

    def setUpSlot(self):
        self.slot_list = []

        self.labels_list = []

        self.labels_gen = [QLabel() for label in range(1, 11)]

        for label in self.labels_gen:
            label.setText("0")
            self.labels_list.append(label)

        left_group_box = QGroupBox()

        left_box = QVBoxLayout()

        for label in self.labels_list:
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            left_box.addWidget(label)

        left_group_box.setLayout(left_box)

        self.name_side_label = QLabel(f"Slot {self.num_slot}")
        self.name_side_label.setStyleSheet(
            "border: black 1px solid; border-radius: 5px;"
        )
        self.name_side_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.name_side_label.setAlignment(Qt.AlignmentFlag.AlignBottom)
        self.name_side_label.installEventFilter(self)

        self.status_label = QLabel("FREE")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        r_box = QVBoxLayout()
        r_box.addWidget(self.name_side_label)
        r_box.addWidget(self.status_label)

        main_box = QHBoxLayout()
        main_box.addWidget(left_group_box)
        main_box.addLayout(r_box)

        self.setLayout(main_box)

    def eventFilter(self, object, event):
        if (
            isinstance(object, QLabel)
            and event.type() == QMouseEvent.Type.MouseButtonDblClick
        ):
            if self.track.isVisible():
                self.track.hide()
            else:
                if not self.track.isVisible():
                    self.track.show()
                else:
                    self.track.close()
                    self.track = Track()
                    self.track.track_signal.connect(self.forwarding)
                    self.track.show()
        return QWidget.eventFilter(self, object, event)

    def forwarding(self, list):
        if list:
            self.slot_list.append(self.num_slot)
            self.slot_list.append(list)
            self.slot_signal.emit(self.slot_list)
            self.status_label.setText("In the queue")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Slot()
    window.show()
    sys.exit(app.exec())
