#!/usr/bin/env python3
# alex-laycalvert
import time
import random
import RPi.GPIO as GPIO

def main():
    try:
        buttons = [
            [11, False], # Red
            [12, False], # Yellow
            [10, False], # Blue
            [8, False],  # Green
        ]
        leds = [
            18, # Red
            16, # Yellow
            15, # Green
            13  # Blue
        ]
        cycle_rate = 0.1

        GPIO.setwarnings(True)
        GPIO.setmode(GPIO.BOARD)

        for (b, _) in buttons:
            GPIO.setup(b, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        for l in leds:
            GPIO.setup(l, GPIO.OUT)

        sequence = []

        while True:
            # Reset LEDs
            for l in leds:
                GPIO.output(l, GPIO.LOW)

            # Add new color to sequence
            led_index = random.randrange(len(leds))
            sequence.append(leds[led_index])

            # Display Sequence
            for l in sequence:
                GPIO.output(l, GPIO.HIGH)
                time.sleep(1)
                GPIO.output(l, GPIO.LOW)
                time.sleep(0.5)

            # Get user input
            user_sequence = []
            while len(user_sequence) < len(sequence):
                for i, b in enumerate(buttons):
                    if GPIO.input(b[0]) == GPIO.HIGH:
                        buttons[i][1] = True
                        GPIO.output(leds[i], GPIO.HIGH)
                    elif b[1]:
                        user_sequence.append(leds[i])
                        buttons[i][1] = False
                        GPIO.output(leds[i], GPIO.LOW)
                    else:
                        GPIO.output(leds[i], GPIO.LOW)
                time.sleep(cycle_rate)

            # Lost
            if sequence != user_sequence:
                time.sleep(0.3)
                for i in range(0, 3):
                    for l in leds:
                        GPIO.output(l, GPIO.HIGH)
                    time.sleep(0.1)
                    for l in leds:
                        GPIO.output(l, GPIO.LOW)
                    time.sleep(0.1)
                break
            time.sleep(0.5)
    except RuntimeError as err:
        print('ERROR:', str(err))
    except KeyboardInterrupt:
        print('Exiting...')
    finally:
        GPIO.cleanup()

if __name__ == '__main__':
    main()
