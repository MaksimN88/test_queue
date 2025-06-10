import sys
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QGridLayout,
    QHBoxLayout,
    QMainWindow,
)

from slot import Slot
from worker import Worker
import queue


class MainWindow(QMainWindow):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.queue = queue.Queue()
        self.worker = Worker(self.queue)
        self.initializeUI()

    def initializeUI(self):
        self.setWindowTitle("Main Window")
        self.setUpMainWindow()

    def setUpMainWindow(self):

        self.slots_list = []

        self.slots_list_gen = [Slot(i) for i in range(1, 7)]

        for slot in self.slots_list_gen:
            slot.slot_signal.connect(self.receiving)
            self.slots_list.append(slot)

        self.slot_hbox_list = []
        hbox = [QHBoxLayout() for i in range(6)]
        for index, box in enumerate(hbox):
            box.addWidget(self.slots_list[index])
            self.slot_hbox_list.append(box)

        self.slot_widget_list = []
        widgets = [QWidget() for i in range(6)]
        for index, widget in enumerate(widgets):
            widget.setLayout(self.slot_hbox_list[index])
            self.slot_widget_list.append(widget)

        grid = QGridLayout()
        for row in range(2):
            if row == 0:
                for col in range(3):
                    grid.addWidget(self.slot_widget_list[col], row, col)
            elif row == 1:
                for col in range(3):
                    grid.addWidget(self.slot_widget_list[col + 3], row, col)

        self.setLayout(grid)

        self.workspace = QWidget()
        self.workspace.setLayout(grid)

        container = QWidget()
        container.setLayout(grid)
        self.setCentralWidget(container)

    def worker_thread(self):
        self.worker.update_value_signal.connect(self.updateValue)
        self.worker.update_status_slot_signal.connect(self.updateStatus)
        self.worker.start()

    def receiving(self, list):
        self.queue.put(list)
        self.worker_thread()

    def updateValue(self, num_slot, num_label, value):
        self.slots_list[num_slot].labels_list[num_label].setText(value)

    def updateStatus(self, num_slot, value):
        self.slots_list[num_slot].status_label.setText(value)

    def closeEvent(self, event):
        if event:
            if self.worker.isRunning():
                self.worker.stopRunning()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
