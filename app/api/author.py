from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse

from typing import List

from .. import crud
from ..schemas.author import Author, AuthorCreate, AuthorUpdate
from ..db.database import get_db

router = APIRouter()

@router.post("/", response_model=Author)
def create_author(author: AuthorCreate, db: Session = Depends(get_db)):
    return crud.author.create_author(db=db, author=author)

@router.get("/", response_model=List[Author])
def read_authors(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    authors = crud.author.get_authors(db, skip=skip, limit=limit)
    return authors

@router.get("/{author_id}", response_model=Author)
def read_author(author_id: int, db: Session = Depends(get_db)):
    db_author = crud.author.get_author(db, author_id=author_id)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return db_author

@router.patch("/{author_id}", response_model=Author)
def update_author(author_id: int, author: AuthorUpdate, db: Session = Depends(get_db)):
    db_author = crud.author.update_author(db=db, author_id=author_id, author=author)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return db_author

@router.delete("/{author_id}", response_model=Author)
def delete_author(author_id: int, db: Session = Depends(get_db)):
    db_author = crud.author.delete_author(db=db, author_id=author_id)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    
    return JSONResponse(status_code=204, content={"message": "Successfully deleted author"})
