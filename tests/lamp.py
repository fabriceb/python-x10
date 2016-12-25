import sys
import logging
from x10.controllers.bus import USBScanner

logging.basicConfig(level=logging.DEBUG)

b = USBScanner()
dev = b.findController()
dev.open()

livinglamp = dev.actuator("A1")

if sys.argv[1] == "on":
  livinglamp.on()
else:
  livinglamp.off()

#roomlamp = dev.actuator("A2")
#roomlamp.on()

#roomlamp.on()

#livinglamp.off()

#livinglamp.adjust(100)

#house = dev.house("A")

#house.unitsOff()

#house.lightsOff()
#house.lightsOn()

#dev.close()






