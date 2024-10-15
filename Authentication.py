from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
import jwt
from passlib.context import CryptContext
import bcrypt
from datetime import datetime, timedelta


SECRET_KEY = "hello-from-escape-team" # must be secret value (enviromental variable)
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

fake_users_db = {
    "user1": {
        "username": "user1",
        "password": bcrypt.hashpw("password1".encode('utf-8'), bcrypt.gensalt()),
        "disabled": False,
    }
}

def authenticate_user(username: str, password: str):
    user = fake_users_db.get(username)
    if not user or not pwd_context.verify(password, user["password"]):
        return False
    return user

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
        token_data = {"username": username}
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    return token_data