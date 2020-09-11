/*Ardunio code for controlling the AD5764R DAC from Analog Devices

  MISO: pin 50
  MOSI: pin 51
  SCK:  pin 52

  LDAC: pin 9
  CLR:  pin 8
  SYNC: pin 48

*/

#include <SPI.h>
int sync = 48; // Using digital pin 52 for SPI slave select
int ldac = 9; // Load DAC (update DAC outputs when LOW)
int clr = 8; // DAC Clear
int error = 0;

void setup()
{
  Serial.begin(115200);
  pinMode(7, OUTPUT); // Aux Scope Trigger pin
  pinMode(sync, OUTPUT);
  pinMode(ldac, OUTPUT);
  pinMode(clr, OUTPUT);
  digitalWrite(7, HIGH);
  digitalWrite(ldac, LOW);
  digitalWrite(sync, HIGH);
  digitalWrite(clr, HIGH);
  SPI.begin(); // Wake up the SPI bus.
  SPI.setBitOrder(MSBFIRST); // Correct order for AD5764.
  SPI.setClockDivider(SPI_CLOCK_DIV32);
  SPI.setDataMode(SPI_MODE1); //1 and 3 communicate with DAC. 1 is the only one that works with no clock divider.
}

void loop()
{
  if ( Serial.available()) // Wait until all data bytes are avaialable
  {
    error = 0;
    byte bytes[4];

    for (int i = 0; i < 4; i++) { // Read 8 characters grouped by 2. Convert each pair od ASCII to HEX
      byte temp = Serial.read() - 48;
      if (temp > 9) temp = temp - 7;
      if (temp > 15) error = 1;

      // Serial.print(temp << 4, HEX);
      // Serial.print(" ");
      delay(1);
      byte temp2 = Serial.read() - 48;
      if (temp2 > 9) temp2 = temp2 - 7;
      if (temp2 > 15) error = 1;

      //Serial.print(temp2, HEX);

      bytes[i] = (temp << 4) + temp2;
      
//            Serial.print(" ");
//            Serial.print(bytes[i], HEX);
//            Serial.print(" ");

      delay(1); // 1mS pause to make sure bytes don’t run into each other.
    }

    if (error == 0) {
      switch (bytes[0]) {
        case 0XFF: SendCommand(bytes);
          break;
        case 0XAA: SendCommandNoFB(bytes);
          break;
        case 0X0F: Sweep(bytes);
          break;
      }
    }
    else Serial.print("\nWrong command. Not sent\n");
  }

}
