void SendCommandNoFB(byte DB[4])
{
  digitalWrite(sync, LOW); // Assert sync
  // digitalWrite(ldac, LOW);
  int o1 = SPI.transfer(DB[1]); // Send command byte to DAC
  Serial.flush();
  int o2 = SPI.transfer(DB[2]); // MS data bits to DAC
  Serial.flush();
  int o3 = SPI.transfer(DB[3]); // LS 8 data bits to DAC
  Serial.flush();
  digitalWrite(sync, HIGH); // Raise sync to change the dac voltage. Must have LDAC tied low.
}
