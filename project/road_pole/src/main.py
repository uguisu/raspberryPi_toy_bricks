import RPi.GPIO as GPIO
import time


TRIG = 11
ECHO = 12

MAX_DISTANCE = 20


def prepare():
    """
    prepare & init
    """

    # ultrasonic ranging
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(TRIG, GPIO.OUT)
    GPIO.setup(ECHO, GPIO.IN)


def distance():
    GPIO.output(TRIG, 0)
    time.sleep(0.000002)

    GPIO.output(TRIG, 1)
    time.sleep(0.00001)
    GPIO.output(TRIG, 0)

    while GPIO.input(ECHO) == 0:
        a = 0
    time1 = time.time()
    while GPIO.input(ECHO) == 1:
        a = 1
    time2 = time.time()

    during = time2 - time1
    return during * 340 / 2 * 100


def loop():
    while True:
        dis = distance()
        print(dis, 'cm\n')
        if dis <= MAX_DISTANCE:
            print('open....')
        else:
            print('close...')
        time.sleep(0.3)


def final_release():
    """
    release resources
    """
    def release_laser_sensor():
        # Release resource
        GPIO.cleanup()

    print('final release')
    release_laser_sensor()


if __name__ == '__main__':
    # prepare
    prepare()

    try:
        loop()
    except KeyboardInterrupt:
        # release resource
        final_release()
