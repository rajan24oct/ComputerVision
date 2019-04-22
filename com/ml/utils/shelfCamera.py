import numpy as np
import cv2
import sys
from imutils.object_detection import non_max_suppression

# from Tkinter import *

ENTER_keycode = 13
ESC_keycode = 27

line_thickness = 3

shelf_color = (255, 0, 0)
shelf_area_color = (0, 255, 0)

shelf_text = "With the left mouse button, click 4 times on the image to put the corners of the shelf" \
             "\n\nPress the ENTER key when done to continue\nPress the ESC key to exit the program"
shelf_area_text = "With the left mouse button, click 4 times on the image to put the corners of the shelf area" \
                  "\n\nPress the ENTER key when done to continue\nPress the ESC key to exit the program"
detect_track_text = "The detection and tracking will now start.\nPress the ENTER or the ESC key to exit the program"


class ShelfCamera:
    ## Class Init Function
    def __init__(self, window_name="Shelf Camera", video=None):
        self.video = video
        self.window_name = window_name

        self.drawing = False
        self.shelf_corner_index = 0
        self.shelf_area_corner_index = 0

        self.shelf = np.array([[0, 0],
                               [0, 0],
                               [0, 0],
                               [0, 0]], dtype=np.int32).reshape(-1, 1, 2)

        self.shelf_area = np.array([[0, 0],
                                    [0, 0],
                                    [0, 0],
                                    [0, 0]], dtype=np.int32).reshape(-1, 1, 2)

        cv2.namedWindow(self.window_name)

        # Get the first frame
        ret, self.first_frame = self.video.read()

        # Drawing Shelf Line

        # Make a copy of the First Frame
        self.draw_frame = self.first_frame.copy()
        self.copy_frame = self.draw_frame.copy()

        cv2.imshow(self.window_name, self.draw_frame)

        """
        # Pop-up window 1
        window = Tk()
        window.title("Shelf Drawing Instructions")

        Label(window, text=shelf_text).pack(padx=10, pady=10)
        Button(window, text="OK", command=lambda: window.destroy()).pack(padx=10, pady=10)
        window.mainloop()
        """

        # Set Mouse Callback for Drawing the Shelf Line
        cv2.setMouseCallback(self.window_name, self.draw_shelf)

        # Show image and wait for user to draw Shelf Line and Press the ESC key
        while True:
            cv2.imshow(self.window_name, self.copy_frame)
            key = cv2.waitKey(1) & 0xFF
            if key == ENTER_keycode and not self.drawing:
                break
            elif key == ESC_keycode:
                sys.exit()

        cv2.polylines(self.draw_frame, [self.shelf], True, shelf_color, line_thickness)

        # Drawing Shelf Area

        # Make a copy of the Shelf Frame
        self.copy_frame = self.draw_frame.copy()
        cv2.imshow(self.window_name, self.draw_frame)

        """
        # Pop-up window 2
        window = Tk()
        window.title("Shelf Area Drawing Instructions")

        Label(window, text=shelf_area_text).pack(padx=10, pady=10)
        Button(window, text="OK", command=lambda: window.destroy()).pack(padx=10, pady=10)
        window.mainloop()
        """

        # Set Mouse Callback for Drawing the Shelf Area
        cv2.setMouseCallback(self.window_name, self.draw_shelf_area)

        # Show image and wait for user to draw Shelf Area and Press the ESC key
        while True:
            cv2.imshow(self.window_name, self.copy_frame)
            key = cv2.waitKey(1) & 0xFF
            if key == ENTER_keycode and not self.drawing:
                break
            elif key == ESC_keycode:
                sys.exit()

        cv2.polylines(self.draw_frame, [self.shelf_area], True, shelf_area_color, line_thickness)

        # Remove mouse callback by giving an anonymous function that does nothing
        cv2.setMouseCallback(self.window_name, lambda event, x, y, flags, param: event)

        # Setting up People Detector
        self.hog = cv2.HOGDescriptor()
        self.hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

        """
        # Pop-up window 3
        window = Tk()
        window.title("Detection and Tracking Instructions")

        Label(window, text=detect_track_text).pack(padx=10, pady=10)
        Button(window, text="OK", command=lambda: window.destroy()).pack(padx=10, pady=10)
        window.mainloop()
        """

        # Running Detection and Tracking loop
        self.detect_and_track_people()

    ## Detect and Track People Function
    def detect_and_track_people(self):
        while True:
            try:
                ok, frame = self.video.read()
                if not ok:
                    break
                self.draw_frame = frame.copy()

                cv2.polylines(self.draw_frame, [self.shelf], True, shelf_color, line_thickness)
                cv2.polylines(self.draw_frame, [self.shelf_area], True, shelf_area_color, line_thickness)

                cv2.imshow(self.window_name, self.draw_frame)

                key = cv2.waitKey(10) & 0xFF
                if key == ENTER_keycode or key == ESC_keycode and not self.drawing:
                    sys.exit()
            except:
                break

    ## Draw Shelf Line Function
    def draw_shelf(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.drawing = True
            if self.shelf_corner_index == 0:
                self.copy_frame = self.draw_frame.copy()
            self.shelf[self.shelf_corner_index:, 0] = [x, y]
            self.shelf_corner_index += 1
            cv2.polylines(self.copy_frame, [self.shelf], True, shelf_color, line_thickness)
        if event == cv2.EVENT_LBUTTONUP:
            if self.shelf_corner_index == 4:
                self.copy_frame = self.draw_frame.copy()
                cv2.polylines(self.copy_frame, [self.shelf], True, shelf_color, line_thickness)
                self.shelf_corner_index = 0
                self.drawing = False

    ## Draw Shelf Area Function
    def draw_shelf_area(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.drawing = True
            if self.shelf_area_corner_index == 0:
                self.copy_frame = self.draw_frame.copy()
            self.shelf_area[self.shelf_area_corner_index:, 0] = [x, y]
            self.shelf_area_corner_index += 1
            cv2.polylines(self.copy_frame, [self.shelf_area], True, shelf_area_color, line_thickness)
        if event == cv2.EVENT_LBUTTONUP:
            if self.shelf_area_corner_index == 4:
                self.copy_frame = self.draw_frame.copy()
                cv2.polylines(self.copy_frame, [self.shelf_area], True, shelf_area_color, line_thickness)
                self.shelf_area_corner_index = 0
                self.drawing = False

    ## Class Destructor Function
    def __del__(self):
        self.video.release()