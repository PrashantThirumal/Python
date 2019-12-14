'''
Written by Prashant Thirumal
'''
import serial
import struct
import time
import numpy as np
from threading import Thread, Lock

lock = Lock()

# ********************************** SERIAL *************************************#
#
#  These variables set the port configuration of the Roomba
#  Sleep is set to 15 ms as the Roomba's sensors update every 15 ms
#  Sleep Extended basically sleeps the Roomba for an extended period of time
#
# ******************************************************************************#
BAUDRATE = 115200
PORT = '/dev/ttyUSB0'
SLEEP = 0.0150
SLEEP_EXTENDED = 1

# The following OP codes are obtained from Roomba Documentation
# ********************************** STATE *************************************#
#
#  Various opcodes for controlling the state of the robot. These can be passed
#  directly as arguments into control_state to change the operational state of
#  the robot.
#
# ******************************************************************************#
START = 128
RESET = 7
STOP = 173
FULL = 132
PASSIVE = 128
SAFE = 131

# ********************************** READING DATA  *******************************#
#
#  Various opcodes and packet id to read button press, wheel drop, bump and cliff
#  Number of Bytes specified to be used with struct unpack. Byte helps isolate
#  a single byte
#
# ******************************************************************************#

SENSORS_OP = 142
BYTE = 0xFF
BYTE_SIZE_BUTTON = 1
BYTE_SIZE_BUMPS = 1
BYTE_SIZE_VELOCITY = 2
DRIVE_BYTES = 2
ANGLE_BYTE = 2

# *********************************** BUTTONS *********************************#
#
# BIT:   | 7     | 6        | 5    | 4    | 3      | 2    | 1    | 0     |
# VALUE: | CLOCK | SCHEDULE | DAY  | HOUR | MINUTE | DOCK | SPOT | CLEAN |
#
# Hex values are used to do bitwise "and" to check the if button has been pressed
# *****************************************************************************#

BUTTONS_PACKET_ID = 18
CLOCK = 0x80
SCHEDULE = 0x40
DAY = 0x20
HOUR = 0x10
MINUTE = 0x08
DOCK = 0x04
SPOT = 0x02
CLEAN = 0x01

# ***************************** BUMPERS AND WHEEL DROPS *************************#
#
# BIT:   | 7-6-5-4  | 3         | 2          | 1         | 0          |
# VALUE: | RESERVED | DROP LEFT | DROP RIGHT | BUMP LEFT | BUMP RIGHT |
#
# ********************************************************************************#

BUMPERS_PACKET_ID = 7
RIGHT_BUMPER = 0x01
LEFT_BUMPER = 0x02
RIGHT_WHEEL = 0x04
LEFT_WHEEL = 0x08

# ****************************** CLIFF SENSORS ***********************************#
#
# Returns a single bit, 0 = false, 1 = true
# Packets
# Each location left, front left, right, front right, virtual wall has its own
# Packet ID which must be called and a single bit to read
#
# *********************************************************************************#

CLIFF = 0x01
CLIFF_LEFT = 9
CLIFF_FLEFT = 10
CLIFF_FRIGHT = 11
CLIFF_RIGHT = 12
V_WALL = 13
WALL = 8

# ****************************** LIGHT BUMPER SENSORS *************************************#
#
# Packets
# Each location left, front left, right, front right, has its own
# Packet ID which must be called and a single bit to read
# Strength of the light bump is returned as an unsigned 16-bit value, high byte first
# 2 Bytes are returned
#
# ****************************************************************************************#

INFRARED_PACK = 17  # Omnidirectional infrared beacon
LIGHT_LEFT = 46
LIGHT_FRONT_LEFT = 47
LIGHT_CENTER_LEFT = 48
LIGHT_CENTER_RIGHT = 49
LIGHT_FRONT_RIGHT = 50
LIGHT_RIGHT = 51
LIGHT_BYTES = 2

# ************************************ DRIVING **************************************#
#
# Specifies the built in opcodes for driving the Roomba straight, turning clockwise
# and turning counter clockwise
# Specifies the minimum and maximum velocity and radius
# Packet ID to read distance passed and angle turned the last time it was requested
# Specifies Default Speed of the Roomba that we set it to -> 100 mm/s
#
# *********************************************************************************#

