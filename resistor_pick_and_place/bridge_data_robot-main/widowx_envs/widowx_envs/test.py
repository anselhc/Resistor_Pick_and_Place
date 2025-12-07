#!/usr/bin/env python3

import argparse
import numpy as np
import threading
import time
from widowx_env_service import WidowXClient, WidowXConfigs, WidowXStatus
import sys
import os
# from tf.transformations import quaternion_from_euler
# from tf.transformations import quaternion_matrix


def main():
    captures = 0
    parser = argparse.ArgumentParser(
        description='WidowX robotic arm for 3D imaging with gaussian splatting')

    parser.add_argument('--ip', type=str, default='localhost')
    parser.add_argument('--port', type=int, default=5556)

    parser.add_argument('--repeats', type=int, default=4,
                        help='Number of back-and-forth repeats')
    parser.add_argument('--sleep', type=float, default=1,
                        help='Time to sleep between moves (seconds)')
    parser.add_argument('--pose1', type=float, nargs=6,
                        default=[0.1, 0, 0.15, 0, 1.5, 0], help='First pose')
    parser.add_argument('--pose2', type=float, nargs=6,
                        default=[0.1, 0.05, 0.15, 0, 1.5, 0], help='Second pose')

    args = parser.parse_args()

    # Initialization
    client = WidowXClient(host=args.ip, port=args.port)
    client.init(WidowXConfigs.DefaultEnvParams, image_size=256)
    print('Waiting 5s to ensure server fully initialized...')
    time.sleep(5)
    print("Starting robot.")

    # Reset
    print('Resetting robot to neutral')
    r = client.reset()
    print('Reset status:', r)
    time.sleep(2)

    # p1 = np.array(args.pose1)
    # p2 = np.array(args.pose2)
    # repeats = args.repeats
    # sleep_between = args.sleep

    # for i in range(repeats):
    #     print(f'Cycle {i+1}: moving to pose 1')
    #     res1 = client.move(p1, blocking=True)
    #     print('Move to pose1 result:', res1)
    #     time.sleep(sleep_between)

    #     print(f'Cycle {i+1}: moving to pose 2')
    #     res2 = client.move(p2, blocking=True)
    #     print('Move to pose2 result:', res2)
    #     time.sleep(sleep_between)

    # test - .3 as center

    radius = .1
    angles = np.linspace(0, 2*np.pi, 20)

    xs = np.array(radius*np.cos(angles)) + 0.3
    ys = -np.array(radius*np.sin(angles))
    rolls = np.array(angles)

    client.move(np.array([xs[0], ys[0], 0.025, rolls[0], 1.5, 0]))
    time.sleep(5)

    for i in range(10):
        client.move(np.array([xs[i], ys[i], 0.025, rolls[i], 1.5, 0]))
        time.sleep(1)

    for i in range(3):
        client.move(np.array([xs[9], ys[9], 0.025, (rolls[9]-((i+1)*rolls[9]/3)), 1.5, 0]))
        time.sleep(0.5)

    for i in range(10):
        client.move(np.array([xs[i+10], ys[i+10], 0.025, rolls[i+10], 1.5, 0]))
        time.sleep(1)

    print("finished")
    time.sleep(10)
    client.move(np.array([0.15, 0, 0.15, 0, 1.5, 0]))

# def get_tf_mat(pose):
#     # convert pose to a 4x4 tf matrix, rpy to quat
#     quat = quaternion_from_euler(pose[3], pose[4], pose[5])
#     tf_mat = quaternion_matrix(quat)
#     tf_mat[:3, 3] = pose[:3]
#     return tf_mat


if __name__ == "__main__":
    main()
