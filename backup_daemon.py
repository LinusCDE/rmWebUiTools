import time


from daemoniker import Daemonizer

from status_window import StatusWindow
from usb_detector import USBDetector

from threading import Thread

window = StatusWindow()



class BackupDaemon(Thread):

    def __init__(self, queue, targetFolder, onlyNotebooks, onlyBookmarked, updateFiles, onlyPathPrefix):
        Thread.__init__(self)
        self.queue = queue
        self.targetFolder = targetFolder
        self.onlyNotebooks = onlyNotebooks
        self.onlyBookmarked = onlyBookmarked
        self.updateFiles = updateFiles
        self.onlyPathPrefix = onlyPathPrefix

    def run(self):
        #usb_detector = USBDetector()
        #usb_detector.detect_newly_added_usb_device()
        self.queue.put(show_status_window)
        #files = api.fetchFileStructure()
        #export.exportTo(files, self.targetFolder, self.onlyNotebooks, self.onlyBookmarked, self.updateFiles, self.onlyPathPrefix, window)
        self.test_update_window()

    def test_update_window(self):
        window.set_total_files(100)
        for i in range(100):
            window.update_status()
            time.sleep(1)


def start_daemon(queue, targetFolder, onlyNotebooks, onlyBookmarked, updateFiles, onlyPathPrefix):
    BackupDaemon(queue, targetFolder, onlyNotebooks, onlyBookmarked, updateFiles, onlyPathPrefix).start()


def show_status_window():
    window.mainloop()
