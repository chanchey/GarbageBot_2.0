int forward = 4;
int reverse = 5;
int right = 6;
int left = 7;

int led = 13;
  int forwardstate;
  int reversestate;
  int leftstate;
  int rightstate;
void setup() {
  // put your setup code here, to run once:
  pinMode(forward,INPUT);
  pinMode(reverse,INPUT);
  pinMode(right,INPUT);
  pinMode(left,INPUT);
  pinMode(led,OUTPUT);

  int forwardstate;
  byte reversestate;
  byte leftstate;
  byte rightstate;
  
}

void loop() {
  // put your main code here, to run repeatedly:
  forwardstate = digitalRead(forward);
  reversestate = digitalRead(reverse);
  rightstate = digitalRead(right);
  leftstate = digitalRead(left);


if (forwardstate == HIGH){
  digitalWrite(led,HIGH);
  delay(100);
  digitalWrite(led,LOW);
  delay(100);
} else {
  digitalWrite(led,LOW);
}
if (reversestate == HIGH){
  digitalWrite(led,HIGH);
  delay(500);
  digitalWrite(led,LOW);
  delay(500);  
} else {
  digitalWrite(led,LOW);
}
if (rightstate == HIGH){
  digitalWrite(led,HIGH);
  delay(1000);
  digitalWrite(led,LOW);
  delay(1000);  
} else {
  digitalWrite(led,LOW);
}
if (leftstate == HIGH){
  digitalWrite(led,HIGH);
  delay(3000);
  digitalWrite(led,LOW);
  delay(3000);  
} else {
  digitalWrite(led,LOW);
}


}
