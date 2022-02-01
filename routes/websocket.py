from app import app
import cv2
from fastapi import Depends, WebSocket, WebSocketDisconnect
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from config.db import get_db
from models.pemilih import Pemilihs
from services.lbph import LBPH
from services.token import create_access_token
from schemas.authentication import Token

lbph = LBPH()


@app.websocket("/faceRecognition")
async def websocket_endpoint(websocket: WebSocket, db: Session = Depends(get_db)):
    await websocket.accept()
    totalDetect = 0
    maxDetect = 5
    currentDetect = None
    try:
        while True:
            data = await websocket.receive_text()
            img = lbph.base64_cv2(data)
            imgBlur = cv2.Laplacian(img, cv2.CV_64F).var()

            response = {'detect': None, 'message': None, 'progress': 0}

            if imgBlur <= 100:
                response['message'] = 'Kamera blur'
                await websocket.send_json(response)
                continue

            imgPredict = lbph.predict_image(img)

            if imgPredict['detect'] == True:
                if currentDetect == imgPredict['label']:
                    totalDetect += 1
                else:
                    totalDetect = 0
                currentDetect = imgPredict['label']
                response['message'] = 'Sedang mengenali wajah...'
            elif imgPredict['detect'] == False:
                response['message'] = 'Wajah tidak terdaftar'
                totalDetect = 0
            else:
                response['message'] = 'Tidak ada wajah terdeteksi'
                totalDetect = 0

            progress = (totalDetect/maxDetect) * 100

            response['detect'] = imgPredict['detect']
            response['progress'] = progress

            if progress == 100:
                pemilih = db.query(Pemilihs).get(currentDetect)

                access_token = create_access_token(
                    data={"sub": pemilih.username})
                token = Token(access_token=access_token, token_type='bearer')

                response['token'] = jsonable_encoder(token)
                response['user'] = jsonable_encoder(pemilih)
                response['user']['role'] = 'pemilih'
                # response['id'] = pemilih.id
                # response['username'] = pemilih.username
                # response['nama'] = pemilih.nama

            await websocket.send_json(response)
    except WebSocketDisconnect:
        pass


@ app.websocket("/regisFace/{id_pemilih}")
async def websocket_endpoint(websocket: WebSocket, id_pemilih: int, db: Session = Depends(get_db)):
    await websocket.accept()
    try:
        trainingPath = 'assets/training/'
        maxImg = 30
        file = 1
        while True:
            data = await websocket.receive_text()
            img = lbph.base64_cv2(data)
            imgBlur = cv2.Laplacian(img, cv2.CV_64F).var()

            response = {"detect": None, "message": "Tidak ada wajah terdeteksi",
                        "progress": (file / maxImg) * 100}

            # if imgBlur <= 100:
            #     response['message'] = 'Kamera blur. Gunakan kamera dengan resolusi lebih tinggi'
            #     await websocket.send_json(response)
            #     continue

            imgDetect = lbph.face_detection(img, False)

            if imgDetect[0] is not None:
                name = str(id_pemilih) + "." + str(file) + '.jpg'
                print(name)
                cv2.imwrite(trainingPath + name, imgDetect)
                response['detect'] = True
                file += 1

                if file < 10:
                    response['message'] = "Sedang merekam data wajah..."
                elif file < 20:
                    response['message'] = "Ubah posisi wajah dan ekspresi wajah anda..."
                elif file <= 30:
                    response['message'] = "Sedang merekam data wajah..."

            await websocket.send_json(response)
    except WebSocketDisconnect:
        if file >= 30:
            pemilih = db.query(Pemilihs).get(id_pemilih)

            pemilih.face_recognition = True

            db.commit()

            lbph.training_model()
        # pass
