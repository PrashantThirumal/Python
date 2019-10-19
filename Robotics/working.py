import serial
import struct
import time
import numpy as np
import threading

'''
Defining Global Variables
Baudrate - Default from Roomba documentation
Port number - Default from Serial
Sleep - The time for sleeping after sending an instruction. (Achieved through trial and error)
Sleep_extended - The time to sleep for an extended period of time
Byte - Helps isolate a byte
Byte_Size - Number of Bits in a byte of the Roomba (From Roomba Documentation)
Drive_Byte - Number of bytes for the drive command
'''
BAUDRATE = 115200
PORT = '/dev/ttyUSB0'
SLEEP = 0.0125
SLEEP_EXTENDED = 1
BYTE = 0xFF
BYTE_SIZE_BUTTON = 1
BYTE_SIZE_VELOCITY = 2
DRIVE_BYTES = 2
MAX_VEL = 500
MIN_VEL = -500
MAX_RAD = 2000
MIN_RAD = -2000

# The following OP codes are obtained from Roomba Documentation
# Packet ID to get button state obtained from Roomba Documentation
START = 128
RESET = 7
STOP = 173
PASSIVE = 128
SAFE = 131
SENSORS_OP = 142
BUTTONS_PACKET_ID = 18
VEL_ID = 41
DRIVE = 137

# These variables represent the different buttons on the Roomba
CLOCK = 0x80
SCHEDULE = 0x40
DAY = 0x20
HOUR = 0x10
MINUTE = 0x08
DOCK = 0x04
SPOT = 0x02
CLEAN = 0x01

'''
# Specifies default speed of the Roomba for our use
# Distance between wheels is the diameter of turn; from roomba documentation
# Radius of turn is 1/2 of diameter
# Counter_clockwise turn is specified by the Roomba documentation as 1
# Radius of turn to drive straight is 0
# Total distance the robot has to travel is 2m = 2000mm
# Total amount of degrees in a straight line, used for calculations
# Minimum number of Sides in a polygon
'''
SPEED = 150
DIAMETER = 235
TURN_RAD = DIAMETER / 2
CC_RAD = 1
STR_RADIUS = 0
TOT_DIST = 2000
STR_LINE = 180
MIN_SIDES = 3

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
        self.ser.baudrate = BAUDRATE  # From Roomba documentation notes
        self.ser.port = PORT
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
Task 2:
a. Control the state of the robot (Start, Reset, Stop, Passive, Safe).
b. Read the state of the buttons.
c. Send a Drive command to set the velocity and the radius of the wheels, given the two as
   arguments.
'''


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
            self.inter.write(chr(PASSIVE))
        if state.lower() == "safe":
            self.inter.write(chr(SAFE))

        # Sleep after setting the state
        time.sleep(SLEEP)

    # Send a request for buttons sensor packet (from Roomba documentation)
    # Read all 7 bits to get the state of the buttons
    # We sleep after sending the instruction to ensure we don't overload the Roomba
    def button(self, buttons):
        self.control('safe')
        self.inter.write(chr(SENSORS_OP) + chr(BUTTONS_PACKET_ID))
        y = self.inter.read(BYTE_SIZE_BUTTON)
        x = struct.unpack('B', y)[0]

        # Return the state of which button is specified
        if buttons.lower() == 'clean':
            clean = bool(x & CLEAN)
            return clean
        if buttons.lower() == 'spot':
            spot = bool(x & SPOT)
            return spot
        if buttons.lower() == 'dock':
            dock = bool(x & DOCK)
            return dock
        if buttons.lower() == 'minute':
            minute = bool(x & MINUTE)
            return minute
        if buttons.lower() == 'hour':
            hour = bool(x & HOUR)
            return hour
        if buttons.lower() == 'day':
            day = bool(x & DAY)
            return day
        if buttons.lower() == 'schedule':
            schedule = bool(x & SCHEDULE)
            return schedule
        if buttons.lower() == 'clock':
            clock = bool(x & CLOCK)
            return clock

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

# Before each method is a block comment explaining our processes

'''
# Checks the state of the button
# Infinite loop to continually check the clean button press
# Sleep each time it is pressed becuase the button is very sensitive, eliminates chance of double press
# Change global boolean CLEAN_STATE for threading with the drive function defined below
'''


def clean_state():
    global CLEAN_STATE
    while True:
        clean = Interface2().button('clean')
        if clean:
            CLEAN_STATE = not CLEAN_STATE
            time.sleep(SLEEP_EXTENDED)


# This method spins the Roomba counter-clockwise
def drive_cc(speed):
    Interface2().drive(speed, CC_RAD)


'''
# Given a distance, and with a speed of our choosing, we drive with both wheels at velocity = speed
# The time the robot drives = distance / speed (accounting for any discrepancies in the units)
'''


def drive_straight(distance, speed):
    t = float(distance) / speed
    Interface2().drive(speed, STR_RADIUS)
    # We sleep the Roomba the amount of time it would take to travel specified distance
    time.sleep(t)
    Interface2().control('stop')


'''
# Given an angle and with a speed of our choosing, we will use drive_cc to rotate counter-clockwise
# radians per sec is our angular velocity which equals speed of the wheels / our turn radius
# Then, our angular velocity is converted to degrees
# Finally, the time to turn = angle we want to turn / angular velocity
'''


def turn(angle, speed):
    radians_per_sec = float(speed) / TURN_RAD
    degrees_per_sec = np.rad2deg(radians_per_sec)
    # We get the float of time to be more precise
    t = float(angle) / degrees_per_sec
    # Turn the roomba counter-clockwise
    # Stop after the specified time is reached
    drive_cc(speed)
    time.sleep(t)
    Interface2().control('stop')


'''
# Uses the above functions to drive about a regular polygon with N sides
# We use the first infinite while loop to wait until the clean button is pressed to take in an input
# Once we have an number of sides, we start driving
# Our polygon method is threaded with the clean state method using global boolean CLEAN_STATE
# While CLEAN_STATE, the robot will drive normally, but when the clean button is pressed, the robot will stop -
# and wait for the clean button to be pressed again before continuing to finish the polygon
# We keep track of the number of sides the robot has already finished with the variable sides_remaining
'''


def polygon():
    Interface2().control('start')
    Interface2().control('safe')

    global CLEAN_STATE

    while True:
        if CLEAN_STATE:
            sides = int(input("Enter a value for N"))

            # Check for valid N
            if sides < MIN_SIDES:
                print("Invalid input N")
            break

    '''
    # The mathematical equations we used to figure out how much we time we must turn and go for
    # Total number of degrees inside a regular polygon = (number of sides - 2) * 180
    # Amount of degrees for each angle = total degrees / number of sides
    # Length of each side = total distance / number of sides
    '''

    angle = float(STR_LINE - float(((sides - 2) * STR_LINE) / sides))
    length = float(TOT_DIST / sides)
    sides_remaining = sides

    while True:
        while sides_remaining > 0 and CLEAN_STATE:
            drive_straight(length, SPEED)
            turn(angle, SPEED)
            sides_remaining -= 1

        if sides_remaining == 0:
            break


# Main method, implementing two threads in parallel

if __name__ == '__main__':
    CLEAN_STATE = False
    thread1 = threading.Thread(target=polygon)
    thread2 = threading.Thread(target=clean_state)
    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()
