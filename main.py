from fastapi import FastAPI

app = FastAPI()

@app.get('/PTM')
async def get_all_tasks():
    return {"message": "tasklist"}

@app.post("/PTM/{create_task}")
async def create_task(create_task: str):
    tasklist = []
    tasklist.append(create_task)
    return tasklist

@app.put("/PTM/task_id")
async def update_task(tasklist: str, query: str):






