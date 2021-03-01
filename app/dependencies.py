from fastapi.security import OAuth2PasswordBearer
from models import User
from pydantic import BaseModel

# Shared variables
JWT_SECRET = '391e1f0185495a70caef9d3693ef115a'
OAUTH2_SCHEME = OAuth2PasswordBearer(tokenUrl='/auth/login')
ALLOWED_ROLES = ["admin"]


class Status(BaseModel):
    """BaseModel class to print messages"""
    detail: str
