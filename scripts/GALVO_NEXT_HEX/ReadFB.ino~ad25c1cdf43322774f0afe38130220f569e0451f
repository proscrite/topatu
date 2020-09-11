void ReadFB(byte DB[4])
{
  switch (DB[1]) {
    case 0X10:
      Serial.print("DAC0 feedback = ");
      Serial.println(analogRead(FB0));
      break;
    case 0X11:
      Serial.print("DAC1 feedback = ");
      Serial.println(analogRead(FB1));
      break;
    default:
      Serial.print("Wrong channel selected\n");
      break;
  }
}
