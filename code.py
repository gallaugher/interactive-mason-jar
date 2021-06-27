import board
import time

# for audio
import digitalio
from audiopwmio import PWMAudioOut as AudioOut
from audiocore import WaveFile

import random
import adafruit_hcsr04
sonar = adafruit_hcsr04.HCSR04(trigger_pin=board.A2, echo_pin=board.A1)
import neopixel
import adafruit_led_animation.color as color

from adafruit_led_animation.animation.solid import Solid
from adafruit_led_animation.animation.colorcycle import ColorCycle
from adafruit_led_animation.animation.blink import Blink
from adafruit_led_animation.animation.comet import Comet
from adafruit_led_animation.animation.chase import Chase
from adafruit_led_animation.animation.pulse import Pulse
from adafruit_led_animation.animation.rainbow import Rainbow
from adafruit_led_animation.animation.rainbowChase import RainbowChase
from adafruit_led_animation.animation.rainbowcomet import RainbowComet
from adafruit_led_animation.animation.rainbowsparkle import RainbowSparkle
from adafruit_led_animation.animation.sparkle import Sparkle
from adafruit_led_animation.animation.SparklePulse import SparklePulse
from adafruit_led_animation.sequence import AnimationSequence
from adafruit_led_animation.group import AnimationGroup

# NOTE: You should be able to refer to these as ex. color.AMBER
# and avoid declaration below.
from adafruit_led_animation.color import (
    AMBER, #(255, 100, 0)
    AQUA, # (50, 255, 255)
    BLACK, #OFF (0, 0, 0)
    BLUE, # (0, 0, 255)
    CYAN, # (0, 255, 255)
    GOLD, # (255, 222, 30)
    GREEN, # (0, 255, 0)
    JADE, # (0, 255, 40)
    MAGENTA, #(255, 0, 20)
    OLD_LACE, # (253, 245, 230)
    ORANGE, # (255, 40, 0)
    PINK, # (242, 90, 255)
    PURPLE, # (180, 0, 255)
    RED, # (255, 0, 0)
    TEAL, # (0, 255, 120)
    WHITE, # (255, 255, 255)
    YELLOW, # (255, 150, 0)
    RAINBOW # a list of colors to cycle through
    # RAINBOW is RED, ORANGE, YELLOW, GREEN, BLUE, and PURPLE ((255, 0, 0), (255, 40, 0), (255, 150, 0), (0, 255, 0), (0, 0, 255), (180, 0, 255))
)

# For Sound
# from adafruit_circuitplayground import cp

# Update to match the pin connected to your NeoPixels
pixel_pin = board.A3
# Update to match the number of NeoPixels you have connected
pixelsOnStrip = 20

stripBrightness = 0.5
pixels = neopixel.NeoPixel(pixel_pin, pixelsOnStrip, brightness=stripBrightness, auto_write=False)

# confirmation all is working
# cp.play_file("chime.wav")
# enable the speaker
speaker = digitalio.DigitalInOut(board.SPEAKER_ENABLE)
speaker.direction = digitalio.Direction.OUTPUT
speaker.value = True

def playfile(filename):
    wave_file = open(filename, "rb")
    with WaveFile(wave_file) as wave:
        with AudioOut(board.SPEAKER) as audio:
            audio.play(wave)
            while audio.playing:
                 pass

def playIntroAndFlash(filename):
    wave_file = open(filename, "rb")
    with WaveFile(wave_file) as wave:
        with AudioOut(board.SPEAKER) as audio:
            audio.play(wave)
            while audio.playing:
                for i in range(0, 11):
                    pixels.brightness = float(i)/10
                    pixels.fill((AMBER))
                    pixels.show()
                    time.sleep(0.05)
                for i in range(10, -1, -1):
                    pixels.brightness = float(i)/10
                    pixels.fill((ORANGE))
                    pixels.show()
                    time.sleep(0.05)

playIntroAndFlash("chime.wav")

solid = Solid(pixels, color=PINK)
turnOff = Solid(pixels, color=BLACK)
blink = Blink(pixels, speed=0.5, color=JADE)
colorcycle = ColorCycle(pixels, speed=0.5, colors=[MAGENTA, ORANGE, TEAL])
chase = Chase(pixels, speed=0.1, color=WHITE, size=3, spacing=6)
# for night-rider, battlestar galactica effect, set length to something lik e3 and speed to a bit longer like 0.2
# Comet has a dimming tale and can also bounce back.
comet = Comet(pixels, speed=0.01, color=PURPLE, tail_length=10, bounce=True)
pulse = Pulse(pixels, speed=0.1, color=AMBER, period=3)

# demonstrate that you can pass in custom colors, too.
# the multi values in parens below are called a tuple value.
# this tuple has three values between 0 and 255.
customMaroonSolid = Solid(pixels, color = (128, 0, 0))

# all pixels the same color, cycling through rainbow
# period = The period over which to cycle the rainbow in seconds
# speed = the animation refresh rate in seconds
rainbow = Rainbow(pixels, speed=0.05, period=2)

# like the theater marquee, but with rainbows.
# will take a while to go through RED through VIOLET
rainbow_chase = RainbowChase(pixels, speed=0.1, size=5, spacing=3)
rainbow_comet = RainbowComet(pixels, speed=0.1, tail_length=7, bounce=True)
# a shifting rainbow that sparkles
# period = The period over which to cycle the rainbow in seconds,
rainbow_sparkle = RainbowSparkle(pixels, speed=0.1, period=3, num_sparkles=15)

