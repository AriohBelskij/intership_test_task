import uvicorn
from fastapi import FastAPI

from src.task.router import tree_router

app = FastAPI()

app.include_router(tree_router)


@app.get("/")
def hello():
    return "Hello, ty for watching my test task!"


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, host="127.0.0.1", port=8000)
