from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from fastapi.responses import JSONResponse


from .. import crud
from ..schemas.post import Post, PostCreate
from ..db.database import get_db

router = APIRouter()

@router.post("/", response_model=Post)
def create_post_for_author(post: PostCreate, author_id: int, db: Session = Depends(get_db)):
    return crud.post.create_post(db=db, post=post, author_id=author_id)

@router.get("/", response_model=List[Post])
def read_author_posts(skip: int = 0, limit: int = 10, search: Optional[str] = None, author_id: int = 1, db: Session = Depends(get_db)):
    posts = crud.post.get_posts(db, skip=skip, limit=limit, search=search, author_id=author_id)
    return posts

@router.get("/{post_id}", response_model=Post)
def read_author_post(post_id: int, author_id:int, db: Session = Depends(get_db)):
    db_post = crud.post.get_post(db, post_id=post_id, author_id=author_id)
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found for this author")
    return db_post

@router.put("/{post_id}", response_model=Post)
def update_author_post(post_id: int, author_id:int, post: PostCreate, db: Session = Depends(get_db)):
    db_post = crud.post.update_post(db=db, post_id=post_id, post=post, author_id=author_id)
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found for this author")
    return db_post

@router.delete("/{post_id}", response_model=Post)
def delete_author_post(post_id: int, author_id: int, db: Session = Depends(get_db)):
    db_post = crud.post.delete_post(db=db, post_id=post_id, author_id=author_id)
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found for this author")

    return JSONResponse(status_code=204, content={"message": "Successfully deleted post"})
