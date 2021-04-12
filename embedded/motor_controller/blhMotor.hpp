#ifndef BLH_MOTOR_H_
#define BLH_MOTOR_H_

#include <inttypes.h>

class BLHMotor{
public:
    BLHMotor() {};
    BLHMotor(uint8_t startPint, uint8_t directionPin, uint8_t speedPint, uint8_t pulsePin);

    void setSpeed(int8_t speed);
    void checkPulsePin();
    void getPulseCounter();

private:
    int8_t speed = 0;
    uint16_t pulseCounter = 0;
    uint8_t startPint, directionPin, speedPint, pulsePin;
};
#endif
