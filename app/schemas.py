from datetime import date, datetime, time
from typing import Optional
from pydantic.types import conint
from pydantic import BaseModel, EmailStr


class Post(BaseModel):
    title: Optional[str]= None
    content: str
    published: bool= True



#class PostBase(BaseModel):
#title: Optional[str]= None
#content: str
#published: bool= True

#class PostCreate(PostBase):
    #pass

#class PostCreate(PostBase):
    #pass


class UserOut(BaseModel):
    email: EmailStr
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

class PostResponse(Post):
    id:int
    created_at: datetime
    owner_id: int
    owner: UserOut
    
    class Config:
        orm_mode = True

class Post_Vote(BaseModel):
    Post: PostResponse
    num_of_votes: int

    class Config:
        orm_mode = True

class CreateUser(BaseModel):
    email: EmailStr 
    password: str


class UserLogin (BaseModel):
    email: EmailStr
    password: str

class Token (BaseModel):
    access_token :str
    token_type: str

class TokenData (BaseModel):
    id: Optional[str] = None

class vote(BaseModel):
    post_id: int
    dir: conint(le=1)

