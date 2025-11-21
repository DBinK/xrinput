import time

from rich import print  # (可选项) 推荐使用 rich 打印更美观

from xrinput import XRRuntime

if __name__ == "__main__":

    print("初始化 OpenXR")

    xr_device = XRRuntime()

    while True:
        
        xr_data = xr_device.read_input()
        print(xr_data)

        time.sleep(0.01)
        