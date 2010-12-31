import usb

from .cm15 import CM15

class USBScanner(object):
    devices = (CM15,)

    def findController(self):
        busses = usb.busses()
        for bus in busses:
            for dev in bus.devices:
                for X10Class in self.devices:
                    if dev.idVendor == X10Class.vendorId and \
                            dev.idProduct == X10Class.productId:
                        return X10Class(dev)

        return None
