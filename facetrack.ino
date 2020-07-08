#include <SoftwareSerial.h>
#include <Servo.h>

SoftwareSerial deviceSerial(10, 11); // RX, TX

Servo panServo;
Servo tiltServo;

int pos = 90; //Default positions
int pos2 = 90;

int panMinAngle = 20;
int panMaxAngle = 120;

int tiltMinAngle = 80;
int tiltMaxAngle = 130;

void setup()
{
  panServo.attach(9);	// Pan servo at pin 9
  tiltServo.attach(6);	// Tilt servo at pin 6

  panServo.write(pos);
  tiltServo.write(pos2);

  delay(1000);

  panServo.detach();
  tiltServo.detach();

  Serial.begin(9600);

  deviceSerial.begin(4800);

  Serial.println("Application Started...");
}

void loop()
{
  int str = 0;
  if (deviceSerial.available())
  {
    str = deviceSerial.read();
    Serial.println(str);
    if (str == 48)
    {
      panServo.attach(9);
      Serial.println("Left");
      for (int i = 0; i < 2; i++)
      {
        pos += 2;
        panServo.write(pos);
        delay(30);
      }
      panServo.detach();
    }
    else if (str == 49)
    {
      panServo.attach(9);
      Serial.println("Right");
      for (int i = 0; i < 2; i++)
      {
        pos -= 2;
        panServo.write(pos);
        delay(30);
      }
      panServo.detach();
    }
    else if (str == 50)
    {
      tiltServo.attach(6);
      Serial.println("Up");
      for (int i = 0; i < 2; i++)
      {
        pos2 -= 1;
        tiltServo.write(pos2);
        delay(30);
      }
      tiltServo.detach();
    }
    else if (str == 51)
    {
      tiltServo.attach(6);
      Serial.println("Down");
      for (int i = 0; i < 2; i++)
      {
        pos2 += 1;
        tiltServo.write(pos2);
        delay(30);
      }
      tiltServo.detach();
    }
    else if (str == 57) //Random movements to find a face
    {
      panServo.attach(9);
      tiltServo.attach(6);
      int val = random(panMinAngle, panMaxAngle);
      pos = val;
      panServo.write(val);
      int val2 = random(tiltMinAngle, tiltMaxAngle);
      pos2 = val2;
      tiltServo.write(val2);
      delay(100);
      panServo.detach();
      tiltServo.detach();
      delay(1000);
    }
  }
  delay(5);
}
