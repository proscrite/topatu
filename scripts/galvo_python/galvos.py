import serial, time

def open_serial_port(port_name='COM4',  baudrate=115200):
    s = serial.Serial(port_name, baudrate=baudrate)
    return s

#======================================
def SendToDAC(serialport, Head,CH,value):
    # Head: \xFF: Sent value and listen DAC response
    #       \xAA: Sent value and do NOT listen DAC response
    #       \x0F: Test sweep (both motors, [CH] and [value] ignored, no response)
    #       \xBB: Ask for feedback ([value] ignored)
    #       \xCC: DAC Reset
    # CH: Channel number (\x10, \x11, \x12 or \x13)
    # Value: 16 bit DAC setting. 0 to 65535 (32768 for 0)
    #s = open_serial_port()
    command = Head
    command += CH + (value).to_bytes(2,byteorder='big')
    #                  ↑ Number between 0 and 65535
    #print(command)
    serialport.write(command)
    serialport.flush()
#======================================

def move_to_positionXY(serialport, position, galbo1=True, galbo2=True, center = [int(65534/2),int(65534/2)], feedback=False, wait=1):
    time.sleep(wait)
    if feedback:
        if galbo1:
            SendToDAC(serialport,b'\xFF',b'\x10',center[0]+position[0])
        if galbo2:
            SendToDAC(serialport,b'\xFF',b'\x11',center[1]+position[1])
    else:
        if galbo1:
            SendToDAC(serialport,b'\xAA',b'\x10',center[0]+position[0])
        if galbo2:
            SendToDAC(serialport,b'\xAA',b'\x11',center[1]+position[1])
