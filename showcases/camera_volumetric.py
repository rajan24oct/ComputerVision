from com.ml.utils.dimension import Dimension
from com.ml.objects.Detection import ObjectDetection
import os
import cv2

execution_path = os.getcwd()
#
camera = cv2.VideoCapture("rtsp://admin:Digitalab_123@192.168.0.21")
#camera = cv2.VideoCapture(0)
#
detector = ObjectDetection()
detector.setModelTypeAsYOLOv3()
detector.setModelPath(os.path.join(execution_path, "../ml-data-set/yolo.h5"))
detector.loadModel()

while True:
    ret, frame = camera.read()
    cacheImagePath = "../cache/cache.jpg"
    cv2.imwrite(cacheImagePath, cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
    detected_copy, output_objects_array = detector.detectObjectsFromImage(input_image=cacheImagePath, input_type='file',
                                                                          output_type='array',
                                                                          minimum_percentage_probability=30)
    dm = Dimension(image=detected_copy, width=0.95)
    objArr = dm.getDimension()

    for obj in objArr:
        # show the output image
        cv2.imshow("Image", obj)

    # #detected_copy = cv2.cvtColor(detected_copy, cv2.COLOR_BGR2YUYV)
    # cv2.imshow("frame", detected_copy)

    key = cv2.waitKey(1) & 0xFF
    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break

# # Release video
camera.release()
cv2.destroyAllWindows()




