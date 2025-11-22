import cv2
from operator import itemgetter


def create_binary_contours(binary_image, invert=False):
    """Creates contours for binary images"""
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
    """
    # Define image dimensions
    img_length = len(img)
    img_width = len(img[0])
    img_center = (img_length // 2, img_width // 2)

    cropped_radius = 400
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
    cv2.namedWindow("Binary image", cv2.WINDOW_NORMAL)
    cv2.imshow("Binary image", binary_image)

    # Generate contours
    contours = create_binary_contours(binary_image)
    # Filter contours by area
    resistor_contour = []
    for i in contours:
        # if 15000 > i[0] > 300:
        resistor_contour.append(i[1])
        print(resistor_contour[0])
    return resistor_contour[0]


def resistor_metric(img, resistor_contour):
    """
    Given a cropped image and contour within that image,
    return how many resistors are present
    """
    single_resistor = 0.85
    no_resistor = 0.1
    # Get number of pixels in image
    total_pixels = len(img) * len(img[0])
    resistor_pixels = resistor_contour[0]
    if no_resistor < resistor_pixels < single_resistor:
        return "1"
    elif resistor_pixels < no_resistor:
        return "0"
    return ">1"


if __name__ == "__main__":
    path = "Media/IMG_8447.JPG"
    active = True
    test_image = cv2.imread(path)
    # test_image = test_image[:-1000, 250:]
    roost_contour = detect_resistors(test_image)
    while active:
        cv2.namedWindow("Original image", cv2.WINDOW_NORMAL)
        cv2.imshow("Original image", test_image)
        for i in enumerate(roost_contour):
            cv2.drawContours(
                test_image,
                roost_contour,
                i[0],
                (0, 0, 255),
                1,
            )
        key = cv2.waitKey(20)
        if key == 27:
            cv2.destroyAllWindows()
            active = False
