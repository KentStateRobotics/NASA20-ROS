#include "blhMotor.hpp"

BLHMotor::BLHMotor(uint8_t motors, uint8_t startPin, uint8_t directionPin, uint8_t speedPin, uint8_t* pulsePins, int8_t direction){
    this->motors = motors;
    this->startPin = startPin;
    this->directionPin = directionPin;
    this->speedPin = speedPin;
    this->direction = direction;

    pinMode(startPin, OUTPUT);
    pinMode(directionPin, OUTPUT);
    pinMode(speedPin, OUTPUT);

    for(uint8_t i = 0; i < motors; ++i){
        this->pulsePins[i] = pulsePins[i];
        this->pulseCounter[i] = 0;
        this->pulseState[i] = false;
        pinMode(pulsePins[i], INPUT);
    }
}

void BLHMotor::setSpeed(int8_t speed){
    digitalWrite(this->directionPin, (speed > 0 == this->direction) ? HIGH : LOW);
    analogWrite(this->speedPin, abs(speed) << 1);
}

void BLHMotor::checkPulsePin(){
    for(uint8_t i = 0; i < motors; ++i){
        if(digitalRead(this->pulsePins[i])){
            this->pulseState[i] = true;
        }else{
            //Count on falling edge
            if(this->pulseState[i]){ 
                this->pulseCounter[i] += 1;
            }
            this->pulseState[i] = false;
        }
    }
}

void BLHMotor::getPulseCounter(uint16_t* countBuffer){
    for(uint8_t i = 0; i < motors; ++i){
        countBuffer[i] = this->pulseCounter[i];
        this->pulseCounter[i] = 0;
    }
}
