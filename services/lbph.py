import base64
import os
import cv2
import numpy as np


class LBPH():
    def __init__(self):
        self.database = ["Rahman", "Tom", "Clon"]
        faces, labels = self.prepare_data('assets/training/')

        # print(faces)
        # print(labels)

        # self.model = cv2.face_EigenFaceRecognizer.create()
        # self.model = cv2.face_FisherFaceRecognizer.create()
        self.model = cv2.face_LBPHFaceRecognizer.create()

        self.model.train(faces, np.array(labels))
        # self.model.read("assets/lbph_model.yml")
        self.model.save(filename="assets/lbph_model.yml")

    def prepare_data(self, data_path):
        folders = os.listdir(data_path)
        labels = []
        faces = []
        for folder in folders:
            if folder.isdigit():
                label = int(folder)
                training_images_path = data_path + '/' + folder
                for image in os.listdir(training_images_path):
                    if image.split('.')[1] == 'jpg':
                        image_path = training_images_path + '/' + image
                        training_image = cv2.imread(image_path)
                        face = self.face_detection(
                            training_image)
                        faces.append(face)
                        labels.append(label)

        print('Training Done')
        return faces, labels

    def face_detection(self, image):
        image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        haar_classifier = cv2.CascadeClassifier(
            'assets/haarcascade_frontalface_default.xml')
        # haar_classifier = cv2.CascadeClassifier(
        #     'assets/lbpcascade_frontalface.xml')
        faces = haar_classifier.detectMultiScale(
            image_gray, scaleFactor=1.2, minNeighbors=5)

        if len(faces) == 0:
            return None, None

        (x, y, w, h) = faces[0]
        return image_gray[y:y+w, x:x+h]

    def predict_image(self, test_image):
        try:
            img = test_image.copy()
            face = self.face_detection(img)

            if face is None:
                return {'detect': None}

            label, confidence = self.model.predict(face)
            print(label, confidence)
            if confidence > 90:
                return {'detect': label, 'nama': self.database[label-1]}
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
