import serial, time
s = serial.Serial(port='/dev/cu.usbmodem1421', baudrate=115200)

time.sleep(1)
s.write(b"FF118F00")

time.sleep(.1)
while s.in_waiting:
    time.sleep(.1)
    print(s.readline())
