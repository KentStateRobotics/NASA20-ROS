import rclpy
import threading
import ksr_msg.msg
import sys

class TeleopKeyboardNode(rclpy.Node):
    def __init__(self):
        super().__init__('teleop')
        self.cmdPub = self.create_publisher(ksr_msg.msg.MotorVel, 'vel_cmd', 10)
        self.create_timer(.2, publishControls)
        self.drivePower = 0
        self.driveAngle = 0

    def publishControls(self):

    def keyboardInput():
        c = sys.stdin.read(1)
        if(c == 's'):
            self.driveAngle = -.5
        elif(c == 'a'):
            self.driveAngle = 0.5
        else:
            self.driveAngle = 0
        if(c == 'w'):
            self.drivePower = .5
        elif(c == 's'):
            self.drivePower = -.5
        else:
            self.drivePower = 0
        msg = ksr_msg.msg.MotorVel()
        msg.leftVel = self.drivePower * 
        msg.rightVel = 
        
        


def main(args=None):
    rclpy.init(args=args)
    driver = TeleopKeyboardNode()
    rclpy.spin(driver)

if __name__ == '__main__':
    main(sys.argv)