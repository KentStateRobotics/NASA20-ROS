import rclpy
import rclpy.node
import ksr_msg.msg
import pygame
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
        self.create_timer(.3, self.publishControls)

    def publishControls(self):
        driveAngle = 0
        drivePower = 0
        if(pygame.key.get_pressed()[pygame.K_d]):
            driveAngle = .5
        elif(pygame.key.get_pressed()[pygame.K_a]):
            driveAngle = -.5
        else:
            driveAngle = 0
        if(pygame.key.get_pressed()[pygame.K_w]):
            drivePower = .5
        elif(pygame.key.get_pressed()[pygame.K_s]):
            drivePower = -.5
        else:
            drivePower = 0
        vec = self.normalize(np.array((driveAngle, drivePower), dtype=np.float))
        vec = np.matmul(self.rotateMatrix, vec)
        self.commandVector = self.squarelize(vec)
        msg = ksr_msg.msg.MotorVel()
        msg.left = self.commandVector[0]
        msg.right = self.commandVector[1]
        self.cmdPub.publish(msg)
        pygame.event.pump()
        
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
    print("Initalizeing...")
    pygame.init()
    print("Initalization complete")
    rclpy.init(args=args)
    driver = TeleopKeyboardNode()
    rclpy.spin(driver)

if __name__ == '__main__':
    main(sys.argv)