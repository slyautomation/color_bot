#include <Mouse.h>
int buttonPin = 9;  // Set a button to any pin

void setup() {
  Serial.begin(115200);
  Serial.setTimeout(1);
  // pinMode(buttonPin, INPUT);  // Set the button as an input
  digitalWrite(buttonPin, HIGH);  // Pull the button high
  delay(1000);  // short delay to let outputs settle
  Mouse.begin(); //Init mouse emulation
}

void loop() {
  if (Serial.available() > 0) {
    String input = Serial.readStringUntil('\n'); // Read the serial input until newline character
    input.trim(); // Remove leading and trailing spaces
    //Serial.println(input);
    // Check if the input is a valid format
    if (input == "left") {
        Mouse.click(MOUSE_LEFT);
      }
      if (input == "right") {
        Mouse.click(MOUSE_RIGHT);
      }
      else
      {
    //if (input.startsWith("[") && input.endsWith("]")) {
      input.remove(0, 1); // Remove the leading '['
      input.remove(input.length() - 1); // Remove the trailing ']'
      //Serial.println(input);
      char charArray[input.length() + 1];
      
      input.toCharArray(charArray, sizeof(charArray));
      //Serial.println("char array");
      //Serial.println(charArray);
      char* pair = strtok(charArray, ", ");
      //Serial.println(pair);
      while (pair != NULL) {
        String pairStr = pair;
        //Serial.println(pair);
        //pairStr.trim();
        pairStr.remove(0, 1); // Remove the leading '('
        pairStr.remove(pairStr.length() - 1); // Remove the trailing ')'

        int commaIndex = pairStr.indexOf(":");
        if (commaIndex != -1) {
          String xStr = pairStr.substring(0, commaIndex);
          String yStr = pairStr.substring(commaIndex + 1);

          int x = xStr.toInt();
          int y = yStr.toInt();
          //Serial.println(x);
          //Serial.println(y);
          float lim = (float)1 + ((float)100/(float)254);
          //Serial.println(lim);
          // Move the mouse to the specified coordinates
          int finx = round((float)x * (float)lim); // adjust for 127 limitation of arduino
          int finy = round((float)y * (float)lim); // adjust for 127 limitation of arduino
          //Serial.println(finx);
          //Serial.println(finy);
          Mouse.move(finx, finy, 0);

          //delay(1); // Add a delay to prevent rapid movements
        }

        pair = strtok(NULL, ", ");
      }
    }
  }
  Serial.flush();
  //Serial.End();
  //Serial.begin(115200);
  }