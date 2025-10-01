"""
Chat Routes
User interface for interacting with the AGI system
"""
from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import logging
import uuid
from datetime import datetime

from auth.auth_system import User
from auth.middleware import get_current_active_user, require_chat_access, require_view_history
from services.main_engine import MainEngine

logger = logging.getLogger(__name__)

def get_agi_engine():
    """Get the global AGI engine instance"""
    import main
    return main.agi_engine

router = APIRouter(prefix="/chat", tags=["chat"])

# Request/Response models
class ChatMessage(BaseModel):
    id: str
    user_id: str
    message: str
    response: str
    timestamp: datetime
    session_id: str
    metadata: Optional[Dict[str, Any]] = None

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None
    context: Optional[Dict[str, Any]] = None

class ChatResponse(BaseModel):
    id: str
    message: str
    response: str
    session_id: str
    timestamp: datetime
    processing_time_ms: float
    metadata: Dict[str, Any]

class ChatSession(BaseModel):
    id: str
    user_id: str
    title: str
    created_at: datetime
    last_message_at: datetime
    message_count: int

# In-memory storage for chat history (in production, use proper database)
chat_history: Dict[str, List[ChatMessage]] = {}
chat_sessions: Dict[str, ChatSession] = {}

@router.post("/message", response_model=ChatResponse)
async def send_message(
    request: ChatRequest,
    current_user: User = Depends(require_chat_access)
):
    """Send a message to the AGI system"""
    try:
        start_time = datetime.now()
        
        # Generate session ID if not provided
        session_id = request.session_id or str(uuid.uuid4())
        
        # Create or update session
        if session_id not in chat_sessions:
            chat_sessions[session_id] = ChatSession(
                id=session_id,
                user_id=current_user.id,
                title=request.message[:50] + "..." if len(request.message) > 50 else request.message,
                created_at=datetime.now(),
                last_message_at=datetime.now(),
                message_count=0
            )
        
        session = chat_sessions[session_id]
        session.last_message_at = datetime.now()
        session.message_count += 1
        
        # Process message through AGI engine
        agi_engine = get_agi_engine()
        if agi_engine:
            try:
                # Use cognitive system to process the message
                agi_response = agi_engine.cognitive_system.process_input(request.message)
                response_text = agi_response.get("response", "I understand your message and I'm processing it.")
            except Exception as e:
                logger.error(f"Error processing message through AGI: {e}")
                response_text = "I'm experiencing some technical difficulties. Please try again."
        else:
            response_text = "AGI system is currently unavailable. Please try again later."
        
        # Calculate processing time
        processing_time = (datetime.now() - start_time).total_seconds() * 1000
        
        # Create chat message
        message_id = str(uuid.uuid4())
        chat_message = ChatMessage(
            id=message_id,
            user_id=current_user.id,
            message=request.message,
            response=response_text,
            timestamp=datetime.now(),
            session_id=session_id,
            metadata=request.context or {}
        )
        
        # Store in history
        if current_user.id not in chat_history:
            chat_history[current_user.id] = []
        chat_history[current_user.id].append(chat_message)
        
        # Prepare response
        response = ChatResponse(
            id=message_id,
            message=request.message,
            response=response_text,
            session_id=session_id,
            timestamp=chat_message.timestamp,
            processing_time_ms=processing_time,
            metadata={
                "user_role": current_user.role.value,
                "session_message_count": session.message_count,
                "agi_status": "available" if agi_engine else "unavailable"
            }
        )
        
        logger.info(f"Message processed for user {current_user.username} in {processing_time:.2f}ms")
        return response
        
    except Exception as e:
        logger.error(f"Error processing chat message: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process message: {str(e)}"
        )

