import serial
import struct
import time
import numpy as np
import random
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
SPEED = 150

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
DEFAULT_ANGLE = 180
UPPER_RAND_BOUND = 46
LOWER_RAND_BOUND = -45

# ************************************ DRIVING **************************************#
#
# Specifies the built in opcodes for uploading a song on the Roomba.
# Specifies the note names in lilypad notation that the Roomba has to play
# Specifies the measure time for each note and song
# Song played: Imperial March - Star wars
#
# *********************************************************************************#

# These variables represent the necessary parameters for the roomba to play a song
SONG = 140
PLAY_SONG = 141
SONG_ZERO = 0
SONG_ONE = 1
SONG_TWO = 2
SONG_THREE = 3
SONG_FOUR = 4
SONG_FIVE = 5

SONG_LEN_ONE = 9
SONG_LEN_TWO = 8
NOTE_NUM = 65  # This plays F note
NOTE_REST = 30  # rest note
NOTE_LEN = 8

# define silence
r = 30

# map note names in the lilypad notation to irobot commands
c4 = 60
cis4 = des4 = 61
d4 = 62
dis4 = ees4 = 63
e4 = 64
f4 = 65
fis4 = ges4 = 66
g4 = 67
gis4 = aes4 = 68
a4 = 69
ais4 = bes4 = 70
b4 = 71
c5 = 72
cis5 = des5 = 73
d5 = 74
dis5 = ees5 = 75
e5 = 76
f5 = 77
fis5 = ges5 = 78
g5 = 79
gis5 = aes5 = 80
a5 = 81
ais5 = bes5 = 82
b5 = 83
c6 = 84
cis6 = des6 = 85
d6 = 86
dis6 = ees6 = 87
e6 = 88
f6 = 89
fis6 = ges6 = 90

# define some note lengths
# change the top MEASURE (4/4 time) to get faster/slower speeds
MEASURE = 160
HALF = MEASURE / 2
Q = MEASURE / 4
E = MEASURE / 8
Ed = MEASURE * 3 / 16
S = MEASURE / 16
MEASURE_TIME = MEASURE / 64


# **************************** INTERFACE CLASS *****************************************#
#
#  Interface 1 - Intializes the Roomba. Sets up the serial connection
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

    # This method returns The distance that Roomba has traveled in millimeters
    # since the distance it was last requested
    def distance(self):
        self.inter.write(chr(SENSORS_OP) + chr(DISTANCE))
        y = self.inter.read(DRIVE_BYTES)
        time.sleep(SLEEP)
        data = struct.unpack('B', y)

        return data[0]

    def angle(self):
        self.inter.write(chr(SENSORS_OP) + chr(ANGLE))
        y = self.inter.read(ANGLE_BYTE)
        time.sleep(SLEEP)
        data = struct.unpack('B', y)

        return data[0]

    # This method specifies the drive ability of the Roomba
    def drive(self, velocity, radius):
        # First set the robot to safe mode
        self.control('start')
        time.sleep(SLEEP)
        self.control('safe')
        time.sleep(SLEEP)
        self.inter.write(struct.pack('>B2h', DRIVE, velocity, radius))

    def drive_direct(self, lvelocity, rvelocity):
        # Set to safe first
        self.control('safe')
        self.inter.write(struct.pack('>B2h', DRIVE_DIRECT, lvelocity, rvelocity))


    def ints2str(self, lst):
        MIN_LIST = 0
        MAX_LIST = 255
        '''
        Taking a list of notes/lengths, convert it to a string
        '''
        s = ""
        for i in lst:
            if i < MIN_LIST or i > MAX_LIST:
                raise Exception
            s = s + str(chr(i))
        return s

    # Upload songs onto the robot
    def song(self):
        print("Sending Songs please wait.....")
        self.inter.write(self.ints2str([SONG, SONG_ZERO, SONG_LEN_ONE,
                                        a4, Q, a4, Q, a4, Q, f4, Ed, c5, S,
                                        a4, Q, f4, Ed, c5, S, a4, Q]))

    def play_song(self):
        print("Playing the song now")
        # Play each song uploaded
        self.inter.write(self.ints2str([PLAY_SONG, SONG_ZERO]))


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

# Upload the song to the Roomba
def play_song():
    lock.acquire()
    Interface2().play_song()
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

# Find the time needed to turn given the angle
def turn_time(speed, angle):
    radians_per_sec = float(np.deg2rad(angle))
    ang_vel = float(speed + speed) / float(DIAMETER)
    t = float(radians_per_sec) / float(ang_vel)
    return t


