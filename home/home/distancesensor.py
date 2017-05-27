from gpiozero import DistanceSensor, PWMLED
from time import sleep

def measure_distance():
    sensor = DistanceSensor( 17, 4, max_distance=1)
    led = PWMLED(22)
    while True:
        led.value = 1.0 - sensor.distance
        sleep(1)

if __name__ == "__main__":
    measure_distance()
