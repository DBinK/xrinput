import random
import time 
from xrinput import CommandLinePanel

panel = CommandLinePanel(title="中控面板", float_precision=4)
panel.start()

data_dict = {
    "index": 0,
    "xr_name": "quest3",
    "xr_grip": 0.0,
    "xr_pos": [0.0, 0.0, 0.0]
}

index = 0

while True:

    index += 1
    
    data_dict = {
    "index": index,
    "xr_name": "quest3",
    "xr_grip": random.uniform(0, 1),
    "xr_pos": [random.uniform(-1, 1), random.uniform(-1, 1), random.uniform(-1, 1)]
    }   

    panel.update(data_dict)

    time.sleep(0.1)

    

