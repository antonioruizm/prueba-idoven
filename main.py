from datetime import timedelta
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from auth import ACCESS_TOKEN_EXPIRE_MINUTES, authenticate_user, create_access_token, create_user, get_current_user
from database import Base, engine, get_db
from models import User
from schemas import ECGSchema, UserCreate, UserOut
from crud import create_ecg, get_ecg_insights

app = FastAPI()

# Crear las tablas en la base de datos
Base.metadata.create_all(bind=engine)

@app.post("/ecgs/")
def create_ecg_endpoint(ecg: ECGSchema, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return create_ecg(db=db, ecg=ecg)

@app.get("/ecgs/{ecg_id}/insights")
def read_ecg_insights(ecg_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    insights = get_ecg_insights(db=db, ecg_id=ecg_id)
    if insights is None:
        raise HTTPException(status_code=404, detail="ECG not found")
    return insights

# Endpoint para registrar un nuevo usuario
@app.post("/register/", response_model=UserOut)
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return create_user(db=db, user=user)

# Endpoint para obtener un token
@app.post("/token")
def login_for_access_token(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