# Randomly pick left or right
def left_or_right():
    random_direction = random.randint(0, 2)
    if random_direction == 0:
        return "counter clockwise"
    else:
        return "clockwise"

# This method calculates the total angle to turn
def angle_to_turn():
    # Pick a random angle between -45 to 45 degrees
    random_angle = random.randint(LOWER_RAND_BOUND, UPPER_RAND_BOUND)
    # Total angle to be turned
    tot_angle = DEFAULT_ANGLE + random_angle
    return tot_angle

# Special method to drive clockwise if left bumper is pressed
def drive_bumper_c():
    tot_angle = angle_to_turn()
    t = turn_time(SPEED, tot_angle)
    # Drive direct for specified time
    Interface2().drive_direct(SPEED, -SPEED)
    time.sleep(t)

# Special method to drive counter clockwise if right bumper is pressed
def drive_bumper_cc():
    tot_angle = angle_to_turn()
    t = turn_time(SPEED, tot_angle)
    Interface2().drive_direct(-SPEED, SPEED)
    time.sleep(t)

# Turn around clockwise
def turn_around_c():
    tot_angle = DEFAULT_ANGLE
    t = turn_time(SPEED, tot_angle)
    Interface2().drive_direct(SPEED, -SPEED)
    time.sleep(t)

# Turn around counter clockwise
def turn_around_cc():
    tot_angle = DEFAULT_ANGLE
    t = turn_time(SPEED, tot_angle)
    Interface2().drive_direct(-SPEED, SPEED)
    time.sleep(t)


# Checks if the wheel has been dropped
# Checks each bumper individually, we want to produce different results per bumper
def bumpers_and_wheels():
    lock.acquire()
    wheel_drop = False
    if Interface2().bump_wheels('lwheel') or Interface2().bump_wheels('rwheel'):
        wheel_drop = True
    left_bumper = Interface2().bump_wheels('left')
    right_bumper = Interface2().bump_wheels('right')
    lock.release()
    return wheel_drop, left_bumper, right_bumper


# Constantly check for cliffs
def surroundings():
    lock.acquire()

    cliff_left = Interface2().cliff(CLIFF_LEFT)
    cliff_right = Interface2().cliff(CLIFF_RIGHT)
    cliff_fleft = Interface2().cliff(CLIFF_FLEFT)
    cliff_fright = Interface2().cliff(CLIFF_FRIGHT)

    if (cliff_left + cliff_right + cliff_fleft + cliff_fright) != 0:
        cliff = True
    else:
        cliff = False

    lock.release()
    return cliff


def random_walk():
    global isMoving

    while isMoving:
        Interface2().drive_direct(SPEED, SPEED)
        wheel_drop, left_bump, right_bump = bumpers_and_wheels()
        cliff = surroundings()

        if wheel_drop:
            Interface2().control('full')
            play_song()
            stop()
            isMoving = False
            break

        if cliff:
            Interface2().control('full')
            play_song()
            stop()
            direction = left_or_right()

            if direction == 'clockwise':
                turn_around_c()
            else:
                turn_around_cc()

        elif left_bump and right_bump:
            direction = left_or_right()

            if direction == 'clockwise':
                drive_bumper_c()
            else:
                drive_bumper_cc()

        elif left_bump:
            drive_bumper_c()

        elif right_bump:
            drive_bumper_cc()


if __name__ == '__main__':
    # Interface2().control('reset')
    isMoving = False
    print("Initalizing iCreate2........")
    Interface2().control('start')
    Interface2().control('safe')
    Interface2().control('full')
    print("Uploading songs.........")
    #song()

    print("Starting now.....")
    while True:
        clean = clean_state()
        wheel_drop, left_bump, right_bump = bumpers_and_wheels()
        cliff = surroundings()
        print("CLEAN: " + str(clean))
        print("WHEEL DROP: " + str(wheel_drop))
        print("CLIFF: " + str(cliff))
        print("LEFT BUMP: " + str(left_bump))
        print("RIGHT BUMP: " + str(right_bump))

        if not isMoving and not wheel_drop and not cliff and clean:
            print("starting thread")
            thread1 = Thread(target=random_walk)
            isMoving = True
            thread1.start()
            print("Thread started ")

        elif isMoving and clean:
            isMoving = False
            print("Stopping now")
            stop()
