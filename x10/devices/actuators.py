import math
from x10.protocol import functions

MIN_VOLTAGE = 0
MAX_VOLTAGE = 128

class AbstractX10Actuator(object):


    """
    These are used to store the history of the device as controlled by the script
    to guess the current state on non-bidirectional devices (devices which do 
    not respond to STATREQ and therefore on which there is no way to know the
    actual state)
     
    WARNING : these values can be invalidated at any moment by a manual operation
    on the device. Example: if somebody manualy turns the light on, on a LW11,
    the script will not know about it. The values must therefore be used as an
    "educated guess"
    """
    is_on = None
    voltage = None
    last_voltage = None

    def __init__(self, x10addr, aX10Controller):
        self.x10addr = x10addr
        self.x10ctrl = aX10Controller

#    def status(self):
#        """
#        Query for status
#        """
#        self.x10ctrl.do(functions.STATREQ, self.x10addr)
#        print self.x10ctrl.read()


class SwitchableX10Actuator(AbstractX10Actuator):
    def on(self):
        """
        Turn on
        """
        self.x10ctrl.do(functions.ON, self.x10addr)
        ack = self.x10ctrl.ack()
        if ack:
            self.is_on = True
            self.voltage = self.last_voltage
        return ack

    def off(self):
        """
        Turn off
        """
        self.x10ctrl.do(functions.OFF, self.x10addr)
        ack = self.x10ctrl.ack()
        if ack:
            self.is_on = False
            self.last_voltage = self.voltage
            self.voltage = MIN_VOLTAGE
        return ack

class DimmableX10Actuator(AbstractX10Actuator):
    def dim(self, amount):
        """
        Reduce voltage
        """
        self.x10ctrl.do(functions.DIM, self.x10addr, amount=amount)
        ack = self.x10ctrl.ack()
        if ack and self.voltage:
            self.voltage = max(MIN_VOLTAGE, self.voltage - amount)
        return ack

    def bright(self, amount):
        """
        Augment voltage
        """
        self.x10ctrl.do(functions.BRIGHT, self.x10addr, amount=amount)
        ack = self.x10ctrl.ack()
        if ack:
            if amount > 0:
                self.is_on = True
            if self.voltage:
                self.voltage = min(MAX_VOLTAGE, self.voltage + amount)
        return ack

    def adjust(self, amount):
        """
        Augment or reduce voltage
        """
        if amount > 0:
            ack = self.bright(amount)
        else:
            ack = self.dim(int(math.fabs(amount)))
        return ack

    def set(self, amount):
        """
        Sets the voltage at an absolute value. Should try to use extended codes in the future
        """

        # if we do not have an educated guess about the current voltage, we have
        # to turn off the device to start from 0
        if not self.voltage:
            self.off()

        self.adjust(amount - self.voltage)

class GenericX10Actuator(SwitchableX10Actuator,
                         DimmableX10Actuator):
    pass
