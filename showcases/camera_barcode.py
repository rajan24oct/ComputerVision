from com.ml.utils.barcode import Barcode
import cv2
import time
import imutils


camera = cv2.VideoCapture(0)
time.sleep(2.0)

while True:
    ret, frame = camera.read()
 #   frame = imutils.resize(frame, width=400)
    bc = Barcode(image=frame)
    barcodes = bc.decode()

    # loop over the detected barcodes
    for barcode in barcodes:
        # extract the bounding box location of the barcode and draw
        # the bounding box surrounding the barcode on the image
        (x, y, w, h) = barcode.rect
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

        # the barcode data is a bytes object so if we want to draw it
        # on our output image we need to convert it to a string first
        barcodeData = barcode.data.decode("utf-8")
        barcodeType = barcode.type

        # draw the barcode data and barcode type on the image
        text = "{} ({})".format(barcodeData, barcodeType)
        cv2.putText(frame, text, (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

        # # if the barcode text is currently not in our CSV file, write
        # # the timestamp + barcode to disk and update the set
        # if barcodeData not in found:
        #     csv.write("{},{}\n".format(datetime.datetime.now(),
        #                                barcodeData))
        #     csv.flush()
        #     found.add(barcodeData)

    cv2.imshow("Barcode Scanner", frame)
    key = cv2.waitKey(1) & 0xFF
    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break
#
# csv.close()
cv2.destroyAllWindows()
camera.release()
