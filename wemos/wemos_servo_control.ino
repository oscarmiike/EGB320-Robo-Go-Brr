#include <Servo.h>
#include <ESP8266WiFi.h>
#include <ArduinoOTA.h>

Servo bigservo;  // Servo on D5
Servo littleservo;  // Servo on D6

// Access Point credentials
const char* apSSID = "WeMos_AP";        // Name of the access point
const char* apPassword = "password123"; // Password for the access point

// Minimum and maximum pulse widths
const int MIN_PULSE_WIDTH = 500;   // Minimum pulse width in microseconds
const int MAX_PULSE_WIDTH = 2500;  // Maximum pulse width in microseconds

void setup() {
    delay(2000);  // Add delay to avoid initial garbage data
    Serial.begin(9600);  // Use 9600 baud rate 
    Serial.println("Booting as Access Point");

    // Set up Access Point
    WiFi.softAP(apSSID, apPassword);
    IPAddress myIP = WiFi.softAPIP();
    Serial.print("AP IP address: ");
    Serial.println(myIP);

    // Set up OTA
    ArduinoOTA.onStart([]() {
        Serial.println("Start OTA update");
    });
    ArduinoOTA.onEnd([]() {
        Serial.println("\nEnd OTA update");
    });
    ArduinoOTA.onProgress([](unsigned int progress, unsigned int total) {
        Serial.printf("Progress: %u%%\r", (progress / (total / 100)));
    });
    ArduinoOTA.onError([](ota_error_t error) {
        Serial.printf("Error[%u]: ", error);
        if (error == OTA_AUTH_ERROR) Serial.println("Auth Failed");
        else if (error == OTA_BEGIN_ERROR) Serial.println("Begin Failed");
        else if (error == OTA_CONNECT_ERROR) Serial.println("Connect Failed");
        else if (error == OTA_RECEIVE_ERROR) Serial.println("Receive Failed");
        else if (error == OTA_END_ERROR) Serial.println("End Failed");
    });
    ArduinoOTA.begin();

    // Attach servos to D5 and D6
    bigservo.attach(D5);
    littleservo.attach(D6);
    
    // Set servos to their initial positions
    bigservo.writeMicroseconds(MIN_PULSE_WIDTH);
    littleservo.writeMicroseconds(MIN_PULSE_WIDTH);
    Serial.println("Servos initialized.");
}

void loop() {
    ArduinoOTA.handle();  // Handle OTA updates

    if (Serial.available() > 0) {
        String command = Serial.readStringUntil('\n');
        command.trim();  // Remove extra whitespace
        Serial.print("Received command: ");
        Serial.println(command);

        // Parse the command for bigservo
        if (command.startsWith("move_bigservo_to_")) {
            Serial.println("Command recognized: move_bigservo_to");

            // substring index to extract the angle for bigservo
            String angleStr = command.substring(17);
            int angle = angleStr.toInt();
            
            Serial.print("Extracted angle for bigservo: ");
            Serial.println(angleStr);  
            Serial.print("Converted angle for bigservo: ");
            Serial.println(angle);  

            if (angle >= 0 && angle <= 180) {
                int pulseWidth = map(angle, 0, 180, MIN_PULSE_WIDTH, MAX_PULSE_WIDTH);
                Serial.print("Calculated pulse width for bigservo: ");
                Serial.println(pulseWidth);  

                bigservo.writeMicroseconds(pulseWidth);
                Serial.println("Servo 1 moved to " + String(angle) + " degrees with pulse width: " + String(pulseWidth) + " µs");
            } else {
                Serial.println("Invalid angle for servo 1. Use an angle between 0 and 180.");
            }
        }
        // Parse the command for littleservo
        else if (command.startsWith("move_littleservo_to_")) {
            Serial.println("Command recognized: move_littleservo_to");

            // substring index to extract the angle for littleservo
            String angleStr = command.substring(20);
            int angle = angleStr.toInt();

            Serial.print("Extracted angle for littleservo: ");
            Serial.println(angleStr);  
            Serial.print("Converted angle for littleservo: ");
            Serial.println(angle); 

            if (angle >= 0 && angle <= 180) {
                int pulseWidth = map(angle, 0, 180, MIN_PULSE_WIDTH, MAX_PULSE_WIDTH);
                Serial.print("Calculated pulse width for littleservo: ");
                Serial.println(pulseWidth); 

                littleservo.writeMicroseconds(pulseWidth);
                Serial.println("Servo 2 moved to " + String(angle) + " degrees with pulse width: " + String(pulseWidth) + " µs");
            } else {
                Serial.println("Invalid angle for servo 2. Use an angle between 0 and 180.");
            }
        } else {
            Serial.println("Unknown command.");
        }
    }
}
