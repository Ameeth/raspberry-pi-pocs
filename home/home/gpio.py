import sys, time
import RPi.GPIO as GPIO

colorMap = {'red':11,'green':13, 'blue':15}
def blink(pin):
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.HIGH)
    time.sleep(5)
    GPIO.cleanup()

def turnOff(pin):
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)
    time.sleep(5)
    GPIO.cleanup()

def glow_led(color):
    print("Glow led " + color)
    blink(colorMap[color])

def glow_switchoff():
    print("Switch off the LED")
    for key, value in d.items():
        turnOff(value)

if __name__ == "__main__":
    import sys
    glow_led(str(sys.argv[1]))
