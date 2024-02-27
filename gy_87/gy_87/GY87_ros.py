import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Imu
from sensor_msgs.msg import MagneticField
from rclpy.clock import ROSClock




from .gy_87_module.GY87 import GY87_module

class GY87_Publisher(Node):

    def __init__(self):
        super().__init__('minimal_publisher')
        self.publisher_imu = self.create_publisher(Imu,'/imu_data', 10)
        self.publisher_mag = self.create_publisher(Imu,'/mag_data', 10)
        self.ros_clock = ROSClock()
        self.imu_msg = Imu()
        self.mag_msg=MagneticField()

        timer_period = 0.1  # seconds
        self.gy87 = GY87_module()
        self.timer = self.create_timer(timer_period, self.timer_callback)

    def timer_callback(self):
         # Read data from GY87.py
        # Replace the following lines with the appropriate code to read data from GY87.py

        [accel, gyro, temp, mag, pressure]=self.gy87.get_all_data()
        print(f"Acceleration: X={accel['x']:.2f}m/s², Y={accel['y']:.2f}m/s², Z={accel['z']:.2f}m/s²")
        print(f"Rotation: X={gyro['x']:.2f}rad/s, Y={gyro['y']:.2f}rad/s, Z={gyro['z']:.2f}rad/s")
        print(f"Temperature ={temp:.2f}°C")
        print(f"Magnetrometer: X={mag['x']:.2f}µT, Y={mag['y']:.2f}µT, Z={mag['z']:.2f}µT")
        print(f"Pressure= {pressure:.2f}hPa")
        print("")

        self.imu_msg.header.stamp = self.get_clock().now().to_msg()
        self.imu_msg.linear_acceleration.x = accel['x']
        self.imu_msg.linear_acceleration.y = accel['y']
        self.imu_msg.linear_acceleration.z = accel['z']
        self.imu_msg.angular_velocity.x = gyro['x']
        self.imu_msg.angular_velocity.y = gyro['y']
        self.imu_msg.angular_velocity.z = gyro['z']

        self.mag_msg.header.stamp = self.get_clock().now().to_msg()
        self.mag_msg.magnetic_field.x = mag['x']
        self.mag_msg.magnetic_field.y = mag['y']
        self.mag_msg.magnetic_field.z = mag['z']

        self.publisher_imu.publish(self.imu_msg)
        self.publisher_mag.publish(self.imu_msg)

def main(args=None):
    rclpy.init(args=args)

    gy87_publisher = GY87_Publisher()

    rclpy.spin(gy87_publisher)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    gy87_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()