from daemoniker import Daemonizer

from status_window import StatusWindow
from usb_detector import USBDetector

PATH_TO_PID_FILE = "daemon.pid"

def handleDaemonArg(daemonArg):
    if daemonArg is 'start':
        startDaemon()
    elif daemonArg is 'stop':
        stopDaemon()
    elif daemonArg is 'restart':
        startDaemon()
        stopDaemon()

def startDaemon():
    print("Starting daemon...")
    with Daemonizer() as (is_setup, daemonizer):

        is_parent = daemonizer(
            PATH_TO_PID_FILE
        )

    usb_detector = USBDetector()
    usb_detector.detect_newly_added_usb_device()
    window = StatusWindow()
    window.mainloop()

def stopDaemon():
    print("Stopping daemon...")

startDaemon()