from typing import List

import jwt
from dependencies import ALLOWED_ROLES, JWT_SECRET, OAUTH2_SCHEME, Status
from fastapi import APIRouter, Depends, HTTPException, status
from models import Comment, User, comment_pyd, commentin_pyd

# Define router
router = APIRouter(
    prefix="/comments",
    tags=["comments"],
    dependencies=[Depends(OAUTH2_SCHEME)]
)


@router.get("/", response_model=List[comment_pyd])
async def get_comments():
    """Return all comments"""
    return await comment_pyd.from_queryset(Comment.all())


@router.post('/', response_model=comment_pyd, status_code=201)
async def create_comment(text: str, token: str = Depends(OAUTH2_SCHEME)):
    """Create comment"""
    payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
    user = await User.get(id=payload.get('id'))
    comment_obj = Comment(
        comment_text=text,
        likes=0,
        user_id=user.id)
    await comment_obj.save()
    return await comment_pyd.from_tortoise_orm(comment_obj)


@router.put('/{comment_id}', response_model=comment_pyd)
async def update_comment(comment_id: int, comment: commentin_pyd):
    """Update existing comment"""
    await Comment.filter(id=comment_id).update(**comment.dict(exclude_unset=True))
    return await comment_pyd.from_queryset_single(Comment.get(id=comment_id))


@router.delete('/{comment_id}', response_model=Status)
async def delete_comment(comment_id: int, token: str = Depends(OAUTH2_SCHEME)):
    """Delete comment by ID. Enabled only for Admins"""
    payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
    if payload.get("roles") in ALLOWED_ROLES:
        deleted_count = await Comment.filter(id=comment_id).delete()
        if not deleted_count:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Comment {comment_id} was not found"
            )
        return Status(detail=f"Deleted comment {comment_id}")
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Operation not permitted"
        )
