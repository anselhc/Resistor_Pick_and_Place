import numpy as np
from scipy.stats import truncnorm
import time
import argparse
import cv2
from Resistor_detector import switch_magnet, detect_resistors, get_video_frame
from widowx_env_service import WidowXClient, WidowXConfigs, WidowXStatus

def pick_up_resistor():
    """
    Pick up a resistor from the bin and hold it in front of the camera.
    """
    magnet_path = "/dev/ttyACM0"

    x_mean = 0.275
    x_upper_bound = x_mean + 0.025
    x_lower_bound = x_mean - 0.025
    x_coord = 0

    z_mean = -0.02
    z_upper_bound = z_mean + 0.01
    z_lower_bound = z_mean - 0.01
    z_coord = 0
    x_coord = 0

    while x_lower_bound > x_coord or x_upper_bound < x_coord:
        x_coord = np.random.normal(loc=x_mean, scale=0.015)
    while z_lower_bound > z_coord or z_upper_bound < z_coord:
        z_coord = np.random.normal(loc=z_mean, scale=0.005)

    switch_magnet(magnet_path, b"h\n")
    # Move the arm to the bin of resistors
    client.move(np.array([x_coord, 0, 0.06, 0, 1.5, 0]))
    client.move(np.array([x_coord, 0, -0.03, 0, 1.5, 0]))
    time.sleep(1)
    # Lift the arm vertically and move towards camera backdrop
    client.move(np.array([x_mean, 0, 0.075, 0, 1.5, 0]))
    client.move(np.array([x_mean, -0.045, 0.075, 0, 1.5, 0]))

def return_home():
    """
    Return the arm to the home position and switch off the magnet.
    """
    x_coord = 0
    client.move(np.array([x_coord, 0, 0.1, 0, 1.5, 0]))
    client.move(np.array([0.15, 0, 0.15, 0, 1.5, 0]))
    switch_magnet(magnet_path, b"l\n")

def integration():
    """
    Lower the arm into the bin until a single resistor has been picked up.
    """
    resistors_detected = "0"
    while resistors_detected != "1":
        pick_up_resistor()
        time.sleep(0.5)
        image = get_video_frame()
        cv2.namedWindow("Video Frame", cv2.WINDOW_NORMAL)
        cv2.imshow('Video Frame', image)
        cv2.waitKey(1)
        resistors_detected = detect_resistors(image)
        print(resistors_detected)
    return_home()

if __name__ == "__main__":
    # Initialize arm
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
    
    # Pick up a resistor
    integration()

    key = cv2.waitKey(20)
    if key == 27:
        cv2.destroyAllWindows()
        active = False

