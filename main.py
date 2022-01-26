from random import randint
import cv2
import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from config.db import engine, Base
from routes.index import authRoute, userRoute, kandidatRoute, pemilihRoute, daftarVoteRoute, voteRoute, totalRoute
from services.lbph import LBPH

import models
Base.metadata.create_all(bind=engine)

app = FastAPI(title="E-Voting REST API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080", "http://192.168.43.239:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/', tags=['Index'])
async def index():
    return "E-Voting REST API"

app.include_router(authRoute)
app.include_router(userRoute)
app.include_router(kandidatRoute)
app.include_router(pemilihRoute)
app.include_router(daftarVoteRoute)
app.include_router(voteRoute)
app.include_router(totalRoute)

# lbph = LBPH()


# @app.websocket("/ws")
# async def websocket_endpoint(websocket: WebSocket):
#     await websocket.accept()
#     try:
#         while True:
#             data = await websocket.receive_text()
#             img = lbph.base64_cv2(data)
#             imgPredict = lbph.predict_image(img)
#             # if imgPredict['detect'] is not None:
#             #     name = randint(1, 1000)
#             #     cv2.imwrite(f"{name}.jpg", img)
#             await websocket.send_json(imgPredict)
#     except WebSocketDisconnect:
#         pass


if __name__ == '__main__':
    import logging
    import sys

    logging.basicConfig(level=logging.DEBUG,
                        stream=sys.stdout)

    uvicorn.run("main:app", host='192.168.43.239',
                port=4000, reload=True, debug=False)
