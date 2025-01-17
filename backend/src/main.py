from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from controller import stat, alert

app = FastAPI()
app.include_router(alert.router)
app.include_router(stat.router)

app.mount("/", StaticFiles(directory="web/public", html=True), name="web")
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api")
def read_root():
    return {"Hello": "World"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", reload=True)

#while True:
#    dao.add_stat("auto", random.randint(0, 20))
#    time.sleep(60)
