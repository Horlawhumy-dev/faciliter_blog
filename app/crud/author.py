from sqlalchemy.orm import Session
from ..models.author import Author as AuthorModel
from ..schemas.author import AuthorCreate, AuthorUpdate
from fastapi import HTTPException

def create_author(db: Session, author: AuthorCreate):
    db_author = AuthorModel(**author.model_dump())

    if db_author.email == author.email:
        raise HTTPException(status_code=400, detail="Author already exists")
        
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author

def get_authors(db: Session, skip: int = 0, limit: int = 10):
    return db.query(AuthorModel).offset(skip).limit(limit).all()

def get_author(db: Session, author_id: int):
    return db.query(AuthorModel).filter(AuthorModel.id == author_id).first()

def update_author(db: Session, author_id: int, author: AuthorUpdate):
    db_author = db.query(AuthorModel).filter(AuthorModel.id == author_id).first()
    if db_author:
        update_data = author.dict(exclude_unset=True)
        if 'email' in update_data:
            raise HTTPException(status_code=400, detail="Email update is not allowed")
        for key, value in update_data.items():
            setattr(db_author, key, value)
        db.commit()
        db.refresh(db_author)
    return db_author

def delete_author(db: Session, author_id: int):
    db_author = db.query(AuthorModel).filter(AuthorModel.id == author_id).first()
    if db_author:
        db.delete(db_author)
        db.commit()
    return db_author
