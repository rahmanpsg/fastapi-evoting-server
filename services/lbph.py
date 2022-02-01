import base64
import os
from sys import flags
import cv2
import numpy as np


class LBPH():
    def __init__(self):
        # # self.model = cv2.face_EigenFaceRecognizer.create()
        # # self.model = cv2.face_FisherFaceRecognizer.create()
        self.model = cv2.face_LBPHFaceRecognizer.create()

        try:
            self.model.read("assets/lbph_model.yml")
        except:
            self.training_model()

    def training_model(self):
        faces, labels = self.prepare_data('assets/training/')
        if len(faces) == 0:
            return

        self.model.train(faces, np.array(labels))
        self.model.save(filename="assets/lbph_model.yml")

    def prepare_data(self, data_path):
        imgPaths = [os.path.join(data_path, f) for f in os.listdir(
            data_path) if os.path.join(data_path, f).split('.')[-1] == 'jpg']
        labels = []
        faces = []

        for imgPath in imgPaths:
            imgTraining = cv2.imread(imgPath)
            face = self.face_detection(imgTraining)

            label = int(os.path.split(imgPath)[-1].split('.')[0])

            if face[0] is not None:
                faces.append(face)
                labels.append(label)

        print('Training Done')
        print('Total Wajah {}'.format(len(np.unique(labels))))
        return faces, labels

    def face_detection(self, image, return_img_gray=True):
        image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        haar_classifier = cv2.CascadeClassifier(
            'assets/haarcascade_frontalface_default.xml')
        # haar_classifier = cv2.CascadeClassifier(
        #     'assets/lbpcascade_frontalface.xml')
        faces = haar_classifier.detectMultiScale(
            image_gray, scaleFactor=1.3, minNeighbors=5, minSize=(30, 30), flags=cv2.CASCADE_SCALE_IMAGE)

        if len(faces) == 0:
            return None, None

        (x, y, w, h) = faces[0]

        if return_img_gray:
            return image_gray[y:y+w, x:x+h]
        else:
            return image[y:y+w, x:x+h]

    def predict_image(self, img):
        try:
            # img = cv2.flip(test_image.copy(), 1)

            # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            # haar_classifier = cv2.CascadeClassifier(
            #     'assets/haarcascade_frontalface_default.xml')

            # faces = haar_classifier.detectMultiScale(
            #     gray, scaleFactor=1.2, minNeighbors=5)

            # for (x, y, w, h) in faces:
            #     label, confidence = self.model.predict(gray[y:y+w, x:x+h])

            #     print(label, confidence)

            face = self.face_detection(img)

            if face[0] is None:
                return {'detect': None}

            label, confidence = self.model.predict(face)
            print(label, confidence)
            if confidence <= 50:
                return {'detect': True, 'label': label}
            else:
                return {'detect': False}
        except:
            return {'detect': None}

    def cv2_base64(self, image):
        base64_str = cv2.imencode('.jpg', image)[1].tostring()
        base64_str = base64.b64encode(base64_str)
        return base64_str

    def base64_cv2(self, base64_string):
        encoded_data = base64_string.split(',')[1]
        nparr = np.fromstring(base64.b64decode(str(encoded_data)), np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_ANYCOLOR)
        return img
