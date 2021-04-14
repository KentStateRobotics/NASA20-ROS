from serial.serialutil import SerialException, to_bytes
import rclpy
import sys
import struct
import ksr_msg.msg
import tf2_ros
import serial
import serial.tools.list_ports
import threading

START_CHAR = '|'

class DriverNode(rclpy.Node):
    '''
    cmdMsg format: bbbb (right side motors, left side motors, elbow, wrist)
    feedbackMsg format: HHHHH (front right, back right, front left, back left, milliseconds)
    '''
    def __init__(self):
        super().__init__('driver')
        self.velSub = self.create_subscription(ksr_msg.msg.MotorVel, 'vel_cmd', onVelCmd, 10)
        self.velPub = self.create_publisher(ksr_msg.msg.MotorVel, 'vel', 10)
        self.connect()
        self.cmdStruct = struct.Struct("cbbbb")
        self.feedbackStruct = struct.Struct("HHHHH")
        self.leftVelCmd = 0
        self.leftSpeed = 0
        self.rightVelCmd = 0
        self.rightSpeed = 0
        self.elbowVelCmd = 0
        self.wristVelCmd = 0
        self.serialConn = None
        self.feedbackThread = threading.Thread(target=self.recvFeedback, daemon=True)
        self.feedbackThread.start()

    def connect():
        for p in serial.tools.list_ports.comports():
            if "Arduino" in p[1]:
                try:
                    self.serialConn = serial.Serial(port = p[0], baudrate = 115200)
                except SerialException as e:
                    self.get_logger().warn('Failed to connect to serial device')

    def onVelCmd(self, msg):
        self.leftVelCmd = min(max(-1, msg.leftVel), 1) * 127
        self.rightVelCmd = min(max(-1, msg.rightVel), 1) * 127
        try:
            self.serialConn.write(self.cmdStruct.pack(START_CHAR, self.rightVelCmd, self.leftVelCmd, self.elbowVelCmd, self.wristVelCmd))
        except SerialException as e:
            self.get_logger().warn('Failed to write to serial device')
        
    def recvFeedback(self):
        while(True):
            try:
                if(self.serialConn.read() == START_CHAR.to_bytes()):
                    data = self.serialConn.read(10)
                    data = self.feedbackStruct.unpack(data)

                    #Both pulse coutners / 2 counters * delta time millis / 1000 millis per sec / 30 pulses per rotation / 50 rps max speed 
                    self.rightSpeed = (data[0] + data[1]) * data[4] / 300000 
                    self.leftSpeed = (data[2] + data[3]) * data[4]  / 300000 

                    #TODO Check for large variation on either side

                    msg = ksr_msg.msg.MotorVel()
                    msg.leftVel = self.leftSpeed
                    msg.rightVel = self.rightSpeed
                    self.velPub.publish(msg)
            except SerialException as e:
                self.get_logger().warn('Failed to read from serial device')


def main(args=None):
    rclpy.init(args=args)
    driver = DriverNode()
    rclpy.spin(driver)

if __name__ == '__main__':
    main(sys.argv)