sparkle = Sparkle(pixels, speed=0.05, color=BLUE, num_sparkles=2)
sparkle_pulse = SparklePulse(pixels, speed=0.05, period=3, color=JADE)

animations = AnimationSequence(
    solid,
    blink,
    colorcycle,
    chase,
    comet,
    pulse,
    rainbow,
    rainbow_chase,
    rainbow_comet,
    rainbow_sparkle,
    sparkle,
    sparkle_pulse,
    advance_interval=5, # Time in seconds between animations
    auto_clear=True, # Clear pixels between animations
)

# apparently you need to be inside the while loop for this to execute. You'll only see the initial flash if you're outside teh while loop,

timesNoReading = 0

# start out with a blank array
# when we light up lights, find out numOfLights

# if numOfLights has increased
# generate a unique random # 0-20 for each increase in numOfLights and add to light array

# if numofLights has decreased
# remove the decreased values from the end of the arrays

currentNumOfLights = 0
lightsArray = []

def generateUniqueRandom():
    global pixelsOnStrip
    global lightsArray
    randomNum = random.randint(0, pixelsOnStrip-1)
    if len(lightsArray) < pixelsOnStrip:
        while randomNum in lightsArray:
            randomNum = random.randint(0, pixelsOnStrip-1)
    return randomNum

distanceColor = ORANGE

turnOff.animate()
validReadings = []

while True:
    try:
        handDistance = int(sonar.distance)
        if len(validReadings) < 5:
            validReadings.append(handDistance)
        elif len(validReadings) > 0:
            #validReadings.remove(max(validReadings))
            #validReadings.remove(min(validReadings))
            print("len(validReadings) = ", validReadings)
            validReadings.remove(validReadings[0])
            handDistance = sum(validReadings) / len(validReadings)
            print("Distance:", handDistance)
            if handDistance <= 163:
                if handDistance < 30:
                    handDistance = 30
                newNumOfLights = 20 - int((handDistance - 30)/6.65)
                print("newNumOfLights based on new distance of", handDistance, " = ", newNumOfLights)
                if newNumOfLights > len(lightsArray):
                    brightness = (300 - handDistance) / 300
                    stripBrightness = brightness
                    print("Brightness:", brightness)
                    pixels.brightness = stripBrightness
                    lightsToAdd = newNumOfLights - len(lightsArray)
                    for i in range (len(lightsArray), newNumOfLights):
                        newRandomLightNumber = generateUniqueRandom()
                        lightsArray.append(newRandomLightNumber)
                        pixels[newRandomLightNumber] = distanceColor
                        # cp.play_file("blink.wav")
                        playfile("blink.wav")
                        pixels.show()
                        print("Adding light ", i, " of ", newNumOfLights, " which is ", newRandomLightNumber)
                    print("lightsArray now contains", len(lightsArray), "lights")
                    print("The new list is: ", lightsArray)
                    print("currentNumOfLights = ", len(lightsArray))
                elif newNumOfLights < len(lightsArray):
                    numOfLightsToRemove = len(lightsArray) - newNumOfLights
                    print("ABOUT TO REMOVE", numOfLightsToRemove, "LIGHTS! Current len(lightsArray = ", len(lightsArray))
                    print("ARRAY lightsArray = ", lightsArray)
                    brightness = (300 - handDistance) / 300
                    stripBrightness = brightness
                    print("Brightness:", brightness)
                    pixels.brightness = stripBrightness
                    for i in range(len(lightsArray)-1, newNumOfLights-1, -1):
                        lightNumberToRemove = lightsArray.pop()
                        pixels[lightNumberToRemove] = BLACK
                        pixels.show()
                        # cp.play_file("off.wav")
                        playfile("off.wav")
                    print("SHOULD HAVE DELETED", numOfLightsToRemove, "LIGHTS! Current len(lightsArray = ", len(lightsArray))
                    print("SHRUNK ARRAY: ", lightsArray)
                    print("SHRUNK ADJUSTED: currentNumOfLights = ", currentNumOfLights, "len(lightsArray) = ", len(lightsArray))
                    currentNumOfLights = newNumOfLights
                print("currentNumOfLights = ", currentNumOfLights)
                #turnOff.animate() # clear out any lights that are on, first
                #for i in lightsArray:
                #    pixels[i] = distanceColor
                #pixels.show()
                timesNoReading = 0
                #brightness = (300 - handDistance) / 300
                #stripBrightness = brightness
                #print("Brightness:", brightness)
                #pixels.brightness = stripBrightness
            # print("Retrying! timesNoReading = ", timesNoReading)
            else:
                timesNoReading += 1
                if timesNoReading > 10:
                    # cpBlack.animate()
                    turnOff.animate()
                    lightsArray = []
                    currentNumOfLights = 0
    except RuntimeError:
        print("Retrying! timesNoReading = ", timesNoReading)
        timesNoReading += 1
        if timesNoReading > 10:
            # turn off all lights
            for i in range(len(lightsArray)-1, -1, -1):
                    lightNumberToRemove = lightsArray.pop()
                    pixels[lightNumberToRemove] = BLACK
                    pixels.show()
                    # cp.play_file("off.wav")
                    playfile("off.wav")
            # turnOff.animate()
            validReadings = []
            stripBrightness = 0.0
            pixels.brightness = stripBrightness
    time.sleep(0.1)
