from sqlalchemy.orm import Session
from sqlalchemy import or_
from ..models.post import Post as PostModel
from ..schemas.post import PostCreate
from typing import Optional
from fastapi import HTTPException

def create_post(db: Session, post: PostCreate, author_id: int):
    db_post = PostModel(**post.dict(), author_id=author_id)
    if db_post.title == post.title:
        raise HTTPException(status_code=400, detail="Post already exists")

    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

def get_posts(db: Session, skip: int = 0, limit: int = 10, search: Optional[str] = None, author_id:int = 1):
    query = db.query(PostModel).filter(PostModel.author_id == author_id)
    if search:
        query = query.filter(or_(PostModel.title.ilike(f"%{search}%"), PostModel.content.ilike(f"%{search}%")))
    return query.offset(skip).limit(limit).all()

def get_post(db: Session, post_id: int, author_id: int):
    return db.query(PostModel).filter(PostModel.id == post_id, PostModel.author_id == author_id).first()

def update_post(db: Session, post_id: int, author_id:int, post: PostCreate):
    db_post = db.query(PostModel).filter(PostModel.id == post_id, PostModel.author_id == author_id).first()
    if db_post:
        for key, value in post.dict().items():
            setattr(db_post, key, value)
        db.commit()
        db.refresh(db_post)
    return db_post

def delete_post(db: Session, post_id: int, author_id: int):
    db_post = db.query(PostModel).filter(PostModel.id == post_id, PostModel.author_id == author_id).first()
    if db_post:
        db.delete(db_post)
        db.commit()
    return db_post
