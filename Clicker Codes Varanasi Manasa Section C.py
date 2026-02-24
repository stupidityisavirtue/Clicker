from machine import Pin
import neopixel
import time

start_btn = Pin(13, Pin.IN, Pin.PULL_UP)
p1_btn = Pin(14, Pin.IN, Pin.PULL_UP)
p2_btn = Pin(27, Pin.IN, Pin.PULL_UP)

ir1 = Pin(35, Pin.IN)
ir2 = Pin(32, Pin.IN)

pixels = neopixel.NeoPixel(Pin(4), 16)

p1_life1 = Pin(26, Pin.OUT)
p1_life2 = Pin(15, Pin.OUT)
p1_life3 = Pin(5, Pin.OUT)

p2_life1 = Pin(21, Pin.OUT)
p2_life2 = Pin(18, Pin.OUT)
p2_life3 = Pin(25, Pin.OUT)

p1_indicator = Pin(22, Pin.OUT)
p2_indicator = Pin(23, Pin.OUT)

#GAME VARIABLES  (Makes it easier to go through it)
p1_score = 0
p2_score = 0
p1_lives = 0
p2_lives = 0
p1_active = True
p2_active = True
reaction_active = False
reaction_start = 0


#FUNCTIONS I used global here as I wanted to define a variable outside the function cuz It kept showing error inside)

def reset_game():
    global p1_score, p2_score, p1_lives, p2_lives
    global p1_active, p2_active, reaction_active

    p1_score = 0
    p2_score = 0
    p1_lives = 0
    p2_lives = 0
    p1_active = True
    p2_active = True
    reaction_active = False

    # Clear NeoPixels
    for i in range(16):
        pixels[i] = (0, 0, 0)
    pixels.write()

    # Turn off life LEDs
    p1_life1.off()
    p1_life2.off()
    p1_life3.off()
    p2_life1.off()
    p2_life2.off()
    p2_life3.off()

    # Turn off indicators
    p1_indicator.off()
    p2_indicator.off()


def update_scoreboard():
    for i in range(8):
        pixels[i] = (0, 255, 0) if i < p1_score else (0, 0, 0)
        pixels[i+8] = (0, 0, 255) if i < p2_score else (0, 0, 0)
    pixels.write()


def update_lives():
    p1_life1.value(p1_lives >= 1)
    p1_life2.value(p1_lives >= 2)
    p1_life3.value(p1_lives >= 3)

    p2_life1.value(p2_lives >= 1)
    p2_life2.value(p2_lives >= 2)
    p2_life3.value(p2_lives >= 3)


# START  (Using while true loop cuz I need this system to work without breaking cuz start and reset with work)
reset_game()

while True:

    # Reset anytime
    if start_btn.value() == 0:
        reset_game()
        time.sleep(0.5)

    # Round activation
    if ir1.value() == 1:

        while ir2.value() == 0:
            pass

        reaction_active = True
        reaction_start = time.ticks_ms()

        # Turn ON indicators
        if p1_active:
            p1_indicator.on()
        if p2_active:
            p2_indicator.on()

    # Reaction window
    if reaction_active:

        elapsed = time.ticks_diff(time.ticks_ms(), reaction_start)

        if elapsed <= 1000:

            if p1_btn.value() == 0 and p1_active:
                p1_score += 1
                update_scoreboard()
                reaction_active = False

            elif p2_btn.value() == 0 and p2_active:
                p2_score += 1
                update_scoreboard()
                reaction_active = False

        else:
            # Time expired  lose life (FIX IT ALL)
            if p1_active:
                p1_lives += 1
            if p2_active:
                p2_lives += 1

            update_lives()

            if p1_lives >= 3:
                p1_active = False

            if p2_lives >= 3:
                p2_active = False

            reaction_active = False

        # Turn OFF indicators when round ends
        if not reaction_active:
            p1_indicator.off()

            p2_indicator.off()

