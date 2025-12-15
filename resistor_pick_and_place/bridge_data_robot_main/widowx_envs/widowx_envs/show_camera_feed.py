#!/usr/bin/env python3

import argparse
import numpy as np
import cv2
from widowx_envs.widowx_env_service import WidowXClient, WidowXConfigs

def show_video(client, full_image=True):
    """
    This shows the video from the camera for a given duration.
    Full image is the image before resized to default 256x256.
    """
    res = client.get_observation()
    if res is None:
        print("No observation available... waiting")
        return

    if full_image:
        img = res["full_image"]
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    else:
        img = res["image"]
        img = (img.reshape(3, 256, 256).transpose(1, 2, 0) * 255).astype(np.uint8)
    cv2.imshow("Robot Camera", img)
    cv2.waitKey(20)  # 20 ms

def main():
    parser = argparse.ArgumentParser(description='Teleoperation for WidowX Robot')
    parser.add_argument('--ip', type=str, default='localhost')
    parser.add_argument('--port', type=int, default=5556)
    args = parser.parse_args()

    client = WidowXClient(host=args.ip, port=args.port)
    client.init(WidowXConfigs.DefaultEnvParams, image_size=256)

    cv2.namedWindow("Robot Camera")
    is_open = 1
    running = True
    while running:
        # Check for key press
        key = cv2.waitKey(100) & 0xFF

        # escape key to quit
        if key == ord('q'):
            print("Quitting camera view.")
            running = False
            continue

        show_video(client)

    client.stop()  # Properly stop the client
    cv2.destroyAllWindows()
    print("Teleoperation ended.")

if __name__ == "__main__":
    main()