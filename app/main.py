from fastapi import FastAPI
from app.routers import auth, user, chat, upload


app = FastAPI()

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(chat.router)
app.include_router(upload.router)
