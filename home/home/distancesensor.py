from gpiozero import DistanceSensor, PWMLED
from signal import pause

def measure_distance():
    sensor = DistanceSensor(4, 17, max_distance=2)
    led = PWMLED(22)
    while True:
        led.value = sensor.distance/2
        sleep(1)

if __name__ == "__main__":
    measure_distance()
