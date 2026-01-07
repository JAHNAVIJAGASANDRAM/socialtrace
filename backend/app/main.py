from fastapi import FastAPI
from .api import cases, analysis

app = FastAPI(title="SocialTrace Case Engine")
app.include_router(cases.router, prefix="/cases")
app.include_router(analysis.router, prefix="/analysis")

@app.get("/")
def root():
    return {"status": "backend running"}
