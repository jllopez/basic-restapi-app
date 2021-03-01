from typing import List
import jwt
from dependencies import ALLOWED_ROLES, JWT_SECRET, OAUTH2_SCHEME, Status
from fastapi import APIRouter, Depends, HTTPException, status
from models import User, user_pyd, userin_pyd
from passlib.hash import bcrypt

# Define router
router = APIRouter(
    prefix="/users",
    tags=["users"]
)


@router.post('/', response_model=user_pyd, status_code=201)
async def create_user(user: userin_pyd, token: str = Depends(OAUTH2_SCHEME)):
    """Create user. Enabled only for Admins"""
    payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
    if payload.get("roles") in ALLOWED_ROLES:
        user_obj = User(username=user.username,
                        password_hash=bcrypt.hash(user.password_hash),
                        roles=user.roles)
        await user_obj.save()
        return await user_pyd.from_tortoise_orm(user_obj)
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Operation not permitted"
        )


@router.get('/me', response_model=user_pyd)
async def get_user(token: str = Depends(OAUTH2_SCHEME)):
    """Get current user"""
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
        user = await User.get(id=payload.get('id'))
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid username or password'
        )
    return await user_pyd.from_tortoise_orm(user)


@router.get("/", response_model=List[user_pyd])
async def get_users(token: str = Depends(OAUTH2_SCHEME)):
    """Get all users. Enabled only for Admins"""
    payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
    if payload.get("roles") in ALLOWED_ROLES:
        return await user_pyd.from_queryset(User.all())
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Operation not permitted"
        )


@router.delete('/{user_id}')
async def delete_user(user_id: int, token: str = Depends(OAUTH2_SCHEME)):
    """Delete user by ID. Enabled only for Admins"""
    payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
    if payload.get("roles") in ALLOWED_ROLES:
        deleted_count = await User.filter(id=user_id).delete()
        if not deleted_count:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id {user_id} was not found"

            )
        return Status(detail=f"Deleted user {user_id}")
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Operation not permitted"
        )
