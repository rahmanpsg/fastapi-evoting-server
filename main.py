import os
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from config.db import engine, Base
from routes.index import authRoute, userRoute, kandidatRoute, pemilihRoute, daftarVoteRoute, voteRoute, totalRoute, cetakRoute
from app import app
import routes.websocket
from dotenv import load_dotenv

load_dotenv()

Base.metadata.create_all(bind=engine)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost",
                   "http://localhost:8080", os.getenv('CLIENT_URL')],
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

    uvicorn.run("main:app", host=os.getenv('BASE_URL'),
                port=4000, reload=True, debug=False)
