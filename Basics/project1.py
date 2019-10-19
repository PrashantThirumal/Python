import serial
import struct
import time
import pprint

'''
Defining Global Variables
Baudrate - Default from Roomba documentation
Port number - Default from Serial
Sleep - The time for sleeping after sending an instruction. (Achieved through trial and error)
Byte - Helps isolate a byte
Byte_Size - Number of Bits in a byte of the Roomba (From Roomba Documentation)
Drive_Byte - Number of bytes for the drive command
'''
BAUDRATE = 115200
PORT = '/dev/ttyUSB0'
SLEEP = 0.0125
BYTE = 0xFF
BYTE_SIZE = 1
DRIVE_BYTES = 2
MAX_VEL = 500
MIN_VEL = -500
MAX_RAD = 2000
MIN_RAD = -2000

'''
Task 1:
a. Connection to the serial interface
b. Sending of commands
c. Reading the data
d. Close the connection
'''


class Interface:
    def __init__(self):
        # Connect to the serial interface
        self.ser = serial.Serial()
        self.ser.baudrate = 115200  # From Roomba documentation notes
        self.ser.port = '/dev/ttyUSB0'
        self.ser.open()

    # Send a command to the roomba
    def write(self, instr):
        self.ser.write(instr)

    # Read the data from the roomba
    # Specify which bits we need to read
    def read(self, num):
        x = self.ser.read(num)
        return x

    # Close the connection
    def close(self):
        self.ser.close()


'''
Code to test Task 1
Roomba = Interface()
Roomba.write(chr(135))
'''

'''
Task 2:
a. Control the state of the robot (Start, Reset, Stop, Passive, Safe).
b. Read the state of the buttons.
c. Send a Drive command to set the velocity and the radius of the wheels, given the two as
   arguments.
'''

# The following OP codes are obtained from Roomba Documentation
# Packet ID to get button state obtained from Roomba Documentation
START = 128
RESET = 7
STOP = 173
SAFE = 131
BUTTONS_OP = 142
BUTTONS_ID = 18
DRIVE = 137

# These variables represents the different buttons on the Roomba
CLOCK = 0x80
SCHEDULE = 0x40
DAY = 0x20
HOUR = 0x10
MINUTE = 0x08
DOCK = 0x04
SPOT = 0x02
CLEAN = 0x01


class Interface2:
    def __init__(self):
        self.inter = Interface()

    # Get the state and ignore case of argument passed
    # OPcodes for respective states are from Roomba documentation
    def control(self, state):
        if state.lower() == "start":
            self.inter.write(chr(START))
        if state.lower() == "reset":
            self.inter.write(chr(RESET))
        if state.lower() == "stop":
            self.inter.write(chr(STOP))
        if state.lower() == "passive":
            self.inter.write(chr(128))
        if state.lower() == "safe":
            self.inter.write(chr(SAFE))

    # Send a request for buttons sensor packet (from Roomba documentation)
    # Read all 7 bits to get the state of the buttons
    # We sleep after sending the instruction to ensure we don't overload the Roomba
    def button(self):
        self.control('safe')
        self.inter.write(chr(BUTTONS_OP) + chr(BUTTONS_ID))
        time.sleep(SLEEP)
        y = self.inter.read(BYTE_SIZE)

        x = struct.unpack('B', y)[0]

        # Define a list of bool for the buttons
        clean = bool(x & CLEAN)
        spot = bool(x & SPOT)
        dock = bool(x & DOCK)
        minute = bool(x & MINUTE)
        hour = bool(x & HOUR)
        day = bool(x & DAY)
        schedule = bool(x & SCHEDULE)
        clock = bool(x & CLOCK)

        buttons_names_list = ["CLEAN:", "SPOT", "DOCK:", "MINUTE:", "HOUR:", "DAY:", "SCHEDULE:", "CLOCK: "]
        buttons_values_list = [clean, spot, dock, minute, hour, day, schedule, clock]
        for result, val in zip(buttons_names_list, buttons_values_list):
            print('{:<30}{:>40}'.format(result, val))
        return clean, spot, dock, minute, hour, day, schedule, clock








    # This method specifies the drive ability of the Roomba
    def drive(self, velocity, radius):
        # First set the robot to safe mode
        self.control('start')
        time.sleep(SLEEP)
        self.control('safe')
        time.sleep(SLEEP)
        # Roomba documentation specifies that we need to do a particular conversion
        # Desired value to twos comp to hex, split into two bytes and convert to decimal
        # Hence we use struct to pack the data and send it to the Roomba
        self.inter.write(struct.pack('>B2h', DRIVE, velocity, radius))


'''
Task 3:
a. Initialize the robot by setting it in passive and safe mode
b. If the robot is stopped, once the clean/power button is pressed, given an input N, move
   counterclockwise along a regular polygon with N sides and total perimeter of 2m
   (meters). The robot stops once the polygon is covered.
c. If the robot is moving, when the clean/power button is pressed, stop the robot when it
   reaches the current goal vertex.
'''
roomba = Interface2()
while True:
    print(roomba.button())
'''
class Robot:
    def __init__(self):
        self.inter = Interface2()
'''
