void Sweep(byte SW[4])
{
  if (SW[0] == 15) {
    SW[3] = 0;
    SW[2] = 0;
    for (char j = 0; j < 5; j++) {

      for (long i = 100; i < 65400; i = i + 100) {

        SW[2] = i / 256;
        SW[3] = i % 256;

        SW[1] = 0X10;
        SendCommandNoFB(SW);
        SW[1] = 0X11;
        SendCommandNoFB(SW);
        delay(1);
      }

      for (long i = 65400; i > 101; i = i - 100) {

        SW[2] = i / 256;
        SW[3] = i % 256;

        SW[1] = 0X10;
        SendCommandNoFB(SW);
        SW[1] = 0X11;
        SendCommandNoFB(SW);
        delay(1);
      }
    }
  }
}
