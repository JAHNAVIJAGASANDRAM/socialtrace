from fastapi import FastAPI

app = FastAPI(title="SocialTrace Case Engine")

@app.get("/")
def root():
    return {"status": "backend running"}
