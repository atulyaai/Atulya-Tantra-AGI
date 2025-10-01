"""
Atulya Tantra AGI - Main Backend Application
===========================================

This is the main backend application for the Atulya Tantra AGI system.
Built with FastAPI for high-performance async operations.

Author: Atulya AI Team
Version: 0.1.0
License: MIT
"""

import asyncio
import logging
import time
from contextlib import asynccontextmanager
from typing import Dict, List, Optional, Any

import uvicorn
from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

# Import AGI systems
from ..config.global_config import CONFIG
from ..systems.main_engine import MainEngine
from ..systems.cognitive_system import CognitiveSystem
from ..systems.evolution_system import EvolutionSystem
from ..systems.repair_system import RepairSystem

# Import authentication and routing
from .auth.auth_manager import AuthManager
from .routes import auth_routes, admin_routes, developer_routes, chat_routes

# Global AGI engine instance
agi_engine: Optional[MainEngine] = None
auth_manager: Optional[AuthManager] = None

# Pydantic models for API
class ChatRequest(BaseModel):
    message: str = Field(..., description="User message")
    context: Optional[Dict[str, Any]] = Field(None, description="Additional context")
    model_preference: Optional[str] = Field(None, description="Preferred AI model")
    temperature: Optional[float] = Field(0.7, ge=0.0, le=2.0, description="Response creativity")

class ChatResponse(BaseModel):
    response: str = Field(..., description="AGI response")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Response confidence")
    model_used: str = Field(..., description="Model that generated response")
    reasoning: Optional[str] = Field(None, description="Reasoning process")
    timestamp: float = Field(..., description="Response timestamp")
    intelligence_level: float = Field(..., description="Current intelligence level")

class MemoryRequest(BaseModel):
    memory_type: str = Field(..., description="Type of memory (short_term, long_term, episodic)")
    key: str = Field(..., description="Memory key")
    data: Dict[str, Any] = Field(..., description="Memory data")

class ReasoningRequest(BaseModel):
    reasoning_type: str = Field(..., description="Type of reasoning (logical, causal, analogical)")
    query: str = Field(..., description="Query to reason about")
    context: Optional[Dict[str, Any]] = Field(None, description="Reasoning context")

class LearningRequest(BaseModel):
    experience: Dict[str, Any] = Field(..., description="Experience to learn from")

class SystemStatus(BaseModel):
    status: str = Field(..., description="System status")
    uptime: float = Field(..., description="System uptime in seconds")
    total_requests: int = Field(..., description="Total requests processed")
    successful_requests: int = Field(..., description="Successful requests")
    failed_requests: int = Field(..., description="Failed requests")
    average_response_time: float = Field(..., description="Average response time")
    intelligence_level: float = Field(..., description="Current intelligence level")
    active_models: List[str] = Field(..., description="Active AI models")
    memory_usage: Dict[str, Any] = Field(..., description="Memory usage statistics")
    evolution_metrics: Dict[str, Any] = Field(..., description="Evolution metrics")

# WebSocket connection manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

# Application lifespan management
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application startup and shutdown"""
    global agi_engine, auth_manager
    
    # Startup
    logging.info("Starting Atulya Tantra AGI Backend...")
    
    try:
        # Initialize AGI engine
        agi_engine = MainEngine()
        await agi_engine.initialize()
        
        # Initialize authentication
        auth_manager = AuthManager()
        await auth_manager.initialize()
        
        logging.info("AGI Backend started successfully")
        
    except Exception as e:
        logging.error(f"Failed to start AGI Backend: {e}")
        raise
    
    yield
    
    # Shutdown
    logging.info("Shutting down Atulya Tantra AGI Backend...")
    
    if agi_engine:
        await agi_engine.shutdown()
    
    if auth_manager:
        await auth_manager.shutdown()
    
    logging.info("AGI Backend shutdown complete")

# Create FastAPI application
app = FastAPI(
    title="Atulya Tantra AGI Backend",
    description="Advanced AGI system with cognitive, evolution, and repair capabilities",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=CONFIG["cors"]["allowed_origins"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(GZipMiddleware, minimum_size=1000)

# Include routers
app.include_router(auth_routes.router, prefix="/api/v1/auth", tags=["authentication"])
app.include_router(admin_routes.router, prefix="/api/v1/admin", tags=["admin"])
app.include_router(developer_routes.router, prefix="/api/v1/dev", tags=["developer"])
app.include_router(chat_routes.router, prefix="/api/v1/chat", tags=["chat"])

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with system information"""
    return {
        "name": "Atulya Tantra AGI Backend",
        "version": "0.1.0",
        "description": "Advanced AGI system with cognitive, evolution, and repair capabilities",
        "status": "operational" if agi_engine else "initializing",
        "capabilities": [
            "Natural Language Processing",
            "Cognitive Reasoning",
            "Self-Evolution",
            "Self-Repair",
            "Memory Management",
            "Multi-Model Integration",
            "Real-time Learning"
        ],
        "endpoints": {
            "docs": "/docs",
            "health": "/health",
            "chat": "/api/v1/chat",
            "websocket": "/api/v1/chat/ws",
            "status": "/api/v1/system/status"
        }
    }

