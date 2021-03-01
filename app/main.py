from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from routers import auth, comments, users
from dependencies import Status

# Initialize the app and add endpoints
app = FastAPI()
app.include_router(comments.router)
app.include_router(users.router)
app.include_router(auth.router)


@app.get("/health", tags=["health"])
async def health():
    """Dummy health endpoint with no authentication"""
    return Status(detail="All Systems On!!!")

# Register DB Models with SQLlite
register_tortoise(
    app,
    db_url='sqlite://db.sqlite3',
    modules={'models': ['models']},
    generate_schemas=True,
    add_exception_handlers=True
)
