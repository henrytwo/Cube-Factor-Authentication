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
String serial;
String serIn;


void setup()   /*----( SETUP: RUNS ONCE )----*/
{
  Serial.begin(9600);  // Used to type in characters
  lcd.begin(16,2);   // initialize the lcd for 16 chars 2 lines, turn on backlight 
  lcd.setCursor(0,0);
}

void clearLcd(){
  lcd.clear();
  delay(1000);  
}

void start(){
  lcd.setCursor(0,0);
  lcd.print("Hello user.");
  delay(1000);
  lcd.clear();
  
  lcd.print("Place cube in");
  lcd.setCursor(0,1);
  lcd.print("marked area.");
  delay(1000);
  lcd.clear();
}

void scanCube(){
  lcd.setCursor(0,0);
  lcd.print("Please wait as");
  lcd.setCursor(0,1);
  lcd.print("we scan the cube...");
  delay(1000);
  lcd.clear();
}

void writeLcd(){
  lcd.setCursor(0,0);
  lcd.clear();
  lcd.write(Serial.read());
}

void loop()   /*----( LOOP: RUNS CONSTANTLY )----*/
{
  while (started == true){
    start();  
  }
  
  if (Serial.available()) {
    lcd.clear();
    while (Serial.available() > 0) {
      lcd.write(Serial.read());
    }
  }
  
  Serial.println("Enter some shit here: ");
  
  while (Serial.available()==0)  
  {              
   // wait for user input
  }
  serial = Serial.readString();
  
  if (serial == "start"){
    Serial.print("Started Program.");
    start();
    started = true;
   }
   
  if (serial == "clearLcd"){
    Serial.print("Cleared.");
    clearLcd();
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