# Health check endpoint
@app.get("/health")
async def health_check():
    """Comprehensive health check"""
    try:
        if not agi_engine:
            raise HTTPException(status_code=503, detail="AGI engine not initialized")
        
        # Check all system components
        cognitive_health = await agi_engine.cognitive_system.health_check()
        evolution_health = await agi_engine.evolution_system.health_check()
        repair_health = await agi_engine.repair_system.health_check()
        model_health = await agi_engine.check_model_health()
        
        return {
            "status": "healthy",
            "timestamp": time.time(),
            "uptime": time.time() - agi_engine.start_time,
            "components": {
                "cognitive_system": cognitive_health,
                "evolution_system": evolution_health,
                "repair_system": repair_health,
                "model_integration": model_health
            }
        }
    except Exception as e:
        logging.error(f"Health check failed: {e}")
        raise HTTPException(status_code=503, detail=f"Service unhealthy: {str(e)}")

# Chat endpoints
@app.post("/api/v1/chat", response_model=ChatResponse)
async def chat(request: ChatRequest, background_tasks: BackgroundTasks):
    """Main chat endpoint for AGI interaction"""
    try:
        if not agi_engine:
            raise HTTPException(status_code=503, detail="AGI engine not available")
        
        # Process the message
        input_data = {
            "message": request.message,
            "context": request.context or {},
            "timestamp": time.time(),
            "user_id": "api_user"  # In production, get from auth
        }
        
        response = await agi_engine.process_input(input_data)
        
        # Add background learning task
        background_tasks.add_task(
            agi_engine.cognitive_system.learn_from_experience,
            {
                "input": input_data,
                "output": response,
                "success": True
            }
        )
        
        return ChatResponse(
            response=response.get("content", "I'm processing your request..."),
            confidence=response.get("confidence", 0.5),
            model_used=response.get("model_used", "unknown"),
            reasoning=response.get("reasoning"),
            timestamp=response.get("timestamp", time.time()),
            intelligence_level=response.get("intelligence_level", 1.0)
        )
        
    except Exception as e:
        logging.error(f"Chat processing failed: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to process message: {str(e)}")

@app.websocket("/api/v1/chat/ws")
async def websocket_chat(websocket: WebSocket):
    """WebSocket endpoint for real-time chat"""
    await manager.connect(websocket)
    try:
        while True:
            # Receive message
            data = await websocket.receive_text()
            
            # Process with AGI
            input_data = {
                "message": data,
                "context": {"connection_type": "websocket"},
                "timestamp": time.time(),
                "user_id": "ws_user"
            }
            
            response = await agi_engine.process_input(input_data)
            
            # Send response
            await manager.send_personal_message(
                response.get("content", "Processing..."),
                websocket
            )
            
    except WebSocketDisconnect:
        manager.disconnect(websocket)

# Memory endpoints
@app.post("/api/v1/memory/store")
async def store_memory(request: MemoryRequest):
    """Store data in AGI memory"""
    try:
        await agi_engine.cognitive_system.store_memory(
            request.memory_type,
            request.key,
            request.data
        )
        return {"status": "success", "message": "Memory stored successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to store memory: {str(e)}")

@app.get("/api/v1/memory/retrieve/{memory_type}/{key}")
async def retrieve_memory(memory_type: str, key: str):
    """Retrieve data from AGI memory"""
    try:
        memory = await agi_engine.cognitive_system.retrieve_memory(memory_type, key)
        return {"memory": memory}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve memory: {str(e)}")

