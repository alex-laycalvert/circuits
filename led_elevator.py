#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time

def main():
    try:
        buttons = [
            [8, False],
            [10, False]
        ]
        leds = [11, 13, 15, 16, 18, 22]
        cycle_rate = 0.01

        GPIO.setwarnings(True)
        GPIO.setmode(GPIO.BOARD)
        for (b, _) in buttons:
            GPIO.setup(b, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        for l in leds:
            GPIO.setup(l, GPIO.OUT)

        current_led = 0

        while True:
            if GPIO.input(buttons[0][0]) == GPIO.HIGH:
                buttons[0][1] = True
            elif buttons[0][1]:
                current_led -= 1
                if current_led < 0:
                    current_led = len(leds) - 1
                buttons[0][1] = False
            if GPIO.input(buttons[1][0]) == GPIO.HIGH:
                buttons[1][1] = True
            elif buttons[1][1]:
                current_led += 1
                if current_led >= len(leds):
                    current_led = 0
                buttons[1][1] = False
            for i, l in enumerate(leds):
                if i == current_led:
                    GPIO.output(l, GPIO.HIGH)
                else:
                    GPIO.output(l, GPIO.LOW)
            time.sleep(cycle_rate)
    except RuntimeError as err:
        print('ERROR:', str(err))
    except KeyboardInterrupt:
        print('Exiting...')
    finally:
        GPIO.cleanup()


if __name__ == '__main__':
    main()
