from PySide6.QtCore import (
    Signal,
    QThread,
)


class Worker(QThread):

    update_value_signal = Signal(int, int, str)
    update_status_slot_signal = Signal(int, str)

    def __init__(self, queue):
        super().__init__()
        self.queue = queue

    def stopRunning(self):
        self.terminate()
        self.wait()

    def run(self):
        while self.queue:
            self.general_list = self.queue.get()
            self.num_slot = self.general_list[0] - 1
            self.labels_list = self.general_list[1]
            self.update_status_slot_signal.emit(self.num_slot, "In progress")
            for label in self.labels_list:
                self.num_label = label
                self.value = str(self.num_label + 1)
                self.update_value_signal.emit(self.num_slot, self.num_label, self.value)
                self.sleep(4)
            self.queue.task_done()
            self.labels_list.clear()
            self.update_status_slot_signal.emit(self.num_slot, "Completed")