@app.get("/api/v1/memory/stats")
async def memory_stats():
    """Get memory system statistics"""
    try:
        stats = await agi_engine.cognitive_system.get_memory_stats()
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get memory stats: {str(e)}")

# Reasoning endpoints
@app.post("/api/v1/reasoning/analyze")
async def analyze_reasoning(request: ReasoningRequest):
    """Perform reasoning analysis"""
    try:
        result = await agi_engine.cognitive_system.reason(
            request.reasoning_type,
            request.query,
            request.context or {}
        )
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Reasoning failed: {str(e)}")

# Learning endpoints
@app.post("/api/v1/learning/experience")
async def learn_from_experience(request: LearningRequest):
    """Learn from new experience"""
    try:
        await agi_engine.cognitive_system.learn_from_experience(request.experience)
        return {"status": "success", "message": "Learning completed"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Learning failed: {str(e)}")

@app.get("/api/v1/learning/stats")
async def learning_stats():
    """Get learning system statistics"""
    try:
        stats = await agi_engine.cognitive_system.get_learning_stats()
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get learning stats: {str(e)}")

# Evolution endpoints
@app.get("/api/v1/evolution/status")
async def evolution_status():
    """Get evolution system status"""
    try:
        status = await agi_engine.evolution_system.get_status()
        return status
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get evolution status: {str(e)}")

@app.post("/api/v1/evolution/trigger")
async def trigger_evolution():
    """Manually trigger evolution process"""
    try:
        result = await agi_engine.evolution_system.evolve()
        return {"status": "success", "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Evolution failed: {str(e)}")

# System monitoring endpoints
@app.get("/api/v1/system/status", response_model=SystemStatus)
async def system_status():
    """Get comprehensive system status"""
    try:
        metrics = agi_engine.get_metrics()
        memory_stats = await agi_engine.cognitive_system.get_memory_stats()
        evolution_metrics = await agi_engine.evolution_system.get_metrics()
        
        return SystemStatus(
            status="operational",
            uptime=time.time() - agi_engine.start_time,
            total_requests=metrics.total_requests,
            successful_requests=metrics.successful_requests,
            failed_requests=metrics.failed_requests,
            average_response_time=metrics.average_response_time,
            intelligence_level=metrics.intelligence_level,
            active_models=["ollama", "langraph", "custom"],
            memory_usage=memory_stats,
            evolution_metrics=evolution_metrics
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get system status: {str(e)}")

@app.get("/api/v1/system/metrics")
async def system_metrics():
    """Get detailed system metrics"""
    try:
        return {
            "agi_metrics": agi_engine.get_metrics(),
            "cognitive_metrics": await agi_engine.cognitive_system.get_metrics(),
            "evolution_metrics": await agi_engine.evolution_system.get_metrics(),
            "repair_metrics": await agi_engine.repair_system.get_metrics(),
            "timestamp": time.time()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get metrics: {str(e)}")

# Admin endpoints
@app.post("/api/v1/admin/shutdown")
async def admin_shutdown():
    """Gracefully shutdown the system"""
    try:
        await agi_engine.shutdown()
        return {"status": "success", "message": "System shutdown initiated"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Shutdown failed: {str(e)}")

@app.post("/api/v1/admin/restart")
async def admin_restart():
    """Restart the AGI engine"""
    try:
        await agi_engine.shutdown()
        await agi_engine.initialize()
        return {"status": "success", "message": "System restarted"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Restart failed: {str(e)}")

# Exception handlers
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler"""
    logging.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
            "type": type(exc).__name__,
            "timestamp": time.time()
        }
    )

if __name__ == "__main__":
    # Setup logging
    logging.basicConfig(
        level=getattr(logging, CONFIG["logging"]["level"].upper()),
        format=CONFIG["logging"]["format"]
    )
    
    # Run the application
    uvicorn.run(
        "main:app",
        host=CONFIG["server"]["host"],
        port=CONFIG["server"]["port"],
        reload=CONFIG["server"]["reload"],
        workers=1 if CONFIG["server"]["reload"] else CONFIG["performance"]["max_workers"],
        log_level=CONFIG["server"]["log_level"]
    )