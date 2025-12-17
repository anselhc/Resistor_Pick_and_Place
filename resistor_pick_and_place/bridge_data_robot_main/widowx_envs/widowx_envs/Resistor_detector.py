import time
import serial
import cv2
from operator import itemgetter


def create_binary_contours(binary_image, invert=False):
    """
    Creates contours for binary images
    
    Args: 
        binary_image: a binary image
        invert: a boolean representing whether image colors are inverted

    Returns:
        countours: a list of contours
    """
    if invert:
        binary_image = cv2.bitwise_not(binary_image)

    contour_list, hierarchy = cv2.findContours(
        binary_image, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE
    )
    contour_areas = [cv2.contourArea(c) for c in contour_list]
    contours = [
        (contour_areas[i], contour_list[i]) for i in range(len(contour_list))
    ]
    contours = sorted(contours, key=itemgetter(0))[::-1]

    return contours


def detect_resistors(img):
    """
    Returns one of three conditions:
    there are no resistors,
    there is one resistor,
    and there are many resistors.

    Args:
        img: an image to process
    """
    # Define image dimensions
    img_length = len(img)
    img_width = len(img[0])
    img_center = (img_length // 2, img_width // 2)

    cropped_radius = 65
    img = img[
        img_center[0] - cropped_radius : img_center[0] + cropped_radius,
        img_center[1] - cropped_radius : img_center[1] + cropped_radius,
    ]
    # Define bounds for Red, Green, and Blue to include in binary image
    rl = 0
    rh = 50
    gl = 0
    gh = 100
    bl = 0
    bh = 100
    # Generate binary image
    binary_image = cv2.inRange(img, (rl, gl, bl), (rh, gh, bh))

    # Uncomment to display binary image
    # cv2.namedWindow("Binary image", cv2.WINDOW_NORMAL)
    # cv2.imshow("Binary image", binary_image)
    # cv2.imshow("Original image", img)
    # cv2.waitKey(0)

    # Generate contours
    resistor_contour = create_binary_contours(binary_image)
    try:
        resistor_contour = resistor_contour[0]
    except IndexError:
        resistor_contour = 0
    # Filter contours by area
    # resistor_contour = []
    # for i in contours:
    #     # if 15000 > i[0] > 300:
    #     resistor_contour.append(i[1])
    # print(resistor_contour[0])
    return resistor_metric(img, resistor_contour)


def resistor_metric(img, contour):
    """
    Given a cropped image and contour within that image,
    return how many resistors are present

    Args:
        img: a cropped image
        contour: an image contour

    Returns:
        "1" when one resistor is detected
        "0" when no resistors are detected
        ">1" when more than one resistor is detected
    """
    if type(contour) is not int: 
        single_resistor = (0.05, 0.005)
        no_resistor = 0.005
        # Get number of pixels in image
        total_pixels = len(img) * len(img[0])
        resistor_pixels = contour[0]
        print(resistor_pixels)
        print(total_pixels)
        if single_resistor[0] > resistor_pixels / total_pixels > single_resistor[1]:
            return "1"
        elif resistor_pixels / total_pixels < no_resistor:
            return "0"
        return ">1"
    return '0'

def switch_magnet(bit_string, usb_port):
    """
    Turns magnet on for h input or off for l input.

    args:
        string - A bit string encoding either h\n or l\n.
        usb_port - A string containing the usb port connected to the magnet.
    """
    try:
        # Configure the serial port (replace 'COM3' with your port name and 9600 with your baud rate)
        # On Linux, port might be '/dev/ttyAMA0' or '/dev/ttyUSB0'
        # On macOS, it might be something like '/dev/tty.usbmodem...'
        ser = serial.Serial(port=f"{usb_port}", baudrate=9600, timeout=1)

        # Wait a moment for the connection to establish
        time.sleep(2)

        # Data must be sent as bytes. Encode the string to bytes using b'' or .encode()
        data_to_send = usb_port
        data_to_send = bit_string

        # Write the data to the serial port
        ser.write(data_to_send)
        print(f"Sent: {data_to_send.decode().strip()}")

        # Optional: read back any response
        while ser.in_waiting > 0:
            response = ser.readline().decode("utf-8").strip()
            print(f"Received response: {response}")

    except serial.SerialException as e:
        print(f"Error: {e}")

    # Always close the port when done
    # if ser.isOpen():
    #     ser.close()
    #     print("Serial port closed.")


def get_video_frame():
    """
    From the camera feed, extracts a single frame and displays

    Returns:
        frame: a still image from the video camera
    """
    cap = cv2.VideoCapture(4)
    if not cap.isOpened():
        print("Cannot open camera")
        exit()
    ret, frame = cap.read()
    cv2.imshow('Video Frame', frame)
    return frame