import RPi.GPIO as GPIO
import time


# pin declare
PIN_ULTRASONIC_RANGING_TRIG = 11
PIN_ULTRASONIC_RANGING_ECHO = 12
PIN_LED_R = 15
PIN_LED_G = 16
PIN_BUZZER = 18
PIN_SG90 = 8

last_status = None

# max distance
MAX_DISTANCE = 20
# LED Frequece
LED_FREQUENCE = 2000

p_R = None
p_G = None

LED_RED = 0xFF00
LED_GREEN = 0x00FF

# parking gate sound
Buzz = None
PARKING_GATE = [294, 350]
PARKING_GATE_BEAT = [0.5, 0.5]

# SG90
SG90_PWM = None
SG90_FREQUENCE = 50


def prepare():
    """
    prepare & init
    """

    global p_R, p_G, Buzz, SG90_PWM

    # Numbers GPIOs by physical location
    GPIO.setmode(GPIO.BOARD)

    # ultrasonic ranging
    GPIO.setup(PIN_ULTRASONIC_RANGING_TRIG, GPIO.OUT)
    GPIO.setup(PIN_ULTRASONIC_RANGING_ECHO, GPIO.IN)

    # LED
    GPIO.setup(PIN_LED_R, GPIO.OUT)  # Set pins' mode is output
    GPIO.output(PIN_LED_R, GPIO.HIGH)  # Set pins to high(+3.3V) to off led
    GPIO.setup(PIN_LED_G, GPIO.OUT)  # Set pins' mode is output
    GPIO.output(PIN_LED_G, GPIO.HIGH)  # Set pins to high(+3.3V) to off led

    # set Frequece to 2KHz
    p_R = GPIO.PWM(PIN_LED_R, LED_FREQUENCE)
    p_G = GPIO.PWM(PIN_LED_G, LED_FREQUENCE)
    # Initial duty Cycle = 0(leds off)
    p_R.start(0)
    p_G.start(0)

    # parking gate
    GPIO.setup(PIN_BUZZER, GPIO.OUT)
    # 440 is initial frequency.
    Buzz = GPIO.PWM(PIN_BUZZER, 440)

    # SG90
    GPIO.setup(PIN_SG90, GPIO.OUT)
    SG90_PWM = GPIO.PWM(PIN_SG90, SG90_FREQUENCE)
    SG90_PWM.start(0)


def distance():
    """
    ultrasonic ranging scan distance
    """
    GPIO.output(PIN_ULTRASONIC_RANGING_TRIG, GPIO.LOW)
    time.sleep(0.000002)

    GPIO.output(PIN_ULTRASONIC_RANGING_TRIG, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(PIN_ULTRASONIC_RANGING_TRIG, GPIO.LOW)

    while GPIO.input(PIN_ULTRASONIC_RANGING_ECHO) == GPIO.LOW:
        # wait until input changes
        pass
    time1 = time.time()

    while GPIO.input(PIN_ULTRASONIC_RANGING_ECHO) == GPIO.HIGH:
        # wait until input changes
        pass
    time2 = time.time()

    return (time2 - time1) * 340 / 2 * 100


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


def parking_gate_sound(is_up=True):

    # Start Buzzer pin with 50% duty ration
    Buzz.start(50)

    local_range = None
    if is_up:
        local_range = range(0, len(PARKING_GATE))
    else:
        local_range = range(len(PARKING_GATE) - 1, -1, -1)

    for i in local_range:
        # Change the frequency along the song note
        Buzz.ChangeFrequency(PARKING_GATE[i])
        # delay a note for beat * 0.5s
        time.sleep(PARKING_GATE_BEAT[i] * 0.5)
    # Stop the buzzer
    Buzz.stop()


def sg_90_turn(angle):
    """
    angle from 0 to 180
    """

    global SG90_PWM

    SG90_PWM.ChangeDutyCycle(2.5 + angle / 360 * 20)
    # wait 20ms until SG90 9G Servo stopped
    time.sleep(0.02)
    # clean signal
    # IMPORTANT: this will prevent SG90 9G Servo jitter
    SG90_PWM.ChangeDutyCycle(0)


def loop():

    global last_status

    while True:
        dis = distance()
        # print(dis, 'cm\n')
        if dis <= MAX_DISTANCE:
            # print('open....')
            set_color(LED_GREEN)

            if last_status is None or 0 == last_status:
                pass
            else:
                parking_gate_sound()
                sg_90_turn(90)

            last_status = 0
        else:
            # print('close...')
            set_color(LED_RED)

            if last_status is None or 1 == last_status:
                pass
            else:
                parking_gate_sound(is_up=False)
                sg_90_turn(0)

            last_status = 1

        time.sleep(0.3)


def final_release():
    """
    release resources
    """
    def release_sensor():
        # Release resource
        GPIO.cleanup()

    global p_R, p_G, Buzz, SG90_PWM

    print('final release')

    # led
    p_R.stop()
    p_G.stop()
    # Turn off all leds
    GPIO.output(PIN_LED_R, GPIO.HIGH)
    GPIO.output(PIN_LED_G, GPIO.HIGH)

    # parking gate
    # Stop the buzzer
    Buzz.stop()
    # Set Buzzer pin to High
    GPIO.output(PIN_BUZZER, GPIO.HIGH)

    # sg 90
    SG90_PWM.ChangeDutyCycle(0)
    SG90_PWM.stop()

    release_sensor()


if __name__ == '__main__':
    # prepare
    prepare()

    try:
        loop()
    except KeyboardInterrupt:
        # release resource
        final_release()
