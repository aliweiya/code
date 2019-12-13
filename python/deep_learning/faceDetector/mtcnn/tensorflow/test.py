import cv2
import tensorflow as tf

from model import PNet, RNet, ONet

def test_camera():
    video_capture = cv2.VideoCapture(0)
    pnet = PNet()
    rnet = RNet()
    onet = ONet()
    while True:
        ret, frame = video_capture.read()
        if ret:
            result = pnet.detect(frame)
            print(result)

def test_img():
    pnet = PNet()
    rnet = RNet()
    onet = ONet()
    img = cv2.imread('C:\\Users\\lenovo\\Desktop\\0_Parade_Parade_0_693.jpg')
    boxes = pnet.detect(img)

    boxes = rnet.detect(img, boxes)
    boxes = onet.detect(img, boxes)

if __name__ == '__main__':
    test_img()
    # test_camera()