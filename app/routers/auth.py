from dependencies import JWT_SECRET
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends, HTTPException, status, APIRouter
from models import user_pyd, User
import jwt

# Define Router
router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


async def authenticate_user(username: str, password: str):
    """Authenticate User"""
    user = await User.get(username=username)
    if not user:
        return False
    if not user.verify_password(password):
        return False
    return user


@router.post('/login')
async def generate_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """Login user and return an access token"""
    user = await authenticate_user(form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid username or password'
        )

    user_obj = await user_pyd.from_tortoise_orm(user)
    token = jwt.encode(user_obj.dict(), JWT_SECRET)
    return {'access_token': token, 'token_type': 'Bearer'}
