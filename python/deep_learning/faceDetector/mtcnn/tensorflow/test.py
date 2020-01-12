import cv2
import tensorflow as tf

from model import PNet, RNet, ONet, draw

def test_camera():
    video_capture = cv2.VideoCapture(0)
    pnet = PNet()
    rnet = RNet()
    onet = ONet()

    frame_counter = 0
    boxes, landmarks = None, None

    while True:
        ret, frame = video_capture.read()
        if ret:
            if frame_counter % 10 == 0:
                boxes = pnet.detect(frame)
                if len(boxes) > 0:
                    boxes = rnet.detect(frame, boxes)
                    if len(boxes) > 0:
                        boxes, landmarks = onet.detect(frame, boxes)
                    else:
                        boxes, landmarks = None, None

        if boxes is not None:
            draw(frame, boxes, landmarks)
        cv2.imshow('image', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        frame_counter += 1

def test_img():
    pnet = PNet()
    rnet = RNet()
    onet = ONet()
    img = cv2.imread('C:\\Users\\lenovo\\Desktop\\0_Parade_Parade_0_693.jpg')
    boxes = pnet.detect(img)

    boxes = rnet.detect(img, boxes)
    boxes, landmarks = onet.detect(img, boxes)
    draw(img, boxes, landmarks)
    cv2.imshow('image', img)
    cv2.waitKey()

def export_to_pb():
    pnet = PNet()
    rnet = RNet()
    onet = ONet()

    pnet.export_to_pb()
    rnet.export_to_pb()
    onet.export_to_pb()

if __name__ == '__main__':
    # test_img()
    test_camera()
    # export_to_pb()