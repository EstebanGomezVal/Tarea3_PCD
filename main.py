import os
from fastapi import FastAPI, HTTPException, Depends, Security, status
from fastapi.security import APIKeyHeader
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from dotenv import load_dotenv
from typing import Optional, List, Any

import models
from database import engine, SessionLocal

# ----------------------------------------------------------------------
# Configuración
# ----------------------------------------------------------------------

load_dotenv()
API_KEY = os.getenv("API_KEY")

app = FastAPI(title="Users API", version="1.0.0")

models.Base.metadata.create_all(bind=engine)

# ----------------------------------------------------------------------
# Dependencias
# ----------------------------------------------------------------------

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=True)

async def get_api_key(api_key: str = Security(api_key_header)) -> str:
    if API_KEY and api_key == API_KEY:
        return api_key
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Credenciales no válidas. Acceso denegado.")

# ----------------------------------------------------------------------
# Esquemas Pydantic
# ----------------------------------------------------------------------

class UserCreate(BaseModel):
    user_name: str
    user_email: EmailStr
    age: Optional[int] = None
    recommendations: List[str] = Field(default_factory=list) 
    ZIP: Optional[str] = None

class UserUpdate(BaseModel):
    user_name: Optional[str] = None
    user_email: Optional[EmailStr] = None
    age: Optional[int] = None
    recommendations: Optional[List[Any]] = None
    ZIP: Optional[str] = None

class UserRead(BaseModel):
    user_id: int 
    user_name: str
    user_email: EmailStr
    age: Optional[int] = None
    recommendations: List[Any]
    ZIP: Optional[str] = None

    class Config:
        orm_mode = True 

# ----------------------------------------------------------------------
# Endpoints (Rutas de la API)
# ----------------------------------------------------------------------

@app.get("/")
def root():
    return {"message": "Users API up. See /docs"}

@app.get(
    "/api/v1/users/{user_id}", 
    response_model=UserRead, 
    tags=["users"]
)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
    return user

@app.post(
    "/api/v1/users/", 
    response_model=UserRead, 
    tags=["users"], 
    status_code=status.HTTP_201_CREATED
)
def create_user(
    user: UserCreate, 
    db: Session = Depends(get_db), 
    api_key: str = Depends(get_api_key)
):
    user_model = models.User(**user.model_dump())
    
    try:
        db.add(user_model)
        db.commit()
        db.refresh(user_model)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, 
            detail="El correo electrónico ya está registrado."
        )

    return user_model

@app.put(
    "/api/v1/users/{user_id}", 
    response_model=UserRead,
    tags=["users"]
)
def update_user(
    user_id: int, 
    user: UserUpdate, 
    db: Session = Depends(get_db), 
    api_key: str = Depends(get_api_key)
):
    user_model = db.query(models.User).filter(models.User.user_id == user_id).first()
    if user_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"ID {user_id} : No existe")

    update_data = user.model_dump(exclude_unset=True) 
    for key, value in update_data.items():
        setattr(user_model, key, value)
    
    try:
        db.add(user_model)
        db.commit()
        db.refresh(user_model)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, 
            detail="El nuevo correo electrónico ya está registrado por otro usuario."
        )

    return user_model

@app.delete(
    "/api/v1/users/{user_id}", 
    tags=["users"],
    status_code=status.HTTP_200_OK
)
def delete_user(
    user_id: int, 
    db: Session = Depends(get_db), 
    api_key: str = Depends(get_api_key)
):
    user_model = db.query(models.User).filter(models.User.user_id == user_id).first()
    if user_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"ID {user_id} : No existe")

    db.delete(user_model)
    db.commit()
    return {"deleted_id": user_id, "message": "Usuario eliminado correctamente"}