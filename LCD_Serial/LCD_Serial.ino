/*-----( Import needed libraries )-----*/
#include <Wire.h>  // Comes with Arduino IDE
// Get the LCD I2C Library here: 
// https://bitbucket.org/fmalpartida/new-liquidcrystal/downloads
// Move any other LCD libraries to another folder or delete them
// See Library "Docs" folder for possible commands etc.
#include <LiquidCrystal_I2C.h>

LiquidCrystal_I2C lcd(0x3F, 2, 1, 0, 4, 5, 6, 7, 3, POSITIVE);  // Set the LCD I2C address

/*-----( Declare Variables )-----*/
int pos = 0;
bool started = false;
bool idleMode = true;
String serial;
String serIn;
String code = "fuck u";
int light = 2;



void setup()   /*----( SETUP: RUNS ONCE )----*/
{
  Serial.begin(9600);  // Used to type in characters
  lcd.begin(16,2);   // initialize the lcd for 16 chars 2 lines, turn on backlight 
  lcd.setCursor(0,0);
  pinMode(light, OUTPUT);
  
}
/**
 * idle
 * instruction state - gets cube name and goes thru scanning state
 * display 2FA for loop countdown timer
 * 
 */
void deny(){
  Serial.println("ha get fucked");
  lcd.clear();
  delay(1000);
  lcd.setCursor(0,0);
  lcd.write("U gei fuck.");
  delay(1000);
  }
void clearLcd(){
  lcd.clear();
  delay(1000);  
}

void idle(){
  digitalWrite(light, LOW);
  lcd.clear();
  lcd.setCursor(0,0);
  lcd.write("Welcome to");
  lcd.setCursor(0,1);
  lcd.write("Cube Factor");
  delay(2000);
  lcd.clear();
  lcd.setCursor(0,0);
  lcd.write("Cube Factor");
  lcd.setCursor(0,1);
  lcd.write("Authentication");
  delay(1000);  
}

void start(){
  digitalWrite(light, HIGH);
  lcd.setCursor(0,0);  
  lcd.print("Place cube in");
  lcd.setCursor(0,1);
  lcd.print("front of camera.");
  delay(1000);
  lcd.clear();
  
  lcd.setCursor(0,0);
  lcd.print("Follow the");
  lcd.setCursor(0,1);
  lcd.print("instructions");
  delay(1000);
  lcd.clear();
  
  lcd.setCursor(0,0);
  lcd.print("on screen.");
  delay(1000);
  lcd.clear();
}

void twoFA(){
  lcd.clear();
  lcd.setCursor(0,0);
  lcd.write("Code: ");
  lcd.setCursor(6,0);
  lcd.print(code);
  lcd.setCursor(0,1);
  lcd.write("Expires in: ");
  delay(1000);
  }
  
void scanCube(){
  digitalWrite(light, HIGH);
  lcd.setCursor(0,0);
  lcd.print("Please wait until");
  lcd.setCursor(0,1);
  lcd.print("scan is done.");
  delay(5000);
  lcd.clear();
}

void writeLcd(){
  lcd.setCursor(0,0);
  lcd.clear();
  lcd.write(Serial.read());
}

void loop()   /*----( LOOP: RUNS CONSTANTLY )----*/
{
  while (idleMode == true){
    if (serial.length() != 0){
      idleMode = false;
      }
    idle();
    Serial.println("Enter some shit here: ");
    serial = Serial.readString();
    if (serial.length()>0) {
      idleMode = false;
    }
  }
 
  while (started == true){
    if (serial.length() != 0){
      started = false;
      idleMode = true;
      }
    start();
    scanCube();
    Serial.println("Enter some shit here: ");
    serial = Serial.readString();
    if (serial.length()>0) {
      started = false;
      idleMode = true;
    }
  }
 /** 
  if (Serial.available()) {
    lcd.clear();
    while (Serial.available() > 0) {
      lcd.write(Serial.read());
    }
  }
  **/
 
  if (serial == "start"){
    Serial.print("Started Program.");
    start();
    started = true;
    idleMode = false;
   }
   
  if (serial == "clearLcd"){
    Serial.print("Cleared.");
    clearLcd();
    idleMode = true;
   }
    
  if (serial == "2FA"){
     Serial.print("code generated!");
     while (Serial.available() > 0) {
      lcd.write(Serial.read());
    }
     code = Serial.readString();
     twoFA();
     
     for (int t = 30; t >= 0; t--){
      if (t < 10){
        lcd.setCursor(13,1);
        lcd.print(" ");
       }
      lcd.setCursor(12,1);
      lcd.print(t);
      delay(500);
      if (t == 0){
        lcd.clear();
        idleMode = true;
        idle();
        delay(1000);
        }
      }
    }   
  if (serial == "deny"){
    deny();
    delay(2000);
    idleMode = true;
    idle();
    }
  if (serial == "writeLcd"){
    Serial.print("Enter chars to print: ");
    while (Serial.available()==0)  
    {              
   // wait for user input
    }
    serIn = Serial.readString();
    writeLcd();
   }
}


/* ( THE END ) */
