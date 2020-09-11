void Sweep(byte SW[4])
{
  if (SW[0] == 15) {
    SW[3] = 0;
    SW[2] = 0;
    for (unsigned long i = 0; i < 65535; i = i + 5) {
      SW[3] = SW[3] + 5;
      if (SW[3] >= 255) {
        SW[3] = 0;
        SW[2] = SW[2] + 5;
      }
      SendCommandNoFB(SW);
      delay(1);
    }
  }
}
