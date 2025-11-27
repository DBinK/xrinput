from rich import print
from xrinput import ZMQSubscriber

sub = ZMQSubscriber()

while True:
    data = sub.try_recv(timeout=500)
    if data:
        print("收到:")
        print(data)