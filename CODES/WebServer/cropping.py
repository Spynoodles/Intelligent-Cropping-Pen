import math


def hp(resolution,Distance,angle):


    Object_height=math.tan(angle)*Distance
    Heigh_Pixels=abs(resolution*math.tan(Object_height/2*185/360*math.pi))
    return Heigh_Pixels

def crop(angle,Distance):

    from PIL import Image

    # Load the image
    image = Image.open("pen_img.jpg")
    image = image.transpose(Image.FLIP_TOP_BOTTOM)
    object_height_pixels = hp(math.sqrt(320*320+240*240),Distance,angle)  # Height of the object in pixels
    print("Pixel size:",object_height_pixels)
    center_x = image.width // 2
    center_y = image.height // 2
    half_side_length = object_height_pixels
    center_y=image.height//2  -50
    left = center_x - half_side_length
    top = center_y - half_side_length
    right = center_x + half_side_length
    bottom = center_y + half_side_length
    cropped_image = image.crop((left, top, right, bottom))

    cropped_image.save("cropped_image.jpg")
    cropped_image.show()

import cv2


def cv():

    import cv2

    net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")

    if net.empty():
        print("Error: Unable to load YOLOv3 model.")
        exit()

    with open("coco.names", "r") as f:
        classes = [line.strip() for line in f.readlines()]

    # Read input image
    image = cv2.imread("cropped_image.jpg")

    if image is None:
        print("Error: Unable to load image.")
        exit()

    blob = cv2.dnn.blobFromImage(image, 1/255.0, (416, 416), swapRB=True, crop=False)

    net.setInput(blob)

    output_layers = net.getUnconnectedOutLayersNames()

    outs = net.forward(output_layers)

    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = scores.argmax()
            confidence = scores[class_id]
            if confidence > 0.5:
                label = classes[class_id]
                print(label)
