#include <Servo.h>
#include <ESP8266WiFi.h>
#include <ArduinoOTA.h>

//  █   █ █▀▀ █▀▄▀█ █▀▀█ █▀▀     
//  █▄█▄█ █▀▀ █ ▀ █ █  █ ▀▀█     
//   ▀ ▀  ▀▀▀ ▀   ▀ ▀▀▀▀ ▀▀▀     
//  █▀▀ █▀▀ █▀▀█ ▀█ █▀ █▀▀█     █▀▀ █▀▀█ █▀▀▄ ▀█▀ █▀▀█ █▀▀█ █   
//  ▀▀█ █▀▀ █▄▄▀  █▄█  █  █     █   █  █ █  █  █  █▄▄▀ █  █ █   
//  ▀▀▀ ▀▀▀ ▀ ▀▀   ▀   ▀▀▀▀     ▀▀▀ ▀▀▀▀ ▀  ▀  ▀  ▀ ▀▀ ▀▀▀▀ ▀▀▀ 
// note: not deployed on the pi. this is for the wemos, only here for
// git history/backups.

Servo big_servo;  // Servo on D5
Servo little_servo;  // Servo on D6

// Access Point credentials
const char* apSSID = "WeMos_AP";        // Name of the access point
const char* apPassword = "password123"; // Password for the access point

// Minimum and maximum pulse widths --- this doesn't seem to have any impact. Maybe my servo is only 90 degrees?
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
    big_servo.attach(D5);
    little_servo.attach(D6);
    
    // Set servos to their initial positions
    big_servo.writeMicroseconds(MIN_PULSE_WIDTH);
    little_servo.writeMicroseconds(MIN_PULSE_WIDTH);
    Serial.println("Servos initialized.");
}

void loop() {
    ArduinoOTA.handle();  // Handle OTA updates

    if (Serial.available() > 0) {
        String command = Serial.readStringUntil('\n');
        command.trim();  
        Serial.print("Received command: ");
        Serial.println(command);

        // Parse the command for big_servo
        if (command.startsWith("move_big_servo_to_")) {
            int angle = command.substring(15).toInt();  // Extract the angle value
            if (angle >= 0 && angle <= 180) {
                int pulseWidth = map(angle, 0, 180, MIN_PULSE_WIDTH, MAX_PULSE_WIDTH);
                big_servo.writeMicroseconds(pulseWidth);
                Serial.println("Servo 1 moved to " + String(angle) + " degrees with pulse width: " + String(pulseWidth) + " µs");
            } else {
                Serial.println("Invalid angle for servo 1. Use an angle between 0 and 180.");
            }
        }
        // Parse the command for little_servo
        else if (command.startsWith("move_little_servo_to_")) {
            int angle = command.substring(15).toInt();  // Extract the angle value
            if (angle >= 0 && angle <= 180) {
                int pulseWidth = map(angle, 0, 180, MIN_PULSE_WIDTH, MAX_PULSE_WIDTH);
                little_servo.writeMicroseconds(pulseWidth);
                Serial.println("Servo 2 moved to " + String(angle) + " degrees with pulse width: " + String(pulseWidth) + " µs");
            } else {
                Serial.println("Invalid angle for servo 2. Use an angle between 0 and 180.");
            }
        } else {
            Serial.println("Unknown command.");
        }
    }
}
