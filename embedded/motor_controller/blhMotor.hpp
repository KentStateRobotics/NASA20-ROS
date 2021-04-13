#ifndef BLH_MOTOR_H_
#define BLH_MOTOR_H_

#include <inttypes.h>
#include <Arduino.h>

#define MAX_MOTORS 8

class BLHMotor{
public:
    BLHMotor() {};
    BLHMotor(uint8_t motors, uint8_t startPin, uint8_t directionPin, uint8_t speedPin, uint8_t* pulsePins, int8_t direction);

    void setSpeed(int8_t speed);
    void checkPulsePin();
    void getPulseCounter(uint16_t* countBuffer);

private:
    uint8_t motors = 0;
    int8_t direction = 1;
    uint8_t startPin, directionPin, speedPin;
    uint8_t pulsePins[MAX_MOTORS];
    uint16_t pulseCounter[MAX_MOTORS];
    bool pulseState[MAX_MOTORS];
};
#endif
