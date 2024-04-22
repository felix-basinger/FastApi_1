from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()


class Task(BaseModel):
    task_id: int
    header: str
    description: str
    is_completed: bool


task_1 = Task(task_id=1, header="Task 1", description="Finish writing the program", is_completed=True)
task_2 = Task(task_id=2, header="Task 2", description="Add a new page to the site", is_completed=False)
task_3 = Task(task_id=3, header="Task 3", description="Update website", is_completed=True)

tasks = [task_1, task_2, task_3]


@app.get("/tasks/")
async def tasks_all():
    logger.info("Список задач успешно получен.")
    return {"tasks": tasks}


@app.get("/tasks/{task_id}")
async def read_task(task_id: int):
    task = [task for task in tasks if task.task_id == task_id]
    logger.info(f"Задача получена {task}")
    return task


@app.post("/tasks/")
async def create_task(task: Task):
    tasks.append(task)
    logger.info("Задача успешно добавлена.")
    return task


@app.put("/tasks/{task_id}")
async def change_task(task_id: int, task: Task):
    for i in range(len(tasks)):
        if tasks[i].task_id == task_id:
            tasks[i] = task
    logger.info(f"Изменена задача {task_id}")
    return task


@app.delete("/tasks/{task_id}")
async def delete_task(task_id: int):
    for i in range(len(tasks)):
        if tasks[i].task_id == task_id:
            logger.info(f"Удалена задача {task_id}")
            return {"item_id": tasks.pop(i)}
    logger.info(f"Ошибка удаления задачи {task_id}")
    return HTTPException(status_code=404, detail="Task not found")
