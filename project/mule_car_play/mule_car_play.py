# coding=utf-8
# author xin.he
from board import SCL, SDA
import busio
import time
import RPi.GPIO as gpio

# Import the PCA9685 module. Available in the bundle and here:
#   https://github.com/adafruit/Adafruit_CircuitPython_PCA9685
from adafruit_pca9685 import PCA9685, PWMChannel
from adafruit_motor import servo

import signal
from xbox360controller import Xbox360Controller

# SCL - The clock pin
# SDA - The data pin
i2c = busio.I2C(SCL, SDA)


# Create a simple PCA9685 class instance.
pca = PCA9685(i2c)


base_pwm = 4500

# 板子的背面写着12bit,意思是12位分辨率，也就是2的12次方，(4096)  => 2 ^ 12 = 4096

# You can optionally provide a finer tuned reference clock speed to improve the accuracy of the
# timing pulses. This calibration will be specific to each board and its environment. See the
# calibration.py example in the PCA9685 driver.
# pca = PCA9685(i2c, reference_clock_speed=25630710)
# 板子的背面写着 freq: 40 - 1000Hz , 意思是工作频率范围，一般设置为50Hz
pca.frequency = 50


# 检查板子上的舵机插座：
#   0 - 转向
#   7 - 进步电机
#   8 - 摄像头左右
#   9 - 摄像头上下
servo_0 = servo.Servo(pca.channels[0])
# 网上查的舵机参数 -> E6001:  Rotation Angle: +/- 60 degree
actuation_range = 120
servo_0.actuation_range = actuation_range

# 进步电机
motor_7: PWMChannel = pca.channels[7]

# 摄像头上下
servo_9 = servo.Servo(pca.channels[9])
actuation_range = 180
servo_9.actuation_range = actuation_range

# 摄像头左右
servo_8 = servo.Servo(pca.channels[8])
actuation_range = 180
servo_8.actuation_range = actuation_range
# 向右修正45度
servo_8_fix = 45
# 真实角度
servo_8_max = 135
servo_8_min = 45


def on_trigger_r_pressed(axis):
    """
    Electronic accelerator
    """
    if axis.value == 0:
        motor_7.duty_cycle = 0
    else:
        speed = int(axis.value * 1000) + base_pwm
        motor_7.duty_cycle = speed
        # print(f'axis.value = {axis.value}, speed = {speed}')
    pass


def on_trigger_l_pressed(axis):
    pass



def on_button_pressed(button):
    # print('Button {0} was pressed'.format(button.name))
    servo_9.angle = 90
    servo_8.angle = 90 + servo_8_fix


def on_button_released(button):
    # print('Button {0} was released'.format(button.name))
    pass


def on_axis_l_moved(axis):
    # print('L Axis {0} moved to {1} {2}'.format(axis.name, axis.x, axis.y))
    if axis.x < 0:
        # left(angle = 120)
        servo_0.angle = round(axis.x * 10) * 60 / 10 * -1 + 60

    if axis.x > 0:
        # right(angle = 0)
        servo_0.angle = 60 - round(axis.x * 10) * 60 / 10

    if axis.x == 0:
        servo_0.angle = 60


def on_axis_r_moved(axis):
    # 摄像头上下只能转动90度，超过90度的部分被挡住了。完全向上是0度
    # print('R Axis {0} moved to {1} {2}'.format(axis.name, axis.x, axis.y))

    if axis.y < 0:
        # 向上推
        servo_9.angle = round((axis.y  + 1) * 90)

    if axis.y >= 0:
        servo_9.angle = 90


    if axis.x == 0:
        target_angle = 90
    else:
        target_angle = round(90 * (1 - axis.x)) - servo_8_fix
        if target_angle > servo_8_max:
            target_angle = servo_8_max
        if target_angle < servo_8_min:
            target_angle = servo_8_min
    
    servo_8.angle = target_angle + servo_8_fix


def start_control():
    """
    start control
    """
    try:
        with Xbox360Controller(0, axis_threshold=0.2) as controller:
            # Button X events
            controller.button_a.when_pressed = on_button_pressed
            # controller.button_a.when_released = on_button_released

            controller.trigger_r.when_moved = on_trigger_r_pressed
            controller.trigger_l.when_moved = on_trigger_l_pressed

            # Left and right axis move event
            controller.axis_l.when_moved = on_axis_l_moved
            controller.axis_r.when_moved = on_axis_r_moved

            signal.pause()
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':

    # init
    servo_9.angle = 90
    servo_8.angle = 90 + servo_8_fix

    try:
        start_control()
    except KeyboardInterrupt:
        print('game over')
        # release environment
        gpio.cleanup()
        pca.deinit()
