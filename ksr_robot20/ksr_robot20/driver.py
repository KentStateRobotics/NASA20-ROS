import rclpy
import sys
import geometry_msgs.msg
import tf2_ros

class DriverNode(rclpy.Node):
    def __init__(self):
        super().__init__('driver')
        self.twistSubscriber = self.create_subscription(geometry_msgs.msg.Twist, 'vel_cmd', onVelCmd, 10)

    def onVelCmd(self, msg):
        pass


def main(args=None):
    rclpy.init(args=args)
    driver = DriverNode()
    rclpy.spin(driver)

if __name__ == '__main__':
    main(sys.argv)
