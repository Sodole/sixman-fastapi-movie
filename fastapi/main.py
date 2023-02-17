from fastapi import FastAPI
import movieinfo
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/ya")
def yahoo():
  return movieinfo.yahoo()