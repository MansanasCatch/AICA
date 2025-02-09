#include <Servo.h>
#include <SoftwareSerial.h>

SoftwareSerial hc06(10, 11);

String inputString;
Servo left_right;
Servo up_down;

void setup() {
  hc06.begin(9600);
  Serial.begin(19200);

  left_right.attach(4);
  up_down.attach(5);

  left_right.write(90);
  up_down.write(90);
}

void loop() {
  if (hc06.available() > 0) {
    inputString = hc06.readStringUntil('\r');
    //int x_axis = inputString.substring(0, inputString.indexOf(',')).toInt();
    //int y_axis = inputString.substring(inputString.indexOf(',') + 1).toInt();

    // int y = map(y_axis, 0, 1080, 180, 0);
    // int x = map(x_axis, 0, 1920, 180, 0);

    char c;
    char no = ',';
    String NewBT_value;
    NewBT_value = inputString;
    for (int i = 0; i < NewBT_value.length() - 1; ++i) {
      c = NewBT_value.charAt(i);
      if (c == no) {
        NewBT_value.remove(i, 1);
      }
    }

    int i1 = NewBT_value.indexOf(',');
    int i2 = NewBT_value.indexOf(',', i1 + 1);

    int x_axis = NewBT_value.substring(0, i1).toInt();
    int y_axis = NewBT_value.substring(i1 + 1, i2).toInt();

    left_right.write(x_axis);
    up_down.write(y_axis);
  }
}