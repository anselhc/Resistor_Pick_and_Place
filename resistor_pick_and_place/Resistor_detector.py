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
    # Define bounds for Red, Green, and Blue to include in binary image
    rl = 120
    rh = 190
    gl = 50
    gh = 90
    bl = 25
    bh = 290
    # Generate binary image
    binary_image = cv2.inRange(img, (rl, gl, bl), (rh, gh, bh))
    # Uncomment to display binary image
    # cv2.namedWindow("Binary image")
    # cv2.imshow("Binary image", binary_image)

    # Generate contours
    contours = create_binary_contours(binary_image)
    # Filter contours by area
    roost_contour = []
    for i in contours:
        if 750 > i[0] > 550:
            roost_contour.append(i[1])
    return roost_contour


if __name__ == "__main__":
    path = "Resistor_Pick_and_Place/Media/single_resistor.JPG"
    active = True
    test_image = cv2.imread(path)
    while active:
        roost_contour = detect_resistors(test_image)
        cv2.namedWindow("Original image")
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
