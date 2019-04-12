from pyzbar import pyzbar
import cv2


class Barcode:

    def __init__(self, image):
        self.image = image

    def decode(self):
        return  pyzbar.decode(self.image)
