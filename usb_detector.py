import sys
import time

import usb.core

import threading

from status_window import StatusWindow


class USBDetector():

    def get_usb_devices(self):
        devs = []
        busses = usb.busses()
        for bus in busses:
            devices = bus.devices
            for dev in devices:
                devs.append((dev.idVendor, dev.idProduct))
        return devs


    def get_diff(self, old_list, new_list):
        return list(set(old_list) - set(new_list))


    def check_if_remarkable(self, dev):
        return dev[0] == 0x04B3 and dev[1] == 0x4010


    def detect_newly_added_usb_device(self):
        print("Insert Remarkable now.")
        print("Waiting...")
        devs = self.get_usb_devices()
        while True:
            time.sleep(1)
            devs_new = self.get_usb_devices()
            # print("Removed: ", get_diff(devs, devs_new))
            # print("Added: ", get_diff(devs_new, devs))
            added_devs = self.get_diff(devs_new, devs)
            if len(added_devs) > 0:
                for added_dev in added_devs:
                    if self.check_if_remarkable(added_dev):
                        print("Remarkable detected!")
                        return added_dev
            devs = devs_new



