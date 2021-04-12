#ifndef SABER_ACT_H_
#define SABER_ACT_H_

#include <inttypes.h>

class SaberAct{
public:
    SaberAct() {};
    SaberAct(uint8_t serialPin);

    void setSpeed(int8_t m1Speed, int8_t m2Speed);

private:
    int8_t m1Speed = 0, m2Speed = 0;
    uint8_t serialPin;
};
#endif
