import numpy as np
from scipy.stats import truncnorm
import time
import argparse
from Resistor_detector import switch_magnet
from widowx_env_service import WidowXClient, WidowXConfigs, WidowXStatus

magnet_path = "/dev/ttyACM0"
parser = argparse.ArgumentParser(
    description="WidowX robotic arm for 3D imaging with gaussian splatting"
)

parser.add_argument("--ip", type=str, default="localhost")
parser.add_argument("--port", type=int, default=5556)

# parser.add_argument('--repeats', type=int, default=4,
#                     help='Number of back-and-forth repeats')
# parser.add_argument('--sleep', type=float, default=1,
#                     help='Time to sleep between moves (seconds)')
# parser.add_argument('--pose1', type=float, nargs=6,
#                     default=[0.1, 0, 0.15, 0, 1.5, 0], help='First pose')
# parser.add_argument('--pose2', type=float, nargs=6,
#                     default=[0.1, 0.05, 0.15, 0, 1.5, 0], help='Second pose')

args = parser.parse_args()

# Initialization
client = WidowXClient(host=args.ip, port=args.port)
client.init(WidowXConfigs.DefaultEnvParams, image_size=256)
print("Waiting 5s to ensure server fully initialized...")
time.sleep(5)
print("Starting robot.")

# Grip magnet
prompt_user = input("Press enter to grip")
while prompt_user != "":
    time.sleep(1)
client.move_gripper(0.2)
time.sleep(1)

# Main loop
x_mean = 0.275
x_upper_bound = x_mean + 0.043
x_lower_bound = x_mean - 0.043
while prompt_user != "q":
    x_coord = 0
    while x_lower_bound > x_coord or x_upper_bound < x_coord:
        x_coord = np.random.normal(loc=x_mean, scale=0.05)
    switch_magnet(magnet_path, b"h\n")
    client.move(np.array([x_coord, 0, 0.1, 0, 1.5, 0]))
    client.move(np.array([x_coord, 0, 0.0175, 0, 1.5, 0]))
    time.sleep(1)
    client.move(np.array([x_coord, 0, 0.1, 0, 1.5, 0]))
    client.move(np.array([0.15, 0, 0.15, 0, 1.5, 0]))
    # switch_magnet(magnet_path, b"l\n")
    prompt_user = input("Press enter to pick and enter q to quit")
# Reset
client.move_gripper(1)
client.move(np.array([0, 0, 0, 0, 0, 0]))
