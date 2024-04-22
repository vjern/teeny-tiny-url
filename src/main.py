from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def liveness():
    return "teeny-tiny-url v0"
