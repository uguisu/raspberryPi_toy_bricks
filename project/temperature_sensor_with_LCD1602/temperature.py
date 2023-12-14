# temperature_sensor_with_LCD1602
import os
import LCD1602
import time

ds18b20 = ''


def setup_temperature():
    """
    Setup temperature
    :return:
    """
    global ds18b20
    for i in os.listdir('/sys/bus/w1/devices'):
        if i != 'w1_bus_master1':
            ds18b20 = i


def setup_display():
    """
    Setup LCD1602 display
    """
    # some device may use 0x3F as address
    LCD1602.init(0x27, 1)  # init(slave address, background light)
    LCD1602.write(0, 0, 'Greetings!!')
    LCD1602.write(1, 1, 'From @Kakin')
    time.sleep(2)


def read():
    """
    Read temperature
    :return: temperature
    """
    # global ds18b20
    location = '/sys/bus/w1/devices/' + ds18b20 + '/w1_slave'
    tfile = open(location)
    text = tfile.read()
    tfile.close()
    secondline = text.split("\n")[1]
    temperaturedata = secondline.split(" ")[9]
    temperature = float(temperaturedata[2:])
    temperature = temperature / 1000
    return temperature


def loop():
    # remove welcome info
    LCD1602.clear()

    while True:
        current_temperature = read()
        msg = "T: %0.3f C" % current_temperature

        if current_temperature is not None:
            LCD1602.write(16 - len(msg), 0, msg)
            time.sleep(0.8)


def destroy():
    """
    Stop all
    :return:
    """
    LCD1602.clear()


if __name__ == '__main__':
    try:
        setup_temperature()
        setup_display()
        loop()
    except KeyboardInterrupt:
        destroy()
