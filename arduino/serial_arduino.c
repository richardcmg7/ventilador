const int analogIn = A7;
int analogVal = 0;

void setup(){
	Serial.begin(115200);
}

void loop(){
	analogVal = analogRead(analogIn);
	Serial.println(analogIn);
	delay(100);
}