# examples/oled_eyes.py
#
# Draw eyes on SwagBadge oleds
# Based on examples from aiko_engine_mp

# Usage
# ~~~~~
# Connect to SwagBadge with (something like) mpfshell
#   $ mpfshell -o ttyUSB0
# Upload this file, and run the code
#   mpfs [/]> put examples/oled_eyes.py
#   mpfs [/]> repl
#   MicroPython v1.13 on 2020-09-02; ESP32 module with ESP32
#   Type "help()" for more information.
#   >>> import examples.oled_eyes as eyes
#   >>> eyes.run()
#
# The software may take a few seconds to load and draw.
#
# To Do
# ~~~~~

import uos

import aiko.event as event
import aiko.oled as oled

import math

oled0 = oled.oleds[0]  # Left Eye
oled1 = oled.oleds[1]  # Right Eye

# offset = oled.font_size
# Assume left and right oleds are same size.
height = oled0.height
width = oled0.width

period = 1

# Utilities
def random(min, max, r_max=255):
    r = uos.urandom(1)[0] & r_max
    r = r / r_max * (max - min) + min
    if r >= max:
        r = min
    return int(r)

def random_position(limit):
    limit = limit // 4
    return random(limit, limit * 3)

#
def new_eyes():
    global eye_position
    eye_position = (random_position(width), random_position(height))

# Global time
ti = 0

def eyes_function(x,y):
    global ti

    # Geometry
    x0 = width / 2 + ti % 50 - 25
    y0 = height / 2
    r = 20
    r2 = r*r

    xr = x - x0
    yr = y - y0

    # Inside circle
    if (x > x0 - r) and (x < x0 + r):
        ys = math.ceil( math.sqrt( r2 - xr*xr ))
        if ((y > y0 - ys) and (y < y0 + ys)):
            return 1

    return 0

def display_eyes():
    global ti
    for x in range(0, width - 1):
        for y in range(0, height - 1):
            if eyes_function(x,y) == 1:
                oled0.pixel(x,y,1)
                oled1.pixel(x,y,1)
            else:
                 oled0.pixel(x,y,0)
                 oled1.pixel(x,y,0)
    ti = ti + 1

def update_eyes():
    display_eyes()

def timer_handler():
    update_eyes()
    oled0.show()
    oled1.show()

def run(period=50):
    oled.oleds_clear(0)

    new_eyes()
    display_eyes()

    event.add_timer_handler(timer_handler, period)
    try:
        event.loop()
    finally:
        event.remove_timer_handler(timer_handler)
