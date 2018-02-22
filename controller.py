import serial
import RPi.GPIO as GPIO
import _thread


class Controller:
    def __init__(self, slave1_config, slave2_config):
        self.slave1 = serial.Serial("/dev/%s" % slave1_config[0], slave1_config[1])
        self.slave1.baudrate = 9600

        self.slave2 = serial.Serial("/dev/%s" % slave2_config[0], slave2_config[1])
        self.slave2.baudrate = 9600

        GPIO.setmode(GPIO.BOARD)

        self.painting = False

        self.handlers = {
            'BLINK': self._blink,
            'PAINT': self._paint,
            'MOVE_LEFT': self._move_left,
            'MOVE_RIGHT': self._move_right,
            'MOVE_UP': self._move_up,
            'MOVE_DOWN': self._move_down,
            'MOVE_FORWARD': self._move_forward,
            'MOVE_BACKWARD': self._move_backward,
            'LIFT_UP_PEN': self._lift_up_pen
        }

    def _move_forward(self):
        self._send(self.slave1, 'MOVE_FORWARD')

    def _move_backward(self):
        self._send(self.slave1, 'MOVE_BACKWARD')

    def _move_left(self, displacement):
        self._send(self.slave1, 'MOVE_LEFT %s' % displacement)

    def _move_right(self, displacement):
        self._send(self.slave1, 'MOVE_RIGHT %s' % displacement)

    def _move_up(self, displacement):
        self._send(self.slave1, 'MOVE_UP %s' % displacement)

    def _move_down(self, displacement):
        self._send(self.slave1, 'MOVE_DOWN %s' % displacement)

    def _lift_up_pen(self):
        self._send(self.slave2, 'LIFT_UP_PEN')

    def _paint(self):
        self._send(self.slave2, 'PAINT')

    def _blink(self):
        self._send(self.slave1, 'BLINK')

    def listen(self):
        _thread.start_new_thread(self._listen, (self.slave1,))
        _thread.start_new_thread(self._listen, (self.slave2,))

    def execute(self, command):
        print(command)
        arguments = command.split(' ')
        print(arguments)
        if len(arguments) > 1:
            command = arguments[0]
            displacement = arguments[1]
            self.handlers[command](displacement)
        else:
            self.handlers[command]()

    def _listen(self, slave):
        while True:
            line = slave.readline()
            print(line)

    def _send(self, slave, message):
        slave.write(("%s\n" % message).encode('utf-8'))
        slave.flush()
