import sys
import logging
from x10.controllers.bus import USBScanner

logging.basicConfig(level=logging.DEBUG)

b = USBScanner()
dev = b.findController()
dev.open()

a = dev.actuator(sys.argv[1])

if sys.argv[2] == "on":
  a.on()
else:
  a.off()



