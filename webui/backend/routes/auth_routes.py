"""
Authentication Routes
"""
from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer
from pydantic import BaseModel
from typing import List, Optional
import logging

from auth.auth_system import auth_system, User, UserRole, Permission
from auth.middleware import (
    get_current_active_user, 
    require_admin,
    require_manage_users
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["authentication"])

# Request/Response models
class LoginRequest(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: User

class UserCreateRequest(BaseModel):
    username: str
    email: str
    password: str
    role: UserRole

class UserUpdateRequest(BaseModel):
    email: Optional[str] = None
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None
    password: Optional[str] = None

class UserResponse(BaseModel):
    user: User
    permissions: List[Permission]

@router.post("/login", response_model=LoginResponse)
async def login(request: LoginRequest):
    """Authenticate user and return tokens"""
    user = auth_system.authenticate_user(request.username, request.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = auth_system.create_access_token(user)
    refresh_token = auth_system.create_refresh_token(user)
    
    logger.info(f"User {user.username} logged in successfully")
    
    return LoginResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        user=user
    )

@router.post("/logout")
async def logout(current_user: User = Depends(get_current_active_user)):
    """Logout user (token invalidation would be handled by client)"""
    logger.info(f"User {current_user.username} logged out")
    return {"message": "Successfully logged out"}

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_active_user)):
    """Get current user information and permissions"""
    permissions = auth_system.get_user_permissions(current_user)
    return UserResponse(user=current_user, permissions=permissions)

@router.get("/users", response_model=List[User])
async def list_users(current_user: User = Depends(require_manage_users)):
    """List all users (admin only)"""
    return auth_system.list_users()

@router.post("/users", response_model=User)
async def create_user(
    request: UserCreateRequest,
    current_user: User = Depends(require_manage_users)
):
    """Create new user (admin only)"""
    try:
        user = auth_system.create_user(
            username=request.username,
            email=request.email,
            password=request.password,
            role=request.role
        )
        logger.info(f"User {user.username} created by {current_user.username}")
        return user
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.put("/users/{username}", response_model=User)
async def update_user(
    username: str,
    request: UserUpdateRequest,
    current_user: User = Depends(require_manage_users)
):
    """Update user (admin only)"""
    updates = request.dict(exclude_unset=True)
    user = auth_system.update_user(username, **updates)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    logger.info(f"User {username} updated by {current_user.username}")
    return user

@router.delete("/users/{username}")
async def delete_user(
    username: str,
    current_user: User = Depends(require_manage_users)
):
    """Delete user (admin only)"""
    if username == current_user.username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete your own account"
        )
    
    success = auth_system.delete_user(username)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    logger.info(f"User {username} deleted by {current_user.username}")
    return {"message": f"User {username} deleted successfully"}

@router.get("/roles")
async def get_roles(current_user: User = Depends(get_current_active_user)):
    """Get available user roles"""
    return {
        "roles": [role.value for role in UserRole],
        "current_role": current_user.role.value
    }

@router.get("/permissions")
async def get_permissions(current_user: User = Depends(get_current_active_user)):
    """Get available permissions and user's permissions"""
    user_permissions = auth_system.get_user_permissions(current_user)
    all_permissions = [perm.value for perm in Permission]
    
    return {
        "all_permissions": all_permissions,
        "user_permissions": [perm.value for perm in user_permissions],
        "role": current_user.role.value
    }