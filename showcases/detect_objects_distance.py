from com.ml.objects.Detection import ObjectDetection
from com.ml.utils.distance import Distance
import numpy as np
import os
import cv2


# initialize the known distance from the camera to the object, which
# in this case is 24 inches
KNOWN_DISTANCE = 24.0


# initialize the known object width, which in this case, the piece of
# paper is 12 inches wide
KNOWN_WIDTH = 11.0


camera = cv2.VideoCapture("rtsp://admin:Digitalab_123@192.168.0.21")

detector = ObjectDetection()
detector.setModelTypeAsYOLOv3()
detector.setModelPath(os.path.join(os.getcwd(), "../ml-data-set/yolo.h5"))
detector.loadModel()

firstImage = ""

while True:
    ret, frame = camera.read()
    cacheImagePath = "../cache/cache.jpg"
    cv2.imwrite(cacheImagePath, cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
    detected_copy, output_objects_array = detector.detectObjectsFromImage(input_image=cacheImagePath, input_type='file',
                                                                          output_type='array',
                                                                          minimum_percentage_probability=30)
    if len(output_objects_array) > 0:
        if(firstImage ==""):
            firstImage = frame
            marker = Distance.find_marker(firstImage)
            focalLength = (marker[1][0] * KNOWN_DISTANCE) / KNOWN_WIDTH

        else:


            marker = Distance.find_marker(detected_copy)
            inches = Distance.distance_to_camera(KNOWN_WIDTH, focalLength, marker[1][0])

            box = np.int0(cv2.boxPoints(marker))
            cv2.drawContours(detected_copy, [box], -1, (0, 255, 0), 2)
            cv2.putText(detected_copy, "%.2fft" % (inches / 12),
                        (detected_copy.shape[1] - 200, detected_copy.shape[0] - 20), cv2.FONT_HERSHEY_SIMPLEX,
                        2.0, (0, 255, 0), 3)
            cv2.imshow("image", detected_copy)


    key = cv2.waitKey(1) & 0xFF
    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break

# # Release video
camera.release()
cv2.destroyAllWindows()
