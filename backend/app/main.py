from fastapi import FastAPI
from .api import cases

app = FastAPI(title="SocialTrace Case Engine")
app.include_router(cases.router, prefix="/cases")

@app.get("/")
def root():
    return {"status": "backend running"}
