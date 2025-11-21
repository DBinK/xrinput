# zmq_pub.py
# 广播端（PUB）

import zmq
from rich import print

class ZMQPublisher:
    """简单的 ZMQ 广播器，不绑定任何数据源"""

    def __init__(self, address: str = "tcp://*:5555"):
        self.address = address
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PUB)
        self.socket.bind(self.address)
        print(f"[ZMQ] 广播端启动: {self.address}")

    def send(self, data):
        """发送任意可 JSON 化的数据（dict/list/...）"""
        self.socket.send_json(data)
        # print(f"[发送] {data}")
