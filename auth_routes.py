from fastapi import APIRouter, status, Depends, Header
from sqlalchemy.orm import Session
from database import SessionLocal
from schemas import SignUpModel, LoginModel
from models import User
from fastapi.exceptions import HTTPException
from werkzeug.security import generate_password_hash, check_password_hash
from fastapi.encoders import jsonable_encoder
import jwt
import datetime
from typing import Optional
from jwt import ExpiredSignatureError, InvalidTokenError
from fastapi import APIRouter, status, Depends, Header
from sqlalchemy.orm import Session
from database import SessionLocal, get_db  # Import get_db from database
from schemas import SignUpModel, LoginModel

auth_router = APIRouter(prefix='/auth', tags=['auth'])

# JWT settings (move these to environment variables in production)
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Define a simple hello endpoint
@auth_router.get("/")
def hello():
    return {"message": "my name is vishal rathore"}

@auth_router.post("/signup", status_code=status.HTTP_201_CREATED)
def signup(user: SignUpModel, db: Session = Depends(get_db)):
    db_email = db.query(User).filter(User.email == user.email).first()
    if db_email is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="User with the email already exists"
        )

    db_username = db.query(User).filter(User.username == user.username).first()
    if db_username is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="User with the username already exists"
        )

    new_user = User(
        username=user.username,
        email=user.email,
        password=generate_password_hash(user.password),
        is_active=user.is_active,
        is_staff=user.is_staff
    )
    
    db.add(new_user)
    db.commit()
    
    return {"message": "User created successfully"} 

def create_access_token(data: dict, expires_delta: Optional[datetime.timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.datetime.now(datetime.timezone.utc) + expires_delta
    else:
        expire = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def create_refresh_token(data: dict):
    expire = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=7)
    to_encode = data.copy()
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@auth_router.post("/login", status_code=200)
def login(user: LoginModel, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    
    if db_user and check_password_hash(db_user.password, user.password):
        access_token = create_access_token(data={"sub": db_user.username})
        refresh_token = create_refresh_token(data={"sub": db_user.username})

        response = {
            "access": access_token,
            "refresh": refresh_token
        }

        return jsonable_encoder(response) 
    
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Invalid Username or Password"
    )
    
@auth_router.get("/refresh")
def refresh_access_token(authorization: str = Header(...)):
    try:
        # Extract token from "Bearer <token>" format
        if not authorization.startswith("Bearer "):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authorization header format"
            )
        
        refresh_token = authorization.replace("Bearer ", "")
        
        # Verify and decode the refresh token
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        
        # Check if token has "sub" (subject) claim
        current_user = payload.get("sub")
        if not current_user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token: missing subject"
            )
        
        # Create new access token
        access_token = create_access_token(data={"sub": current_user})
        return jsonable_encoder({"access": access_token})
        
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token has expired"
        )
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )