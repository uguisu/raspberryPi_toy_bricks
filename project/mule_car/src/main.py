import RPi.GPIO as GPIO
from flask import Flask, jsonify
from waitress import serve

from car_config import *

app = Flask(__name__)


def prepare():
    """
    prepare & init
    """
    def init_laser_sensor():
        """
        init laser sensor
        """
        # Numbers GPIOs by physical location
        GPIO.setmode(GPIO.BOARD)
        # Set LedPin's mode is output
        GPIO.setup(laser_gpio_pin_number, GPIO.OUT)
        # Set LedPin high(+3.3V) to off led
        GPIO.output(laser_gpio_pin_number, GPIO.HIGH)

    init_laser_sensor()


def final_release():
    """
    release resources
    """
    def release_laser_sensor():
        # led off
        GPIO.output(laser_gpio_pin_number, GPIO.HIGH)
        # Release resource
        GPIO.cleanup()

    print('final release')
    release_laser_sensor()


@app.route('/laserOn', methods=['GET'])
def laser_on():
    # led on
    GPIO.output(laser_gpio_pin_number, GPIO.LOW)
    return jsonify({"status": "true"})


@app.route('/laserOff', methods=['GET'])
def laser_off():
    # led off
    GPIO.output(laser_gpio_pin_number, GPIO.HIGH)
    return jsonify({"status": "true"})


if __name__ == '__main__':
    # prepare
    prepare()

    # start http server
    serve(app, host=app_binding_address, port=app_port)

    # release resource
    final_release()
