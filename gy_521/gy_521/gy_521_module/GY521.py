import smbus
from .MPU6050 import mpu6050
import time

class GY521_module:
    def __init__(self,mpu_address=0x68,hmc_address=0x1E,bmp_address=0x77 , bus=1):
        self.bus = smbus.SMBus(bus)
        self.mpu = mpu6050(mpu_address)

    def bypass_i2c(self):
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

            print(f"Acceleration: X={accel['x']:.2f}m/s², Y={accel['y']:.2f}m/s², Z={accel['z']:.2f}m/s²")
            print(f"Rotation: X={gyro['x']:.2f}rad/s, Y={gyro['y']:.2f}rad/s, Z={gyro['z']:.2f}rad/s")
            print(f"Temperature ={temp:.2f}°C")
            print("")
            time.sleep(0.1)

if __name__ == "__main__":
    gy512=GY512()
    gy512.main()