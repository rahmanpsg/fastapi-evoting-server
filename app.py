from fastapi import FastAPI
from services.lbph import LBPH

app = FastAPI(title="E-Voting REST API")

lbph = LBPH()