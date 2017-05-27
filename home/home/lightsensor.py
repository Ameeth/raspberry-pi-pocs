from gpiozero import LightSensor, PWMLED
from time import sleep

def measure_light():
    sensor = LightSensor( 18 )
    led = PWMLED(22)
    while True:
        led.value = 1.0 - sensor.values
        sleep(1)

if __name__ == "__main__":
    measure_light()
