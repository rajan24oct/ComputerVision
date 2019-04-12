from com.ml.utils.dimension import Dimension
import cv2

image = cv2.imread("../test-data/input/example_02.png")
print(image)
dm = Dimension(image=image, width=0.95)
objArr = dm.getDimension()

for obj in objArr:
    # show the output image
    cv2.imshow("Image", obj)
    cv2.waitKey(0)