DRIVE = 137
DRIVE_DIRECT = 145
VEL_ID = 41
CC_RAD = 1
C_RAD = 0
MAX_VEL = 500
MIN_VEL = -500
MAX_RAD = 2000
MIN_RAD = -2000
DISTANCE = 19
ANGLE = 20
SPEED = 50

# ********************************* DRIVING PART 2 *********************************#
#
# Theses are more specific variables for driving the Roomba and is unique to Project 2
#
# To turn the Roomba a specific angle, we need the distance between the wheels and
# turn radius. We use these values in our differential drive equation
#
# Default angle is set to 180 so the Roomba just turns around
#
# We need to pick a random angle between -45 and 45 degrees. Hence we specified the upper
# and lower angle bound to use with math.random Note: Upper is exclusive and lower is
# inclusive
#
# *********************************************************************************#
DIAMETER = 235
TURN_RAD = DIAMETER / 2
STR_RADIUS = 0
DEFAULT_ANGLE = 90
UPPER_RAND_BOUND = 46
LOWER_RAND_BOUND = -45


# **************************** INTERFACE CLASS *****************************************#
#
#  Interface 1 - Initializes the Roomba. Sets up the serial connection
#  Interface 2 - Expanded version from project 1
# Following Methods Included:
#
#   control: Sets the Roomba to the specified state
#
#   button: checks for pressing of the specified button
#       returns a boolean: true if the buttons is pressed
#
#   bump_wheels: checks for bumps and wheel drops:
#      returns four booleans:
#      left wheel drop, right wheel drop, bump left, bump right
#
#   cliff: checks the specified cliff sensor.
#       returns an int: 1 = Specified cliff sensor is activated
#
#   light_bump: checks the specified light bump sensor
#       returns an unsigned 16 bit value, high byte first
#
#   angle: returns, in two bytes, the total degrees the robot
#       has turned since the function was last called.
#
#   distance: returns, in two bytes, the total millimeters the robot
#       has traveled since the function was last called.
#
#   drive: Drives the Roomba forwards or backwards given a specific velocity
#
#   drive_direct: Specifies the left wheel and the right wheel's velocity
#
#   ints2str: Converts a list to a string to write to the Roomba
#
#   song_upload: Uploads a song to the roomba to be played late
#
#   plat_song: Plays the uploaded song
# ******************************************************************************#
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


class Interface2:
    def __init__(self):
        self.inter = Interface()

    # Get the state and ignore case of argument passed
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
        if state.lower() == "full":
            self.inter.write(chr(FULL))

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
        time.sleep(SLEEP)

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

    # Send a request for bumpers and wheel drops sensor packet (from Roomba documentation)
    def bump_wheels(self, bumper):
        # self.control('safe')
        self.inter.write(chr(SENSORS_OP) + chr(BUMPERS_PACKET_ID))
        y = self.inter.read(BYTE_SIZE_BUMPS)
        x = struct.unpack('B', y)[0]
        time.sleep(SLEEP)

        if bumper.lower() == 'left':
            left_bumper = bool(x & LEFT_BUMPER)
            return left_bumper
        if bumper.lower() == 'right':
            right_bumper = bool(x & RIGHT_BUMPER)
            return right_bumper
        if bumper.lower() == 'lwheel':
            left_wheel = bool(x & LEFT_WHEEL)
            return left_wheel
        if bumper.lower() == 'rwheel':
            right_wheel = bool(x & RIGHT_WHEEL)
            return right_wheel

    # Send a request for cliff sensors
    def cliff(self, cliff_packet):
        # self.control('safe')
        self.inter.write(chr(SENSORS_OP) + chr(cliff_packet))
        y = self.inter.read(BYTE_SIZE_BUTTON)
        time.sleep(SLEEP)
        x = struct.unpack('B', y)[0]

        return x  # 0 = no cliff 1 = cliff

    # Send a request for the light bump sensors
    def light_bump(self, light_packet):
        self.inter.write(chr(SENSORS_OP) + chr(light_packet))
        y = self.inter.read(LIGHT_BYTES)
        x = struct.unpack('>H', y)[0]
        return x

    def drive_direct(self, lvelocity, rvelocity):
        # Set to safe first
        self.control('safe')
        self.inter.write(struct.pack('>B2h', DRIVE_DIRECT, lvelocity, rvelocity))


