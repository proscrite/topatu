import serial, time
s = serial.Serial(port='COM4', baudrate=115200)

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
#======================================

SendToDAC(b'\xAA',b'\x11',0) # Set value without response
time.sleep(.1)
SendToDAC(b'\xBB',b'\x11',0) # Ask for feedback

time.sleep(.1)
while s.in_waiting: # Print while serial input buffer has something
    time.sleep(.1)
    print(s.readline())
