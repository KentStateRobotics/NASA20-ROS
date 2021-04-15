import rclpy
import rclpy.node
import ksr_msg.msg
import sys, select, termios, tty
import numpy as np
import numpy.linalg as npla
import math



class TeleopKeyboardNode(rclpy.node.Node):
    def __init__(self):
        super().__init__('teleop')
        self.cmdPub = self.create_publisher(ksr_msg.msg.MotorVel, 'vel_cmd', 10)
        rotAngle = math.sin(math.pi / 4)
        self.rotateMatrix = np.array([[rotAngle, rotAngle],[-1 * rotAngle, rotAngle]])
        self.commandVector = np.array((0,0), dtype=np.float)
        self.newSettings = termios.tcgetattr(sys.stdin.fileno())
        self.newSettings[3] = self.newSettings[3] & ~(termios.ECHO | termios.ICANON)
        self.newSettings[6][termios.VMIN] = 0
        self.newSettings[6][termios.VTIME] = 1
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.newSettings)
        self.create_timer(.3, self.publishControls)

    def publishControls(self):
        driveAngle = 0
        drivePower = 0
        for i in range(3):
            key = sys.stdin.read(1)
            if(key == ''): break
            if(key == 'd'):
                driveAngle = .5
            elif(key == 'a'):
                driveAngle = -.5
            if(key == 'w'):
                drivePower = .5
            elif(key == 's'):
                drivePower = -.5
        termios.tcflush(sys.stdin, termios.TCIFLUSH)
        vec = self.normalize(np.array((driveAngle, drivePower), dtype=np.float))
        vec = np.matmul(self.rotateMatrix, vec)
        self.commandVector = self.squarelize(vec)
        msg = ksr_msg.msg.MotorVel()
        msg.left = self.commandVector[0]
        msg.right = self.commandVector[1]
        self.cmdPub.publish(msg)
        
    def normalize(self, v):
        length = npla.norm(v, 2)
        if length == 0:
            return v
        return v / length

    def squarelize(self, v):
        length = npla.norm(v, 1)
        if length == 0:
            return v
        return v / length

def main(args=None):
    oldSettins = termios.tcgetattr(sys.stdin)
    rclpy.init(args=args)
    driver = TeleopKeyboardNode()
    try:
        rclpy.spin(driver)
    except (KeyboardInterrupt, Exception):
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, oldSettins)

if __name__ == '__main__':
    main(sys.argv)