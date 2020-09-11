/*Ardunio code for controlling the AD5764R DAC from Analog Devices
-- Javier Rodriguez

SPI:
  MISO: pin 50
  MOSI: pin 51
  SCK:  pin 52
DAC Control:
  LDAC: pin 9
  CLR:  pin 8
  SYNC: pin 48

*/

#include <SPI.h>
int sync = 48;
int ldac = 9; // Load DAC (update DAC outputs when LOW)
int clr = 8; // DAC Clear
// int error = 0; // Not used in HEX version
// int LED = 13; // Arduino LED for debug
const int FB0 = A0;  // Analog input pin for DAC0 feedback
const int FB1 = A1; // Analog intput pin for DAC1 feedback

void setup()
{
  Serial.begin(115200); // Open USB serial port
  
  // pinMode(7, OUTPUT); // Aux Scope Trigger pin
  pinMode(sync, OUTPUT);
  pinMode(ldac, OUTPUT);
  pinMode(clr, OUTPUT);
  // pinMode(LED, OUTPUT);
  
  // digitalWrite(LED, LOW);
  // digitalWrite(7, HIGH);
  digitalWrite(ldac, LOW); // Kept LOW forever (sync update not implemented)
  digitalWrite(sync, HIGH);
  digitalWrite(clr, HIGH);
  
  SPI.begin(); // Wake up the SPI bus.
  SPI.setBitOrder(MSBFIRST); // Correct order for AD5764.
  SPI.setClockDivider(SPI_CLOCK_DIV32);
  SPI.setDataMode(SPI_MODE1); // 1 and 3 communicate with DAC. 1 is the only one that works with no clock divider.
}

void loop()
{
  if ( Serial.available()) // Wait until all data bytes received are avaialable
  {
    //error = 0;
    byte bytes[4];

    for (int i = 0; i < 4; i++) { // Read 4 bytes from serial port
      bytes[i] = Serial.read();
      delay(1);  // 1mS pause to make sure bytes don’t run into each other.

      // Serial.print(" ");
      // Serial.print(bytes[i], HEX);
      // Serial.print(" ");
    }

    //if (error == 0) { // Error not used in HEX communication
    
      switch (bytes[0]) {
        case 0XFF: SendCommand(bytes);
          break;
        case 0XAA: SendCommandNoFB(bytes);
          break;
        case 0X0F: Sweep(bytes);
          break;
        case 0XBB: ReadFB(bytes);
          break;
        case 0XCC: Reset();
          break;
      }
      
    //}
    //else Serial.print("\nWrong command. Not sent\n");
  }
}

