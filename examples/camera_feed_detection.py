from com.ml.objects.Detection import VideoObjectDetection
import os
import cv2


execution_path = os.getcwd()

camera = cv2.VideoCapture(0)

detector = VideoObjectDetection()
detector.setModelTypeAsYOLOv3()
detector.setModelPath(os.path.join(execution_path , "../ml-data-set/yolo.h5"))
detector.loadModel()

video_path = detector.detectObjectsFromVideo(camera_input=camera,
                                output_file_path="../test-data/output/camera_detected_video"
                                , frames_per_second=20, log_progress=True, minimum_percentage_probability=30)
print(video_path)