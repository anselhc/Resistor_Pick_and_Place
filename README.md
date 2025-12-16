# Resister Pick and Place

## Overview
Welcome! This project is a simple proof of concept of a robust robotic resistor sorting system. It utilizes the [WidowX robotic arm](https://www.trossenrobotics.com/widowx-250), an 1080p [Logitech webcam](https://www.logitech.com/en-us/shop/p/c615-webcam), and a programmable electromagnet to implement a resistor pick and place program. The program works through trial and error. The arm attempts to extract a resistor with the electromagnet, checks whether it succeeded by holding it in front of the camera, and then either tries again or returns to a home position and drops the resistor. 

Our code is organized into two python files in bridge_data_robot_main/widowx_envs/widowx_envs: resistor_detector, which uses OpenCV to determine whether there are 0, 1, or more than 1 resistors in front of the camera, and main, which integrates the detection with the arm to repeatedly attempt to pick up a resistor until it verified that it succeeded to pick up exactly one. See requirements.txt for library reqs.

## The arm
<a href="https://www.trossenrobotics.com/widowx-250">
  <img src="media/d3716d_d76dcf2bab224f389689874d9cf3fa97~mv2.jpg.avif" alt="WidowX Arm" style="width: 25%; height: 25%; object-fit: cover;">
</a>

The WidowX Arm comes with open source code for its inverse kinematics, allowing for precise coordinate frame motion and correction. All code, however, must be executed in a docker container in the directory bridge_data_robot_main. For details on the computational setup, see the bridge_data_robot_main README. 

The [chess_bot](https://github.com/eddydpan/chess_bot/tree/main) repository was an invaluable reference for testing and debugging the WidowX arm computational setup. Several of the files regarding the computational setup we're modified based on this reppository.

## The camera
<img src="media/IMG_1793.JPG" alt="WidowX Arm" style="width: 25%; height: 25%; object-fit: cover;">

In order to ensure consistency, we 3D printed a resistor depot that we could mount the camera to and a cardboard backdrop. This is critical for the detection algorithm. The backdrop allows the algorithm to iscolate the end of the magnet precicely without interfering noise and the contrained camera location ensures that the resistors are in focus and an appropriate size in the image. The .ai file is included for specifics.

## The Electromagnet
<img src="media/IMG_1792.JPG" alt="WidowX Arm" style="width: 25%; height: 25%; object-fit: cover;">

We used an Arduino Uno as a power source and controller for the electromagnet. Because the ditial output pins cannot supply the required 5V to power it, the Arduino is wired to a relay that recieves power from the 5V pin and toggles on and off the magnet according to a digital signal. The magnet itself we mounted onto the arm where the gripper used to be using a 3D printed mount. See the image above for the full electrical system. Attached to it is a ~2.5mm diameter ferromagnetic steel rod to increase the precision of the magnet by concentrating the magnetic field.
