import RPi.GPIO as GPIO
import time


TRIG = 11
ECHO = 12
PIN_LED_R = 15
PIN_LED_G = 16

MAX_DISTANCE = 20

p_R = None
p_G = None

LED_RED = 0xFF00
LED_GREEN = 0x00FF


def prepare():
    """
    prepare & init
    """

    global p_R, p_G

    # Numbers GPIOs by physical location
    GPIO.setmode(GPIO.BOARD)

    # ultrasonic ranging
    GPIO.setup(TRIG, GPIO.OUT)
    GPIO.setup(ECHO, GPIO.IN)

    # LED
    GPIO.setup(PIN_LED_R, GPIO.OUT)  # Set pins' mode is output
    GPIO.output(PIN_LED_R, GPIO.HIGH)  # Set pins to high(+3.3V) to off led
    GPIO.setup(PIN_LED_G, GPIO.OUT)  # Set pins' mode is output
    GPIO.output(PIN_LED_G, GPIO.HIGH)  # Set pins to high(+3.3V) to off led
    # set Frequece to 2KHz
    p_R = GPIO.PWM(PIN_LED_R, 2000)
    p_G = GPIO.PWM(PIN_LED_G, 2000)
    # Initial duty Cycle = 0(leds off)
    p_R.start(0)
    p_G.start(0)


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


def set_color(col):
    """
    set color
    # For example : col = 0x112233
    """
    def map(x, in_min, in_max, out_min, out_max):
        return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

    global p_R, p_G

    R_val = (col & 0x1100) >> 8
    G_val = (col & 0x0011) >> 0

    R_val = map(R_val, 0, 255, 0, 100)
    G_val = map(G_val, 0, 255, 0, 100)

    p_R.ChangeDutyCycle(R_val)  # Change duty cycle
    p_G.ChangeDutyCycle(G_val)


def loop():
    while True:
        dis = distance()
        # print(dis, 'cm\n')
        if dis <= MAX_DISTANCE:
            # print('open....')
            set_color(LED_GREEN)
        else:
            # print('close...')
            set_color(LED_RED)
        time.sleep(0.3)


def final_release():
    """
    release resources
    """
    def release_sensor():
        # Release resource
        GPIO.cleanup()

    global p_R, p_G

    print('final release')

    # led
    p_R.stop()
    p_G.stop()
    # Turn off all leds
    GPIO.output(PIN_LED_R, GPIO.HIGH)
    GPIO.output(PIN_LED_G, GPIO.HIGH)

    release_sensor()


if __name__ == '__main__':
    # prepare
    prepare()

    try:
        loop()
    except KeyboardInterrupt:
        # release resource
        final_release()
