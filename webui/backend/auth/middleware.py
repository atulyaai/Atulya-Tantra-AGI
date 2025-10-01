"""
FastAPI Authentication Middleware and Dependencies
"""
from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
import logging

from .auth_system import auth_system, User, UserRole, Permission

logger = logging.getLogger(__name__)

# Security scheme
security = HTTPBearer()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> User:
    """Get current authenticated user from JWT token"""
    token = credentials.credentials
    payload = auth_system.verify_token(token)
    
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    username = payload.get("sub")
    if username is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user = auth_system.get_user_by_username(username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    
    return user

async def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    """Get current active user"""
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

def require_role(required_role: UserRole):
    """Dependency factory to require specific role"""
    async def role_checker(current_user: User = Depends(get_current_active_user)) -> User:
        if current_user.role != required_role and current_user.role != UserRole.ADMIN:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Operation requires {required_role.value} role"
            )
        return current_user
    return role_checker

def require_permission(required_permission: Permission):
    """Dependency factory to require specific permission"""
    async def permission_checker(current_user: User = Depends(get_current_active_user)) -> User:
        if not auth_system.has_permission(current_user, required_permission):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Operation requires {required_permission.value} permission"
            )
        return current_user
    return permission_checker

# Role-specific dependencies
require_admin = require_role(UserRole.ADMIN)
require_developer = require_role(UserRole.DEVELOPER)
require_user = require_role(UserRole.USER)

# Permission-specific dependencies
require_manage_users = require_permission(Permission.MANAGE_USERS)
require_manage_system = require_permission(Permission.MANAGE_SYSTEM)
require_view_logs = require_permission(Permission.VIEW_LOGS)
require_configure_system = require_permission(Permission.CONFIGURE_SYSTEM)
require_view_metrics = require_permission(Permission.VIEW_METRICS)
require_debug_system = require_permission(Permission.DEBUG_SYSTEM)
require_manage_models = require_permission(Permission.MANAGE_MODELS)
require_chat_access = require_permission(Permission.CHAT_ACCESS)
require_view_history = require_permission(Permission.VIEW_HISTORY)