@router.get("/history", response_model=List[ChatMessage])
async def get_chat_history(
    session_id: Optional[str] = None,
    limit: int = 50,
    current_user: User = Depends(require_view_history)
):
    """Get chat history for the current user"""
    try:
        user_messages = chat_history.get(current_user.id, [])
        
        # Filter by session if specified
        if session_id:
            user_messages = [msg for msg in user_messages if msg.session_id == session_id]
        
        # Sort by timestamp (newest first) and limit
        user_messages.sort(key=lambda x: x.timestamp, reverse=True)
        return user_messages[:limit]
        
    except Exception as e:
        logger.error(f"Error getting chat history: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get chat history: {str(e)}"
        )

@router.get("/sessions", response_model=List[ChatSession])
async def get_chat_sessions(current_user: User = Depends(require_view_history)):
    """Get chat sessions for the current user"""
    try:
        user_sessions = [
            session for session in chat_sessions.values()
            if session.user_id == current_user.id
        ]
        
        # Sort by last message time (newest first)
        user_sessions.sort(key=lambda x: x.last_message_at, reverse=True)
        return user_sessions
        
    except Exception as e:
        logger.error(f"Error getting chat sessions: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get chat sessions: {str(e)}"
        )

@router.delete("/history")
async def clear_chat_history(
    session_id: Optional[str] = None,
    current_user: User = Depends(require_view_history)
):
    """Clear chat history for the current user"""
    try:
        if current_user.id in chat_history:
            if session_id:
                # Clear specific session
                chat_history[current_user.id] = [
                    msg for msg in chat_history[current_user.id]
                    if msg.session_id != session_id
                ]
                # Remove session
                if session_id in chat_sessions:
                    del chat_sessions[session_id]
                message = f"Chat history for session {session_id} cleared"
            else:
                # Clear all history
                del chat_history[current_user.id]
                # Remove all user sessions
                user_session_ids = [
                    sid for sid, session in chat_sessions.items()
                    if session.user_id == current_user.id
                ]
                for sid in user_session_ids:
                    del chat_sessions[sid]
                message = "All chat history cleared"
        else:
            message = "No chat history found"
        
        logger.info(f"Chat history cleared for user {current_user.username}")
        return {"message": message}
        
    except Exception as e:
        logger.error(f"Error clearing chat history: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to clear chat history: {str(e)}"
        )

@router.get("/session/{session_id}", response_model=ChatSession)
async def get_chat_session(
    session_id: str,
    current_user: User = Depends(require_view_history)
):
    """Get specific chat session"""
    try:
        session = chat_sessions.get(session_id)
        
        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Chat session not found"
            )
        
        if session.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied to this chat session"
            )
        
        return session
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting chat session: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get chat session: {str(e)}"
        )

@router.put("/session/{session_id}/title")
async def update_session_title(
    session_id: str,
    title: str,
    current_user: User = Depends(require_view_history)
):
    """Update chat session title"""
    try:
        session = chat_sessions.get(session_id)
        
        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Chat session not found"
            )
        
        if session.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied to this chat session"
            )
        
        session.title = title
        logger.info(f"Session {session_id} title updated by user {current_user.username}")
        
        return {"message": "Session title updated", "title": title}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating session title: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update session title: {str(e)}"
        )

@router.get("/stats")
async def get_chat_stats(current_user: User = Depends(require_view_history)):
    """Get chat statistics for the current user"""
    try:
        user_messages = chat_history.get(current_user.id, [])
        user_sessions = [
            session for session in chat_sessions.values()
            if session.user_id == current_user.id
        ]
        
        stats = {
            "total_messages": len(user_messages),
            "total_sessions": len(user_sessions),
            "avg_messages_per_session": len(user_messages) / len(user_sessions) if user_sessions else 0,
            "first_message": min(msg.timestamp for msg in user_messages) if user_messages else None,
            "last_message": max(msg.timestamp for msg in user_messages) if user_messages else None,
            "most_active_day": None  # Could be calculated from message timestamps
        }
        
        return stats
        
    except Exception as e:
        logger.error(f"Error getting chat stats: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get chat stats: {str(e)}"
        )