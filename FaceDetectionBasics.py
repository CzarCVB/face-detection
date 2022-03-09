import cv2
import mediapipe as mp
import time


class FaceDetector():
    def __init__(self, minDetecConf = 0.5):
        self.mpFaceDetection = mp.solutions.face_detection
        self.mpDraw = mp.solutions.drawing_utils
        self.faceDetection = self.mpFaceDetection.FaceDetection(0.3)

    def findFaces(self, img, draw=True):

        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.faceDetection.process(imgRGB)
        bbList = []

        if self.results.detections:
            for id, detection in enumerate(self.results.detections):
                # mpDraw.draw_detection(img, detection
                bboxe = detection.location_data.relative_bounding_box
                ih, iw, ic = img.shape
                bbox = int(bboxe.xmin * iw), int(bboxe.ymin * ih), \
                       int(bboxe.width * iw), int(bboxe.height * ih)
                bbList.append([id, bbox, detection.score[0]])
                if draw:
                    img = self.fancyDraw(img, bbox)
                    cv2.putText(img, f'{int(detection.score[0] * 100)}%', (bbox[0], bbox[1] - 20),
                                cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 255), 2)

        return img, bbList

    def fancyDraw(self, img, bbox, l=30, t=10, rt=1):
        x, y, w, h = bbox
        x1, y1 = x+w, y+h
        cv2.rectangle(img, bbox, (255, 0, 255), rt)

        #top left
        cv2.line(img, (x, y), (x+l, y), (255,0,255), t)
        cv2.line(img, (x, y), (x, y+l), (255, 0, 255), t)

        #top right
        cv2.line(img, (x1, y), (x1 - l, y), (255, 0, 255), t)
        cv2.line(img, (x1, y), (x1, y + l), (255, 0, 255), t)

        #bottom left
        cv2.line(img, (x, y1), (x+l, y1), (255,0,255), t)
        cv2.line(img, (x, y1), (x, y1-l), (255, 0, 255), t)

        #bottom right
        cv2.line(img, (x1, y1), (x1 - l, y1), (255, 0, 255), t)
        cv2.line(img, (x1, y1), (x1, y1 - l), (255, 0, 255), t)

        return img

def main():
    cap = cv2.VideoCapture(1)
    pTime = 0
    detector = FaceDetector(minDetecConf=0.3)
    while True:
        success, img = cap.read()
        img = cv2.resize(img, (1280, 720))
        img, bbList = detector.findFaces(img)
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(img, f'FPS: {int(fps)}', (10, 50), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 0), 2)
        cv2.imshow("Face Detection", img)
        cv2.waitKey(1)


if __name__ == "__main__":
    main()