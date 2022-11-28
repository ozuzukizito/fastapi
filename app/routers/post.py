from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional
from .. import models, schemas, oauth2
from sqlalchemy import func
from ..database import get_db


router = APIRouter(
    prefix= "/posts",
    tags= ['POSTS']
)

@router.get("/", response_model=List[schemas.Post_Vote])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), 
limit:int = 16, skip:int = 0, search: Optional[str] = ""):

    print()
#posts= db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    posts= db.query(models.Post, func.count(models.Vote.post_id).label("num_of_votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id
        ).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    print()
    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_posts(post: schemas.Post, db: Session = Depends(get_db), current_user: int = 
Depends(oauth2.get_current_user)):
    
    new_post = models.Post (owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@router.get("/{id}", response_model=schemas.Post_Vote)
def get_post(id: int, db: Session = Depends (get_db), current_user: int = 
Depends(oauth2.get_current_user)):
    print(current_user.email)
    post = db.query(models.Post, func.count(models.Vote.post_id).label("num_of_votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id
        ).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail= f"user with id: {id} not found")
    
    return post


@router.delete("/{id}", status_code= status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends (get_db), current_user: int = 
Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail= f"user with id: {id} does not exist")
    if post.owner_id !=current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="request not authorised")

    post_query.delete(synchronize_session=False)
    db.commit()
    

@router.put("/{id}", response_model=schemas.PostResponse)
def update_post (id: int, updated_post: schemas.Post, db: Session = Depends (get_db), current_user: int = 
Depends(oauth2.get_current_user)):

    post_query =  db.query(models.Post).filter(models.Post.id == id) 
 
    post = post_query.first() 

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail= f"user with id: {id} does not exist")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="request not authorised")

    post_query.update(updated_post.dict(), synchronize_session=False)

    db.commit()

    return post_query.first()