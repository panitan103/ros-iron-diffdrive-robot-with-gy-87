import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Imu

from .gy_521_module.GY521 import GY521_module

class GY521_Publisher(Node):

    def __init__(self):
        super().__init__('minimal_publisher')
        self.publisher_imu = self.create_publisher(Imu,'/imu_data', 10)

        self.imu_msg = Imu()

        timer_period = 0  # seconds
        self.gy521 = GY521_module()
        self.timer = self.create_timer(timer_period, self.timer_callback)

    def timer_callback(self):
         # Read data from GY521.py
        # Replace the following lines with the appropriate code to read data from GY521.py

        [accel, gyro, temp]=self.gy521.get_all_data()
        print(f"Acceleration: X={accel['x']:.2f}m/s², Y={accel['y']:.2f}m/s², Z={accel['z']:.2f}m/s²")
        print(f"Rotation: X={gyro['x']:.2f}rad/s, Y={gyro['y']:.2f}rad/s, Z={gyro['z']:.2f}rad/s")
        print(f"Temperature ={temp:.2f}°C")
        print("")

        self.imu_msg.header.stamp = self.get_clock().now().to_msg()
        self.imu_msg.linear_acceleration.x = accel['x']
        self.imu_msg.linear_acceleration.y = accel['y']
        self.imu_msg.linear_acceleration.z = accel['z']
        self.imu_msg.angular_velocity.x = gyro['x']
        self.imu_msg.angular_velocity.y = gyro['y']
        self.imu_msg.angular_velocity.z = gyro['z']

        self.publisher_imu.publish(self.imu_msg)

def main(args=None):
    rclpy.init(args=args)

    gy521_publisher = GY521_Publisher()

    rclpy.spin(gy521_publisher)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    gy521_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()