from fastapi import FastAPI
from sqlalchemy.orm import Session
from .db import database
from .api import author, post

# Create the FastAPI app
app = FastAPI()

# Include routers
app.include_router(author.router, prefix="/authors", tags=["authors"])
app.include_router(post.router, prefix="/posts", tags=["posts"])

# Database setup
@app.on_event("startup")
def on_startup():
    database.Base.metadata.create_all(bind=database.engine)

@app.on_event("shutdown")
def on_shutdown():
    database.SessionLocal().close()

# Root endpoint for basic testing
@app.get("/")
def read_root():
    return {"message": "Welcome to the Faciliter Blogging Platform!"}
