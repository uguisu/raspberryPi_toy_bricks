from board import SCL, SDA
import busio
import time
# Import the PCA9685 module. Available in the bundle and here:
#   https://github.com/adafruit/Adafruit_CircuitPython_PCA9685
from adafruit_pca9685 import PCA9685, PWMChannel
from adafruit_motor import servo


# SCL - The clock pin
# SDA - The data pin
i2c = busio.I2C(SCL, SDA)


# Create a simple PCA9685 class instance.
pca = PCA9685(i2c)


# 板子的背面写着12bit,意思是12位分辨率，也就是2的12次方，(4096)  => 2 ^ 12 = 4096


# You can optionally provide a finer tuned reference clock speed to improve the accuracy of the
# timing pulses. This calibration will be specific to each board and its environment. See the
# calibration.py example in the PCA9685 driver.
# pca = PCA9685(i2c, reference_clock_speed=25630710)
# 板子的背面写着 freq: 40 - 1000Hz , 意思是工作频率范围，一般设置为50Hz
pca.frequency = 50


# To get the full range of the servo you will likely need to adjust the min_pulse and max_pulse to
# match the stall points of the servo.
# This is an example for the Sub-micro servo: https://www.adafruit.com/product/2201
# servo7 = servo.Servo(pca.channels[7], min_pulse=580, max_pulse=2350)
# This is an example for the Micro Servo - High Powered, High Torque Metal Gear:
#   https://www.adafruit.com/product/2307
# servo7 = servo.Servo(pca.channels[7], min_pulse=500, max_pulse=2600)
# This is an example for the Standard servo - TowerPro SG-5010 - 5010:
#   https://www.adafruit.com/product/155
# servo7 = servo.Servo(pca.channels[7], min_pulse=400, max_pulse=2400)
# This is an example for the Analog Feedback Servo: https://www.adafruit.com/product/1404
# servo7 = servo.Servo(pca.channels[7], min_pulse=600, max_pulse=2500)
# This is an example for the Micro servo - TowerPro SG-92R: https://www.adafruit.com/product/169
# servo7 = servo.Servo(pca.channels[7], min_pulse=500, max_pulse=2400)

# The pulse range is 750 - 2250 by default. This range typically gives 135 degrees of
# range, but the default is to use 180 degrees. You can specify the expected range if you wish:
# servo7 = servo.Servo(pca.channels[7], actuation_range=135)
# servo7 = servo.Servo(pca.channels[7])


# 检查板子上的舵机插座：
#   0 - 转向
#   7 - 进步电机
# servo_0 = servo.Servo(pca.channels[0], min_pulse=150, max_pulse=600)
servo_0 = servo.Servo(pca.channels[0])
# 网上查的舵机参数 -> E6001:  Rotation Angle: +/- 60 degree
actuation_range = 120
servo_0.actuation_range = actuation_range







servo_8 = servo.Servo(pca.channels[8])
actuation_range = 180
servo_8.actuation_range = actuation_range

sleep_time = 0.01
for i in range(actuation_range):
    servo_8.angle = i
    time.sleep(sleep_time)

for i in range(actuation_range, 0, -1):
    servo_8.angle = i
    time.sleep(sleep_time)

servo_8.angle = 135
time.sleep(sleep_time)






# servo_9 = servo.Servo(pca.channels[9])
# actuation_range = 180
# servo_9.actuation_range = actuation_range

# sleep_time = 0.01
# for i in range(0, 90):
#     servo_9.angle = i
#     time.sleep(sleep_time)


# servo_9.angle = 90









pca.deinit()
import sys
sys.exit()




# We sleep in the loops to give the servo time to move into position.
actuation_range = 120
sleep_time = 0.01
for i in range(actuation_range):
    servo_0.angle = i
    time.sleep(sleep_time)
for i in range(actuation_range):
    servo_0.angle = actuation_range - i
    time.sleep(sleep_time)

# 车轮回正，中间位置是 60度 的位置
servo_0.angle = 60



# 这个方法行不通
# motor_7 = motor.DCMotor(pca.channels[7], positive_pwm = 1, negative_pwm = -1)

# # 前进速度 0.5
# motor_7.throttle(0.5)
# time.sleep(3)
# # 停车
# motor_7.throttle(0)


# hobbywing 1625, PWM Frequency: 1KHz
# pca.frequency = 1000
# motor_7 = servo.Servo(pca.channels[7], min_pulse=1000, max_pulse=2000)
motor_7: PWMChannel = pca.channels[7]


motor_7.duty_cycle = 0
time.sleep(3)


motor_7.duty_cycle = 4560


# 查找可以驱动的频率
sleep_time = 1
# for i in range(35000, 45000, 100):
for i in range(0, 6200, 50):
    print(f'i = {i}')
    motor_7.duty_cycle = i
    time.sleep(sleep_time)
# 4600 -> 发出声音，起步?
# TODO 上限在什么位置？是否存在倒车档位？




# print('start motor')
# motor_7.duty_cycle = 4750
# print('motor started...')

# time.sleep(5)

print('stop motor')
motor_7.duty_cycle = 0
print('motor stopped')


pca.deinit()
