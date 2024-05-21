from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

security = HTTPBasic()

def verify_token(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = "attorney"
    correct_password = "123qweasd"
    user = credentials.username
    password = credentials.password
    if user != correct_username or password != correct_password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return user