# ************************************ HELPER METHODS **************************************#
#
# We use semaphores to avoid synchronisation problems
# Cliffs, wheels, bumpers and clean all need to read and write to the roomba
# By locking the specific method each time it is used, we prevent multiple threads
# from overloading the Roomba
#
# Following Methods Included:
#   turn_time: Given the velocity and angle, we find the time needed to turn Roomba
#              This method goes by the differential drive formula
#
#   clean_state: Checks specifically for clean button press
#
# ********************************************************************************************#

# Stops the robot
def stop():
    lock.acquire()
    Interface2().control("stop")
    lock.release()


# Check if the clean button has been pressed
# Sleep whenever it is pressed because it is very sensitive
def clean_state():
    lock.acquire()
    clean = Interface2().button('clean')
    time.sleep(SLEEP_EXTENDED)
    lock.release()
    return clean


# Control the individual speed of the wheels
def drive_direct(lspeed, rspeed):
    Interface2().drive_direct(lspeed, rspeed)


# Get the values for all the right light bump requests
def light():
    lock.acquire()
    light_right = Interface2().light_bump(LIGHT_RIGHT)
    lock.release()
    return light_right


# Calculate the turn time for a 90 degree angle turn
def turn_time(speed, angle):
    radians_per_sec = float(np.deg2rad(angle))
    ang_vel = float(speed + speed) / float(DIAMETER)
    t = float(radians_per_sec) / float(ang_vel)
    return t


# Special method to drive clockwise if left bumper is pressed
def turn_c():
    tot_angle = DEFAULT_ANGLE
    t = turn_time(SPEED, tot_angle)
    # Drive direct for specified time
    Interface2().drive_direct(SPEED, -SPEED)
    time.sleep(t)
    stop()


# Special method to drive counter clockwise if right bumper is pressed
def turn_cc():
    tot_angle = DEFAULT_ANGLE
    t = turn_time(SPEED, tot_angle)
    Interface2().drive_direct(-SPEED, SPEED)
    time.sleep(t)
    stop()


def bumps():
    lock.acquire()
    lbump = Interface2().bump_wheels('left')
    rbump = Interface2().bump_wheels('right')
    lock.release()
    return lbump, rbump


# Global Constants
isMOVING = True
l_bumper = False
r_bumper = False
LSPEED = 50
RSPEED = 50

set_point = 300
past_error = 0
error = 0
sampling_time = 0.25
# original kp = 0.016, kd=0.002
kp = 0.016
kd = 0.002


# PD Controller
# Determines what to based on sensor readings
def pd():
    global error
    global past_error
    light_right = light()
    '''
    print('LIGHT_RIGHT: ' + str(light_right))
    print("LIGHT_FRONT_R: " + str(light_front_right))
    print("LIGHT_CENTER_R: " + str(light_center_right))
    '''
    print('LIGHT_RIGHT: ' + str(light_right))

    # Update last error
    past_error = error
    error = set_point - light_right
    print("LIGHT RIGHT: " + str(light_right))
    print("ERROR: " + str(error))
    # Proportional Controller
    P = kp * error
    # Derivative Controller
    D = (kd * (error - past_error)) / sampling_time
    # Controller output
    u = P
    print("U Value: " + str(u))
    return int(u)


def wall():
    print("entered wall")
    global isMOVING
    global l_bumper
    global r_bumper
    global LSPEED
    global RSPEED

    # drive_direct(LSPEED, RSPEED)
    l_bumper, r_bumper = bumps()
    print("l_bumper: " + str(l_bumper))
    print("r_bumper: " + str(r_bumper))
    if r_bumper:
        turn_cc()

    elif l_bumper:
        turn_c()

    u = pd()

    if u > 5:
        LSPEED = 35
        RSPEED = 25

    elif 3.5 <= u <= 5:
        LSPEED = 100 + u
        RSPEED = 40 - u

    else:
        LSPEED = 40 + u
        RSPEED = 40 - u

    if isMOVING:
        drive_direct(RSPEED, LSPEED)
        time.sleep(sampling_time)


# Interface2().control('reset')

Interface2().control('start')
Interface2().control('safe')
Interface2().control('full')

while True:
    wall()
