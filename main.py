from fastapi import FastAPI, Request, status
from models import Base
from database import engine
from routers import auth, todos, admin, users
# from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, RedirectResponse

app = FastAPI()

Base.metadata.create_all(bind=engine)
BASE_DIR = Path(__file__).resolve().parent


# templates = Jinja2Templates(directory="TodoApp_New/templates")
# templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")

# app.mount("/static", StaticFiles(directory="TodoApp_New/static"), name="static")

@app.get("/")
async def root(request: Request):

    try:
        await auth.get_current_user(request)
        return RedirectResponse("/todos/todo-page")

    except Exception:
        return RedirectResponse("/auth/login-page")

# @app.get("/")
# def test(request: Request):
#     # return templates.TemplateResponse("home.html", {"request": request})
#     return RedirectResponse(url="/todos/todo-page", status_code=status.HTTP_302_FOUND)

@app.get("/healthy")
def health_check():
    return {"message": "Healthy"}

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    print("VALIDATION ERROR:", exc.errors())
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors()}
    )

app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)

# Base.metadata.create_all(bind=engine)

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run("main:app", reload=True)

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run("FastAPI_Course.TodoApp_New.main:app", reload=True)
