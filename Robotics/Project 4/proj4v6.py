from Interface import *
import threading

lock = threading.Lock()


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
    global clean
    lock.acquire()
    if Interface2().button('clean'):
        clean = not clean
    time.sleep(SLEEP_EXTENDED)
    print("CLEAN: " + str(clean))
    lock.release()


# Control the individual speed of the wheels
def drive_direct(lspeed, rspeed):
    lock.acquire()
    Interface2().drive_direct(lspeed, rspeed)
    lock.release()


def bumpers():
    lock.acquire()
    l_bumper = Interface2().bump_wheels('left')
    r_bumper = Interface2().bump_wheels('right')
    lock.release()
    return l_bumper, r_bumper


def song():
    lock.acquire()
    Interface2().song()
    lock.release()


def play_song():
    lock.acquire()
    Interface2().play_song()
    lock.release()


# Get the values for all the right light bump requests
def light():
    lock.acquire()
    light_right = Interface2().light_bump(LIGHT_RIGHT)
    while (light_right > 1000):
        light_right = 300
    lock.release()
    return light_right


def omni_value():
    lock.acquire()
    omni_v = Interface2().ir_omni()
    lock.release()
    return omni_v


def dock_red_value():
    lock.acquire()
    dock_red = Interface2().ir_right()
    lock.release()
    return dock_red


def dock_green_value():
    lock.acquire()
    dock_green = Interface2().ir_left()
    lock.release()
    return dock_green


def charging_state_value():
    global charging_state_v
    lock.acquire()
    charging_state_v = Interface2().charging_state()
    time.sleep(SLEEP_EXTENDED)
    lock.release()


# Global Constants
isMOVING = False
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


def hug_wall():
    print("entered hug wall")
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

    Interface2().drive_direct(RSPEED, LSPEED)
    time.sleep(sampling_time)


def dock():
    print("Dock Detected.")
    dock_red = dock_red_value()
    dock_green = dock_green_value()
    global LSPEED
    global RSPEED
    global charging_state_v

    l_bumper, r_bumper = bumpers()

    while charging_state_v <= 0 or (not l_bumper and r_bumper):
        print("Entered charging loop")

        dock_red = dock_red_value()
        dock_green = dock_green_value()

        print("CHARGING STATE: " + str(charging_state_v))
        omni_v = omni_value()
        print("OMNI: " + str(omni_v))

        print("Dock Green\t:" + str(dock_green) + "\tDock Red:\t" + str(dock_green))

        while dock_green - dock_red > 10:
            print("in g > r")
            Interface2().drive_direct(20, -20)
            dock_red = dock_red_value()
            dock_green = dock_green_value()
            l_bumper, r_bumper = bumpers()
            time.sleep(SLEEP_EXTENDED / 2)
            if l_bumper and r_bumper:
                stop()
                charging_state = 1
                break

        while dock_red - dock_green > 10:
            print("in r > g")
            Interface2().drive_direct(-20, 20)
            dock_red = dock_red_value()
            dock_green = dock_green_value()
            l_bumper, r_bumper = bumpers()
            time.sleep(SLEEP_EXTENDED / 2)
            if l_bumper and r_bumper:
                stop()
                charging_state = 1
                break

        while dock_red - dock_green < 10 or dock_red - dock_green < 10 or omni_v == 168:
            print("in r = g")
            Interface2().drive_direct(20, 20)
            dock_red = dock_red_value()
            dock_green = dock_green_value()
            l_bumper, r_bumper = bumpers()
            time.sleep(SLEEP_EXTENDED / 2)
            if l_bumper and r_bumper:
                stop()
                charging_state = 1
                break

        l_bumper, r_bumper = bumpers()
        print("Charging state:" + str(charging_state_v))

    stop()
    play_song()


Interface2().control('start')
Interface2().control('safe')
Interface2().control('full')
Interface2().song()

clean = True
charging_state_v = 0
clean_thread = threading.Thread(target=clean_state)
clean_thread.start()
charging_thread = threading.Thread(target=charging_state_value)
charging_thread.start()
clean_thread.join()
charging_thread.join()
while True:

    # Interface2().play_song()
    if not isMOVING and clean:
        isMOVING = True
        omni_v = omni_value()
        print("Entering loop")
        while omni_v <= 0:
            print("Looping")
            hug_wall()
            omni_v = omni_value()
        print("Omni V Detected: " + str(omni_v))

        dock()

        if charging_state_v > 0:
            stop()
            play_song()
            quit()

    if isMOVING and not clean:
        stop()
    # u = pd()
    # print("U value: " + str(u))
