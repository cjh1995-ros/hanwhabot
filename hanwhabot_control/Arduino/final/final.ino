#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>
#include <ros.h>

#include <std_msgs/UInt8.h>

#define PulseRev 800
#define SERVOMIN  150 // 서보모터 최소 출력 값 = 0도
#define SERVOMAX  600 // 서보모터 최대 출력 값 = 180도 
Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();
int ENA=5; //define Enable Pin
int DIR=6; //define Direction pin
int PUL=7; //define Pulse pin

uint8_t re;

void messageCb( const std_msgs::UInt8& msg){
  re = msg.data;
}

//ros param declare
ros::NodeHandle nh;
std_msgs::UInt8 success_string;
ros::Subscriber<std_msgs::UInt8> order("order", messageCb);
ros::Publisher success("goal_Success",&success_string);
//ros param declare end

void setup() 
{
  Serial.begin(9600);

  nh.initNode();
  nh.getHardware()->setBaud(57600);
  nh.subscribe(order);
  nh.advertise(success);
  
  pinMode(2, OUTPUT);
  pinMode(3, OUTPUT);
  pinMode(4, OUTPUT);
  pinMode(5, OUTPUT);
  pinMode (PUL, OUTPUT);
  pinMode (DIR, OUTPUT);
  pinMode (ENA, OUTPUT);
  pwm.begin(); //pwm 제어 시작
  pwm.setPWMFreq(60);  // Analog servos run at ~60 Hz update
  delay(10);
}
void cw(int cycle) 
{
  int steps = PulseRev * cycle;
  for (int i=0; i<steps; i++)    //Forward 5000 steps
  {
    digitalWrite(DIR,LOW);
    digitalWrite(ENA,HIGH);
    digitalWrite(PUL,HIGH);
    delayMicroseconds(100);
    digitalWrite(PUL,LOW);
    delayMicroseconds(100);
  }
}
void ccw(int cycle)
{ 
  int steps = PulseRev * cycle;
  for (int i=0; i<steps; i++)   //Backward 5000 steps
  {
    digitalWrite(DIR,HIGH);
    digitalWrite(ENA,HIGH);
    digitalWrite(PUL,HIGH);
    delayMicroseconds(100);
    digitalWrite(PUL,LOW);
    delayMicroseconds(100);
  }
}
void mgcw()
{
    pwm.setPWM(0, 0, 600); // 0번 핀에 서보모터 연결, 600이므로 최대로 열림//
    Serial.println(600);
    delay(10);
}
void mgccw()
{
    pwm.setPWM(0, 0, 150); // 0번 핀에 서보모터 연결, 0이므로 완전히 닫힘//
    Serial.println(150);
    delay(10);
}
void loop() 
{
  nh.spinOnce();
  if(Serial.available()) 
  // Serial.available 함수는 받아둔 데이터가 있으면 true를 반환
  {
//    char re = Serial.read(); // 받아둔 데이터 중에서 1byte를 가져온다
    if(re==1) // 액추에이터 '1'이 입력되면 늘어남
    {
      digitalWrite(4, HIGH);
      digitalWrite(5, LOW);
      success_string.data = 1;
      success.publish(&success_string);
    }
    else if(re==2) // 액추에이터 '2'가 입력되면 줄어듬
    {
      digitalWrite(4, LOW);
      digitalWrite(5, HIGH);
      success_string.data = 2;
      success.publish(&success_string);
    }
    else if(re==3) // 액추에이터 바로 멈춤
    {
      digitalWrite(4, LOW);
      digitalWrite(5, LOW);
      success_string.data = 3;
      success.publish(&success_string);
      
    }
    else if(re==4) // mg995 시계방향 무한회전
    {
      digitalWrite(2, HIGH);
      digitalWrite(3, LOW);
      success_string.data = 4;
      success.publish(&success_string);

    }
    else if(re==5) // mg995 반시계방향 무한회전
    {
      digitalWrite(2, LOW);
      digitalWrite(3, HIGH);
      success_string.data = 5;
      success.publish(&success_string);

    }
    else if(re==6) // mg995 바로 멈춤
    {
      digitalWrite(2, LOW);
      digitalWrite(3, LOW);
      success_string.data = 6;
      success.publish(&success_string);

    }
    else if(re==7) //스텝모터 1바퀴 시계 방향//
    {
      cw(1);   
      success_string.data = 7;
      success.publish(&success_string);

    }
    else if(re==8) //스텝모터 1바퀴 시계 반대 방향//
    {
      ccw(1);
      success_string.data = 8;
      success.publish(&success_string);

    }
    else if(re==9) //서보모터(mg995 개조전) 바구니 문열기
    {
      mgcw();
      success_string.data = 9;
      success.publish(&success_string);

    }
    else if(re==10) //서보모터(mg995 개조전) 바구니 문닫기
    {
      mgccw();
      success_string.data = 10;
      success.publish(&success_string);
    }
  }
}
