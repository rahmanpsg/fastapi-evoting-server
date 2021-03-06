import asyncio
import io
from app import app, lbph
import cv2
from fastapi import Depends, WebSocket, WebSocketDisconnect
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from config.db import get_db
from models.pemilih import Pemilihs
from services.token import create_access_token
from schemas.authentication import Token
import cloudinary.uploader
from PIL import Image


@app.websocket("/faceRecognition/{id_pemilih}")
async def websocket_endpoint(id_pemilih: int,websocket: WebSocket, db: Session = Depends(get_db)):
    await websocket.accept()
    totalDetect = 0
    maxDetect = 5
    currentDetect = None
    try:
        while True:
            progress = (totalDetect/maxDetect) * 100

            if progress > 100:
                return

            data = await websocket.receive_text()
            img = lbph.base64_cv2(data)
            imgBlur = cv2.Laplacian(img, cv2.CV_64F).var()

            response = {'detect': None, 'message': None, 'progress': 0}

            if imgBlur <= 100:
                response['message'] = 'Kamera blur. Gunakan kamera dengan resolusi lebih tinggi'
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

                if currentDetect != id_pemilih:
                    imgPredict['detect'] = False
                    totalDetect = 0
                    response['message'] = 'Data wajah tidak sesuai'
            elif imgPredict['detect'] == False:
                response['message'] = 'Wajah tidak terdaftar'
                totalDetect = 0
            else:
                response['message'] = 'Tidak ada wajah terdeteksi'
                totalDetect = 0

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

            await websocket.send_json(response)
    except WebSocketDisconnect:
        pass


@ app.websocket("/regisFace/{id_pemilih}")
async def websocket_endpoint(websocket: WebSocket, id_pemilih: int, db: Session = Depends(get_db)):
    await websocket.accept()
    try:
        maxImg = 100
        file = 1
        while True:
            progress = (file / maxImg) * 100

            if progress > 100:
                pemilih = db.query(Pemilihs).get(id_pemilih)
                pemilih.face_recognition = True
                db.commit()

                asyncio.create_task(lbph.training_model())
                return

            data = await websocket.receive_text()
            img = lbph.base64_cv2(data)
            imgBlur = cv2.Laplacian(img, cv2.CV_64F).var()

            response = {"detect": None, "message": "Tidak ada wajah terdeteksi",
                        "progress": progress}

            if imgBlur <= 100:
                response['message'] = 'Kamera blur. Gunakan kamera dengan resolusi lebih tinggi'
                await websocket.send_json(response)
                continue

            imgDetect = lbph.face_detection(img, False)

            if imgDetect[0] is not None:
                name = str(id_pemilih) + "." + str(file)

                imgColor = cv2.cvtColor(imgDetect, cv2.COLOR_BGR2RGB)
                image = Image.fromarray(imgColor)

                imgByteArr = image_to_byte_array(image)

                upload = cloudinary.uploader.upload(
                    imgByteArr, public_id=name, folder='training', invalidate=True, **{'async': True})

                print(upload)

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
        pass


def image_to_byte_array(image: Image):
    imgByteArr = io.BytesIO()
    image.save(imgByteArr, format='PNG')
    imgByteArr = imgByteArr.getvalue()
    return imgByteArr
