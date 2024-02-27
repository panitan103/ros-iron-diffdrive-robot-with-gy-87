import smbus

from .MPU6050 import mpu6050


class GY521_module:
    def __init__(self,mpu_address=0x68, bus=1):
        self.bus = smbus.SMBus(bus)
        self.mpu = mpu6050(mpu_address)

        self.mpu.bypass_i2c()
    def get_all_data(self):
        accel = self.mpu.get_accel_data()
        gyro = self.mpu.get_gyro_data()
        temp = self.mpu.get_temp()

        return [accel, gyro, temp]
    def main(self):
        while True:
            [accel, gyro, temp]=self.get_all_data()
            # print(self.get_all_data())
            print(f"Acceleration: X={accel['x']:.2f}g, Y={accel['y']:.2f}g, Z={accel['z']:.2f}g")
            print(f"Rotation: X={gyro['x']:.2f}rad/s, Y={gyro['y']:.2f}rad/s, Z={gyro['z']:.2f}rad/s")
            print(f"Temperature ={temp:.2f}°C")

            print("")

if __name__ == "__main__":
    gy521=GY521_module()
    gy521.main()