# Resister Pick and Place

Robotics project in progress with a simple goal: To utilize a robotic are equipped with an electromagnet and a camera to extract a single resistor from a pile of resistors.

## Milestone I: Completed

The first milestone of this project consisted of two fundimental goals. First, we wanted to verify the feasibilty of connecting to the WidowX robotic arm we have on hand for experimentation purposes as we develop this projcet. Through collaboration with an other project team, we were indeed able to verify that this would be reasonably attainable. 

Our second goal was to develop a simple algorithm for determining whether a given image contains zero, one, or many resistors. The most challenging part here was dealing with lighting, considering the wide variety of resistor colors and their reflective leads. We were eventually able to attain this goal provided we are able to make some key assumptions about the image. Our most successful technique thus far involves cropping the image down to include only a small square in the center, doing a contour search, and determining whether the area of the largest contour is in the expected range for a single resistor. Importantly, we assume here that the resistor is in the center of the image and the camera is a certain distance away (within a small range of error), factors that we hope to control to some extent when we incorperate the robotic arm. Notably, without these assumptions, we would not be able to crop the image without initial detection, nor filter based on how much of the image is occupied by the resistor. 

Considering how delicately the algorithm's success rests on those key assumptions, we plan to use multiple images from different persepctives as well as layering multiple filtering techniques.

## Milestone II: In progress


## MVP and Stretch Goals
