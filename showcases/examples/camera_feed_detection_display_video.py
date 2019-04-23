# # from com.ml.objects.Detection import VideoObjectDetection
# # import os
# import cv2
#
#
# # execution_path = os.getcwd()
#
# camera = cv2.VideoCapture(0)
#
# # detector = VideoObjectDetection()
# # detector.setModelTypeAsYOLOv3()
# # detector.setModelPath(os.path.join(execution_path , "../ml-data-set/yolo.h5"))
# # detector.loadModel()
#
#
# while True:
#     ret, frame = camera.read()
#
#     # detections = detector.detectObjectsFromImage(input_image=frame,
#     #                                              minimum_percentage_probability=30,output_type='image')
#     #
#     # print(detections)
#
#     # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2YUYV)
#     cv2.imshow("frame", frame)
#
#     key = cv2.waitKey(1) & 0xFF
#     # if the `q` key was pressed, break from the loop
#     if key == ord("q"):
#         break
#
#
# # # Release video
# camera.release()
# cv2.destroyAllWindows()
#
#
