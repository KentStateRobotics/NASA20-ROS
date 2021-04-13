#include "ksrConsts.hpp"
#include "blhMotor.hpp"
#include <SoftwareSerial.h>
#include <Sabertooth.h>

BLHMotor PMotors, SMotors;
SoftwareSerial saberSerial(NOT_A_PIN, PIN_SABER_SERIAL);
Sabertooth ST(128, saberSerial);

char buffer[8];
uint32_t lastUpdate = 0;

void setup(){
    Serial.begin(OUT_BAUD);
    uint8_t pulsePins[2] = {PIN_P_F_PULSE, PIN_P_R_PULSE};
    PMotors = BLHMotor(2, PIN_P_START, PIN_P_DIR, PIN_P_SPEED, pulsePins, DIRECTION_P);
    uint8_t pulsePins2[2] = {PIN_S_F_PULSE, PIN_S_R_PULSE};
    SMotors = BLHMotor(2, PIN_S_START, PIN_S_DIR, PIN_S_SPEED, pulsePins2, DIRECTION_S);
    saberSerial.begin(9600);
    ST.autobaud();
}

void loop(){
    while(Serial.available() >= CMD_MSG_LENGTH + 1){
        if(Serial.read() == MSG_START_CHAR){
            Serial.readBytes(buffer, CMD_MSG_LENGTH);
            SMotors.setSpeed(static_cast<int8_t>(buffer[0]));
            SMotors.setSpeed(static_cast<int8_t>(buffer[1]));
            ST.motor(1, static_cast<int8_t>(buffer[2]));
            ST.motor(2, static_cast<int8_t>(buffer[3]));
        }
    }

    PMotors.checkPulsePin();
    SMotors.checkPulsePin();

    if(lastUpdate + UPDATE_DELAY >= millis()){
        uint16_t deltaTime = millis() - lastUpdate;
        lastUpdate = millis();
        SMotors.getPulseCounter(reinterpret_cast<uint16_t*>(buffer));
        PMotors.getPulseCounter(reinterpret_cast<uint16_t*>(&(buffer[4])));
        Serial.write('|');
        Serial.write(buffer, 8);
        Serial.write(deltaTime);
    }
}
