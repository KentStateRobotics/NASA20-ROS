import rclpy
import rclpy.node
import os
import ksr_msg.msg
import ksr_robot20.webserver.httpserver
import ksr_robot20.webserver.ws_server
import numpy as np
import numpy.linalg as npla
import math
from ament_index_python.packages import get_package_share_directory



class WebControl(rclpy.node.Node):
    def __init__(self):
        super().__init__('teleop')
        self.cmdPub = self.create_publisher(ksr_msg.msg.MotorVel, 'vel_cmd', 10)
        self.httpServer = ksr_robot20.webserver.httpserver.HttpServer(os.path.join(get_package_share_directory('ksr_robot20'), 'static'))
        self.wsServer = ksr_robot20.webserver.ws_server.WsServer(self.recvCallback)
        self.motorVelPub = self.create_publisher(ksr_msg.msg.MotorVel, 'vel_cmd', 10)
        #For converting angle and power to tank controls
        rotAngle = math.sin(math.pi / 4)
        self.rotateMatrix = np.array([[rotAngle, rotAngle],[-1 * rotAngle, rotAngle]])
        self.commandVector = np.array((0,0), dtype=np.float)

    def recvCallback(self, rcv):
        if(rcv["type"] == 'DriveCmd'):
            #For converting angle and power to tank controls
            vec = self.normalize(np.array((rcv["angle"], rcv["power"]), dtype=np.float))
            vec = np.matmul(self.rotateMatrix, vec)
            self.commandVector = self.squarelize(vec)
            #Construct message
            msg = ksr_msg.msg.MotorVel()
            msg.left = self.commandVector[0]
            msg.right = self.commandVector[1]
            self.cmdPub.publish(msg)
        elif(msg.type == 'ArmVel'):
            pass
    
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
    rclpy.init(args=args)
    driver = WebControl()
    try:
        rclpy.spin(driver)
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    main(sys.argv)