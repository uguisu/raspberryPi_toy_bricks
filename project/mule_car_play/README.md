# Mule Car Play

Remote Control Car Toys Based on Donkey Car Hardware Platform Transformation

## Allow bluetooth

1) Allow bluetooth via `raspi-config`

2) Config bluetooth via `bluetoothctl` for the first time
```sh
bluetoothctl

# enable bluetooth
agent on
power on

# enable scan, find your device's address
scan on


# pair <address>
pair    98:B6:E7:C9:A1:47
connect 98:B6:E7:C9:A1:47
trust   98:B6:E7:C9:A1:47
```

Prepare a shell to connect bluetooth for later use
```sh
bluetoothctl connect 98:B6:E7:C9:A1:47
bluetoothctl trust 98:B6:E7:C9:A1:47
```

## xbox controller

```sh
apt-get install joystick

# test
jstest /dev/input/js0
```

## I2C

```sh
apt-get install python3-smbus python3-dev i2c-tools
```

Try to find i2c device
```sh
i2cdetect -y 1
```

## Use mjpg

```sh
git clone https://github.com/jacksonliam/mjpg-streamer.git
sudo apt-get install cmake libjpeg62-turbo-dev
sudo apt-get install gcc g++

cd mjpg-streamer-experimental
make
sudo make install
```

Start service
```sh
./mjpg_streamer -i "input_uvc.so -d /dev/video0 -r 640x480 -f 30" -o "output_http.so -w www"
# open browser  http://<PI's IP>:8080/stream.html
```