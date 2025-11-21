import time


from xrinput import XRRuntime, ZMQPublisher

if __name__ == "__main__":

    print("初始化 OpenXR")

    xr_device = XRRuntime()
    pub = ZMQPublisher()

    while True:
        
        xr_data = xr_device.read_input()
        # print(xr_data)
        pub.send(xr_data)

        time.sleep(0.01)
        