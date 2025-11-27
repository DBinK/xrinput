# zmq_sub.py
# 接收端（SUB）

import zmq
from rich import print

class ZMQSubscriber:
    """使用 Poller 的非阻塞 SUB"""

    def __init__(self, address="tcp://localhost:5555"):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.SUB)
        self.socket.setsockopt(zmq.CONFLATE, 1)  # 仅保留最新的1帧消息
        self.socket.connect(address)
        self.socket.setsockopt_string(zmq.SUBSCRIBE, "")

        self.poller = zmq.Poller()
        self.poller.register(self.socket, zmq.POLLIN)

        print(f"[ZMQ] Poll 模式接收端: {address}")

    def try_recv(self, timeout:int = 0):
        """timeout 毫秒，0 表示完全非阻塞"""
        socks = dict(self.poller.poll(timeout))
        if self.socket in socks and socks[self.socket] == zmq.POLLIN:
            return self.socket.recv_json()
        return None

    def recv(self):
        """阻塞接收一条消息"""
        return self.socket.recv_json()


if __name__ == "__main__":
    sub = ZMQSubscriber("tcp://localhost:5555")
    while True:
        data = sub.try_recv(timeout=500) 
        if data:
            print("收到:")
            print(data)
        else:
            print("没有收到数据")