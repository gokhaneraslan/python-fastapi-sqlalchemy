from signal import raise_signal
from fastapi import Depends, FastAPI, status, HTTPException
from .models import schemas, model
from .auth import hashing, token
from .services.database import SessionLocal, engine
from sqlalchemy.orm import Session
from typing import List


model.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    
    try:
        
        yield db
        
    finally:
        
        db.close()


@app.post("/blog/login", tags=["authentication"])
def login(request: schemas.Login,  db: Session = Depends(get_db)):
    user = db.query(model.User).filter(model.User.email == request.username).first()
    
    if not user:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= 'username not existed')
    
    password = hashing.Hash.verify(user.password, request.password)
    
    if not password:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= 'password not existed')
    
    access_token = token.create_access_token(data={"sub": user.email})
    
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/blog", status_code=status.HTTP_201_CREATED, tags=['Blogs'])
def create(request: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = model.Blog(title= request.title, body= request.body, user_id= 1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    
    return new_blog

@app.get("/blog", response_model=List[schemas.ShowBlog], tags=['Blogs'])
def get_post(db: Session = Depends(get_db)):
    blogs = db.query(model.Blog).all()
    
    return blogs

@app.get('/blog/{id}', status_code=status.HTTP_200_OK, response_model=schemas.ShowBlog, tags=['Blogs'])
def show(id, db: Session = Depends(get_db)):
    blog = db.query(model.Blog).filter(model.Blog.id == id).first()
    
    if not blog:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f'Blog with id {id} not available')
    
    return blog


@app.delete("/blog/{id}", status_code= status.HTTP_204_NO_CONTENT, tags=['Blogs'])
def delete_post(id, db: Session = Depends(get_db)):
    blog = db.query(model.Blog).filter(model.Blog.id == id).delete(synchronize_session=False)
    db.commit()
    
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Blog {id} not available')
    
    return { "detail": f"Blog with {id} is deleted." }

@app.put('/blog/{id}', status_code= status.HTTP_202_ACCEPTED, tags=['Blogs'])
def update_post(id, request: schemas.Blog, db: Session = Depends(get_db)):
    blog = db.query(model.Blog).filter(model.Blog.id == id)
    
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Blog {id} not available')
    
    blog.update({"title": request.title, "body": request.body})
    db.commit()
    return "Updated"




@app.post("/user", response_model=schemas.ShowUser, tags=['users'])
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    new_user = model.User(name=request.name, email=request.email, password= hashing.Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user

@app.get("/user/{username}", response_model= schemas.ShowUser, tags=['users'])
def get_user(username, db: Session = Depends(get_db)):
    user = db.query(model.User).filter(model.User.name == username).first()
    
    if not user:
        
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f"User with {username} not available")
    
    return user