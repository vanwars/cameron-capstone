import os
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select, text
from sqlalchemy.orm import Session

from . import models, schemas
from .db import Base, engine, get_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Simple bootstrap. Swap for Alembic migrations when the schema grows.
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title="Capstone API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ORIGINS", "http://localhost:5173").split(","),
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
def health(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))
    return {"status": "ok"}


@app.get("/api/items", response_model=list[schemas.ItemRead])
def list_items(db: Session = Depends(get_db)):
    return db.scalars(select(models.Item).order_by(models.Item.id)).all()


@app.post("/api/items", response_model=schemas.ItemRead, status_code=201)
def create_item(payload: schemas.ItemCreate, db: Session = Depends(get_db)):
    item = models.Item(**payload.model_dump())
    db.add(item)
    db.commit()
    return item


@app.delete("/api/items/{item_id}", status_code=204)
def delete_item(item_id: int, db: Session = Depends(get_db)):
    item = db.get(models.Item, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(item)
    db.commit()
