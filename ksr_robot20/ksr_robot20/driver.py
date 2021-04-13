import rclpy
import sys
import struct
import ksr_msg.msg
import tf2_ros
import serial
import serial.tools.list_ports

START_CHAR = '|'

class DriverNode(rclpy.Node):
    def __init__(self):
        super().__init__('driver')
        self.twistSubscriber = self.create_subscription(ksr_msg.msg.MotorCmd, 'vel_cmd', onVelCmd, 10)
        self.connect()
        self.cmdStruct = struct.Struct("cbbbb")
        self.feedbackStruct = struct.Struct("cHHHHH")

    def connect():
        for p in serial.tools.list_ports.comports():
            if "Arduino" in p[1]:
                self.serialConn = serial.Serial(port = p[0], baudrate = 115200)

    def onVelCmd(self, msg):
        
        self.serialConn.write(self.cmdStruct.pack())
        


def main(args=None):
    rclpy.init(args=args)
    driver = DriverNode()
    rclpy.spin(driver)

if __name__ == '__main__':
    main(sys.argv)
