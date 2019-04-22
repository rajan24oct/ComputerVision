import cv2
import sys
from com.ml.utils.shelfCamera import ShelfCamera

video_path = "../test-data/input/PrixCameraLat.mov"

capture = cv2.VideoCapture(video_path)

if not capture.isOpened():
    print("Couldn't open video")
    sys.exit()

try:
    ShelfCamera(video=capture)
finally:
    capture.release()
    cv2.destroyAllWindows()