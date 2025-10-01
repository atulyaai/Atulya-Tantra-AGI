"""
Authentication and Authorization System
Role-based access control for Atulya Tantra AGI
"""
import jwt
import bcrypt
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List
from enum import Enum
from pydantic import BaseModel

logger = logging.getLogger(__name__)

class UserRole(str, Enum):
    """User roles with different access levels"""
    ADMIN = "admin"
    DEVELOPER = "developer"
    USER = "user"

class Permission(str, Enum):
    """System permissions"""
    # Admin permissions
    MANAGE_USERS = "manage_users"
    MANAGE_SYSTEM = "manage_system"
    VIEW_LOGS = "view_logs"
    CONFIGURE_SYSTEM = "configure_system"
    
    # Developer permissions
    VIEW_METRICS = "view_metrics"
    DEBUG_SYSTEM = "debug_system"
    MANAGE_MODELS = "manage_models"
    
    # User permissions
    CHAT_ACCESS = "chat_access"
    VIEW_HISTORY = "view_history"

class User(BaseModel):
    """User model"""
    id: str
    username: str
    email: str
    role: UserRole
    is_active: bool = True
    created_at: datetime
    last_login: Optional[datetime] = None

class AuthSystem:
    """Authentication and authorization system"""
    
    def __init__(self, secret_key: str = "atulya-tantra-secret-key"):
        self.secret_key = secret_key
        self.algorithm = "HS256"
        self.access_token_expire_minutes = 30
        self.refresh_token_expire_days = 7
        
        # Role permissions mapping
        self.role_permissions = {
            UserRole.ADMIN: [
                Permission.MANAGE_USERS,
                Permission.MANAGE_SYSTEM,
                Permission.VIEW_LOGS,
                Permission.CONFIGURE_SYSTEM,
                Permission.VIEW_METRICS,
                Permission.DEBUG_SYSTEM,
                Permission.MANAGE_MODELS,
                Permission.CHAT_ACCESS,
                Permission.VIEW_HISTORY
            ],
            UserRole.DEVELOPER: [
                Permission.VIEW_METRICS,
                Permission.DEBUG_SYSTEM,
                Permission.MANAGE_MODELS,
                Permission.VIEW_LOGS,
                Permission.CHAT_ACCESS,
                Permission.VIEW_HISTORY
            ],
            UserRole.USER: [
                Permission.CHAT_ACCESS,
                Permission.VIEW_HISTORY
            ]
        }
        
        # Mock user database (in production, use proper database)
        self.users_db = {
            "admin": {
                "id": "admin-001",
                "username": "admin",
                "email": "admin@atulya-tantra.ai",
                "password_hash": self._hash_password("admin123"),
                "role": UserRole.ADMIN,
                "is_active": True,
                "created_at": datetime.now()
            },
            "developer": {
                "id": "dev-001",
                "username": "developer",
                "email": "dev@atulya-tantra.ai",
                "password_hash": self._hash_password("dev123"),
                "role": UserRole.DEVELOPER,
                "is_active": True,
                "created_at": datetime.now()
            },
            "user": {
                "id": "user-001",
                "username": "user",
                "email": "user@atulya-tantra.ai",
                "password_hash": self._hash_password("user123"),
                "role": UserRole.USER,
                "is_active": True,
                "created_at": datetime.now()
            }
        }
    
    def _hash_password(self, password: str) -> str:
        """Hash password using bcrypt"""
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def _verify_password(self, password: str, hashed: str) -> bool:
        """Verify password against hash"""
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
    
    def authenticate_user(self, username: str, password: str) -> Optional[User]:
        """Authenticate user with username and password"""
        user_data = self.users_db.get(username)
        if not user_data:
            return None
        
        if not self._verify_password(password, user_data["password_hash"]):
            return None
        
        if not user_data["is_active"]:
            return None
        
        # Update last login
        user_data["last_login"] = datetime.now()
        
        return User(
            id=user_data["id"],
            username=user_data["username"],
            email=user_data["email"],
            role=user_data["role"],
            is_active=user_data["is_active"],
            created_at=user_data["created_at"],
            last_login=user_data["last_login"]
        )
    
    def create_access_token(self, user: User) -> str:
        """Create JWT access token"""
        expire = datetime.utcnow() + timedelta(minutes=self.access_token_expire_minutes)
        to_encode = {
            "sub": user.username,
            "user_id": user.id,
            "role": user.role.value,
            "exp": expire,
            "type": "access"
        }
        return jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
    
    def create_refresh_token(self, user: User) -> str:
        """Create JWT refresh token"""
        expire = datetime.utcnow() + timedelta(days=self.refresh_token_expire_days)
        to_encode = {
            "sub": user.username,
            "user_id": user.id,
            "exp": expire,
            "type": "refresh"
        }
        return jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
    
    def verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Verify and decode JWT token"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except jwt.ExpiredSignatureError:
            logger.warning("Token has expired")
            return None
        except jwt.JWTError:
            logger.warning("Invalid token")
            return None
    
    def get_user_by_username(self, username: str) -> Optional[User]:
        """Get user by username"""
        user_data = self.users_db.get(username)
        if not user_data:
            return None
        
        return User(
            id=user_data["id"],
            username=user_data["username"],
            email=user_data["email"],
            role=user_data["role"],
            is_active=user_data["is_active"],
            created_at=user_data["created_at"],
            last_login=user_data.get("last_login")
        )
    
    def has_permission(self, user: User, permission: Permission) -> bool:
        """Check if user has specific permission"""
        user_permissions = self.role_permissions.get(user.role, [])
        return permission in user_permissions
    
    def require_permission(self, user: User, permission: Permission) -> bool:
        """Require user to have specific permission, raise exception if not"""
        if not self.has_permission(user, permission):
            raise PermissionError(f"User {user.username} does not have permission: {permission}")
        return True
    
    def get_user_permissions(self, user: User) -> List[Permission]:
        """Get all permissions for a user"""
        return self.role_permissions.get(user.role, [])
    
    def list_users(self) -> List[User]:
        """List all users (admin only)"""
        users = []
        for user_data in self.users_db.values():
            users.append(User(
                id=user_data["id"],
                username=user_data["username"],
                email=user_data["email"],
                role=user_data["role"],
                is_active=user_data["is_active"],
                created_at=user_data["created_at"],
                last_login=user_data.get("last_login")
            ))
        return users
    
    def create_user(self, username: str, email: str, password: str, role: UserRole) -> User:
        """Create new user (admin only)"""
        if username in self.users_db:
            raise ValueError(f"User {username} already exists")
        
        user_id = f"{role.value}-{len(self.users_db) + 1:03d}"
        user_data = {
            "id": user_id,
            "username": username,
            "email": email,
            "password_hash": self._hash_password(password),
            "role": role,
            "is_active": True,
            "created_at": datetime.now()
        }
        
        self.users_db[username] = user_data
        
        return User(
            id=user_data["id"],
            username=user_data["username"],
            email=user_data["email"],
            role=user_data["role"],
            is_active=user_data["is_active"],
            created_at=user_data["created_at"]
        )
    
    def update_user(self, username: str, **updates) -> Optional[User]:
        """Update user information (admin only)"""
        if username not in self.users_db:
            return None
        
        user_data = self.users_db[username]
        
        # Update allowed fields
        if "email" in updates:
            user_data["email"] = updates["email"]
        if "role" in updates:
            user_data["role"] = updates["role"]
        if "is_active" in updates:
            user_data["is_active"] = updates["is_active"]
        if "password" in updates:
            user_data["password_hash"] = self._hash_password(updates["password"])
        
        return User(
            id=user_data["id"],
            username=user_data["username"],
            email=user_data["email"],
            role=user_data["role"],
            is_active=user_data["is_active"],
            created_at=user_data["created_at"],
            last_login=user_data.get("last_login")
        )
    
    def delete_user(self, username: str) -> bool:
        """Delete user (admin only)"""
        if username in self.users_db:
            del self.users_db[username]
            return True
        return False

# Global auth system instance
auth_system = AuthSystem()