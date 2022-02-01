import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config.db import engine, Base
from routes.index import authRoute, userRoute, kandidatRoute, pemilihRoute, daftarVoteRoute, voteRoute, totalRoute, cetakRoute
import routes.websocket


Base.metadata.create_all(bind=engine)

app = FastAPI(title="E-Voting REST API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost",
                   "http://localhost:8080", "http://192.168.43.239:8080"],
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
app.include_router(cetakRoute)


if __name__ == '__main__':
    import logging
    import sys

    logging.basicConfig(level=logging.DEBUG,
                        stream=sys.stdout)

    uvicorn.run("main:app", host='192.168.43.239',
                port=4000, reload=True, debug=False)
