import serial, time
s = serial.Serial(port='/dev/cu.usbmodem1421', baudrate=115200)

time.sleep(1)

#======================================
def SendToDAC(Head,CH,value):
    # Head: \xFF: Sent value and listen DAC response
    #       \xAA: Sent value and do NOT listen DAC response
    #       \x0F: Test sweep (both motors, [CH] and [value] ignored, no response)
    #       \xBB: Ask for feedback ([value] ignored)
    #       \xCC: DAC Reset
    # CH: Channel number (\x10, \x11, \x12 or \x13)
    # Value: 16 bit DAC setting. 0 to 65535 (32768 for 0)

    command = Head
    command += CH + (value).to_bytes(2,byteorder='big')
    #                  ↑ Number between 0 and 65535
    #print(command)
    s.write(command)
    s.flush()
#======================================

for j in range(5): # Loops for (almost) full range movement
    for i in range(100,65100,500):
        SendToDAC(b'\xAA',b'\x10',i)
        SendToDAC(b'\xAA',b'\x11',i)
        time.sleep(.01)
        #print(i)
    for i in range(65100,100,-500):
        SendToDAC(b'\xAA',b'\x10',i)
        SendToDAC(b'\xAA',b'\x11',i)
        time.sleep(.01)
        #print(i)
