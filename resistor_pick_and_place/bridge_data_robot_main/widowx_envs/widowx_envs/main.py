import numpy as np
from scipy.stats import truncnorm
import time
import argparse
import cv2
from Resistor_detector import switch_magnet, detect_resistors, get_video_frame
from widowx_env_service import WidowXClient, WidowXConfigs, WidowXStatus

def pick_up_resistor():
    """
    Starts at neutral, moves to resistor bin, picks up resistor, holds in place
    """
    magnet_path = "/dev/ttyACM0"
    # parser = argparse.ArgumentParser(
    #     description="WidowX robotic arm for 3D imaging with gaussian splatting"
    # )

    # parser.add_argument("--ip", type=str, default="localhost")
    # parser.add_argument("--port", type=int, default=5556)

    # parser.add_argument('--repeats', type=int, default=4,
    #                     help='Number of back-and-forth repeats')
    # parser.add_argument('--sleep', type=float, default=1,
    #                     help='Time to sleep between moves (seconds)')
    # parser.add_argument('--pose1', type=float, nargs=6,
    #                     default=[0.1, 0, 0.15, 0, 1.5, 0], help='First pose')
    # parser.add_argument('--pose2', type=float, nargs=6,
    #                     default=[0.1, 0.05, 0.15, 0, 1.5, 0], help='Second pose')

    # args = parser.parse_args()

    # # Initialization
    # client = WidowXClient(host=args.ip, port=args.port)
    # client.init(WidowXConfigs.DefaultEnvParams, image_size=256)
    # print("Waiting 5s to ensure server fully initialized...")
    # time.sleep(5)
    # print("Starting robot.")

    # # Grip magnet
    # prompt_user = input("Press enter to grip")
    # while prompt_user != "":
    #     time.sleep(1)
    # client.move_gripper(0.2)
    # time.sleep(1)

    # Main loop
    x_mean = 0.275
    x_upper_bound = x_mean + 0.025
    x_lower_bound = x_mean - 0.025
    x_coord = 0

    z_mean = -0.02
    z_upper_bound = z_mean + 0.01
    z_lower_bound = z_mean - 0.01
    z_coord = 0
    #while prompt_user != "q":
    x_coord = 0
    while x_lower_bound > x_coord or x_upper_bound < x_coord:
        x_coord = np.random.normal(loc=x_mean, scale=0.015)
    while z_lower_bound > z_coord or z_upper_bound < z_coord:
        z_coord = np.random.normal(loc=z_mean, scale=0.005)
    switch_magnet(magnet_path, b"h\n")
    client.move(np.array([x_coord, 0, 0.06, 0, 1.5, 0]))
    client.move(np.array([x_coord, 0, -0.03, 0, 1.5, 0]))
    time.sleep(1)
    # return to home and drop magne
    client.move(np.array([x_mean, 0, 0.075, 0, 1.5, 0]))
    client.move(np.array([x_mean, -0.045, 0.075, 0, 1.5, 0]))
    # client.move(np.array([0.15, 0, 0.15, 0, 1.5, 0]))
    # switch_magnet(magnet_path, b"l\n")
        #prompt_user = input("Press enter to pick and enter q to quit")
    # Reset
    #client.move_gripper(1)
    #client.move(np.array([0, 0, 0, 0, 0, 0]))

def return_home():
    """
    Drops resistor, returns to home position
    """
    x_coord = 0
    client.move(np.array([x_coord, 0, 0.1, 0, 1.5, 0]))
    client.move(np.array([0.15, 0, 0.15, 0, 1.5, 0]))
    switch_magnet(magnet_path, b"l\n")

def integration():
    resistors_detected = "0"
    while resistors_detected != "1":
        # return_home()
        pick_up_resistor()
        time.sleep(0.5)
        image = get_video_frame()
        # image = image[100:-100, 50:-50] # May not need to crop image; backdrop fills entire window
        cv2.namedWindow("Video Frame", cv2.WINDOW_NORMAL)
        cv2.imshow('Video Frame', image)
        cv2.waitKey(1)
        resistors_detected = detect_resistors(image)
        print(resistors_detected)
    return_home()

if __name__ == "__main__":
    # Initialize
    magnet_path = "/dev/ttyACM0"
    parser = argparse.ArgumentParser(
        description="WidowX robotic arm for 3D imaging with gaussian splatting" #?????
    )

    parser.add_argument("--ip", type=str, default="localhost")
    parser.add_argument("--port", type=int, default=5556)

    args = parser.parse_args()

    client = WidowXClient(host=args.ip, port=args.port)
    client.init(WidowXConfigs.DefaultEnvParams, image_size=256)
    print("Waiting 5s to ensure server fully initialized...")
    time.sleep(5)
    print("Starting robot.")
    # pick_up_resistor()
    # Pick up resistors
    integration()

    # # Reset
    # client.move_gripper(1)
    # client.move(np.array([0, 0, 0, 0, 0, 0]))

    key = cv2.waitKey(20)
    if key == 27:
        cv2.destroyAllWindows()
        active = False

