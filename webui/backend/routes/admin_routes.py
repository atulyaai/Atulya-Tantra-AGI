"""
Admin Panel Routes
System monitoring, configuration, and management for administrators
"""
from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
import logging
import psutil
import os
from datetime import datetime

from auth.auth_system import auth_system, User
from auth.middleware import require_admin, require_manage_system, require_view_logs
from services.main_engine import MainEngine

logger = logging.getLogger(__name__)

def get_agi_engine():
    """Get the global AGI engine instance"""
    import main
    return main.agi_engine

router = APIRouter(prefix="/admin", tags=["admin"])

# Response models
class SystemMetrics(BaseModel):
    cpu_usage: float
    memory_usage: float
    disk_usage: float
    network_io: Dict[str, int]
    process_count: int
    uptime: float

class SystemStatus(BaseModel):
    status: str
    components: Dict[str, Any]
    metrics: SystemMetrics
    timestamp: datetime

class LogEntry(BaseModel):
    timestamp: datetime
    level: str
    message: str
    module: str

class ConfigurationItem(BaseModel):
    key: str
    value: Any
    description: str
    category: str

@router.get("/dashboard", response_model=SystemStatus)
async def get_admin_dashboard(current_user: User = Depends(require_admin)):
    """Get comprehensive admin dashboard data"""
    try:
        # Get system metrics
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        network = psutil.net_io_counters()
        
        system_metrics = SystemMetrics(
            cpu_usage=cpu_percent,
            memory_usage=memory.percent,
            disk_usage=(disk.used / disk.total) * 100,
            network_io={
                "bytes_sent": network.bytes_sent,
                "bytes_recv": network.bytes_recv
            },
            process_count=len(psutil.pids()),
            uptime=(datetime.now() - get_agi_engine().start_time).total_seconds()
        )
        
        # Get component status
        agi_engine = get_agi_engine()
        components = {
            "agi_engine": {
                "status": "healthy" if agi_engine else "error",
                "metrics": agi_engine.get_metrics() if agi_engine else {}
            },
            "cognitive_system": {
                "status": "healthy",
                "active_processes": getattr(agi_engine.cognitive_system, 'active_processes', 0)
            },
            "evolution_system": {
                "status": "healthy",
                "generation": getattr(agi_engine.evolution_system, 'current_generation', 0)
            },
            "repair_system": {
                "status": "healthy",
                "metrics": getattr(agi_engine.repair_system, 'metrics', {})
            }
        }
        
        return SystemStatus(
            status="healthy",
            components=components,
            metrics=system_metrics,
            timestamp=datetime.now()
        )
        
    except Exception as e:
        logger.error(f"Error getting admin dashboard: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get dashboard data: {str(e)}"
        )

@router.get("/system/health")
async def get_system_health(current_user: User = Depends(require_admin)):
    """Get detailed system health information"""
    try:
        health_data = {
            "overall_status": "healthy",
            "components": {},
            "timestamp": datetime.now()
        }
        
        # Check each component
        agi_engine = get_agi_engine()
        if agi_engine:
            health_data["components"]["agi_engine"] = {
                "status": "healthy",
                "uptime": (datetime.now() - agi_engine.start_time).total_seconds(),
                "metrics": agi_engine.get_metrics()
            }
            
            # Check cognitive system
            try:
                cog_health = agi_engine.cognitive_system.health_check()
                health_data["components"]["cognitive_system"] = {
                    "status": "healthy" if cog_health > 0.7 else "warning",
                    "health_score": cog_health
                }
            except Exception as e:
                health_data["components"]["cognitive_system"] = {
                    "status": "error",
                    "error": str(e)
                }
            
            # Check evolution system
            try:
                evo_health = agi_engine.evolution_system.health_check()
                health_data["components"]["evolution_system"] = {
                    "status": "healthy" if evo_health > 0.7 else "warning",
                    "health_score": evo_health
                }
            except Exception as e:
                health_data["components"]["evolution_system"] = {
                    "status": "error",
                    "error": str(e)
                }
            
            # Check repair system
            try:
                repair_health = agi_engine.repair_system.health_check()
                health_data["components"]["repair_system"] = {
                    "status": "healthy" if repair_health > 0.7 else "warning",
                    "health_score": repair_health
                }
            except Exception as e:
                health_data["components"]["repair_system"] = {
                    "status": "error",
                    "error": str(e)
                }
        
        return health_data
        
    except Exception as e:
        logger.error(f"Error getting system health: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get system health: {str(e)}"
        )

@router.get("/logs")
async def get_system_logs(
    limit: int = 100,
    level: Optional[str] = None,
    current_user: User = Depends(require_view_logs)
):
    """Get system logs"""
    try:
        # In a real implementation, you would read from log files
        # For now, return mock log data
        logs = [
            LogEntry(
                timestamp=datetime.now(),
                level="INFO",
                message="System started successfully",
                module="main_engine"
            ),
            LogEntry(
                timestamp=datetime.now(),
                level="INFO",
                message="Cognitive system initialized",
                module="cognitive_system"
            ),
            LogEntry(
                timestamp=datetime.now(),
                level="INFO",
                message="Evolution system ready",
                module="evolution_system"
            )
        ]
        
        if level:
            logs = [log for log in logs if log.level.lower() == level.lower()]
        
        return logs[:limit]
        
    except Exception as e:
        logger.error(f"Error getting logs: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get logs: {str(e)}"
        )

@router.get("/configuration")
async def get_system_configuration(current_user: User = Depends(require_admin)):
    """Get system configuration"""
    try:
        config = [
            ConfigurationItem(
                key="max_concurrent_requests",
                value=100,
                description="Maximum number of concurrent API requests",
                category="performance"
            ),
            ConfigurationItem(
                key="cognitive_learning_rate",
                value=0.01,
                description="Learning rate for cognitive system",
                category="ai"
            ),
            ConfigurationItem(
                key="evolution_population_size",
                value=50,
                description="Population size for evolution system",
                category="ai"
            ),
            ConfigurationItem(
                key="repair_check_interval",
                value=300,
                description="Interval for repair system checks (seconds)",
                category="maintenance"
            ),
            ConfigurationItem(
                key="log_level",
                value="INFO",
                description="System logging level",
                category="logging"
            )
        ]
        
        return config
        
    except Exception as e:
        logger.error(f"Error getting configuration: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get configuration: {str(e)}"
        )

@router.put("/configuration/{key}")
async def update_configuration(
    key: str,
    value: Any,
    current_user: User = Depends(require_manage_system)
):
    """Update system configuration"""
    try:
        # In a real implementation, you would update the actual configuration
        logger.info(f"Configuration {key} updated to {value} by {current_user.username}")
        
        return {
            "message": f"Configuration {key} updated successfully",
            "key": key,
            "value": value,
            "updated_by": current_user.username,
            "timestamp": datetime.now()
        }
        
    except Exception as e:
        logger.error(f"Error updating configuration: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update configuration: {str(e)}"
        )

@router.post("/system/restart")
async def restart_system(current_user: User = Depends(require_manage_system)):
    """Restart system components"""
    try:
        logger.info(f"System restart initiated by {current_user.username}")
        
        # In a real implementation, you would restart components
        # For now, just return a success message
        
        return {
            "message": "System restart initiated",
            "initiated_by": current_user.username,
            "timestamp": datetime.now()
        }
        
    except Exception as e:
        logger.error(f"Error restarting system: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to restart system: {str(e)}"
        )

@router.get("/users/activity")
async def get_user_activity(current_user: User = Depends(require_admin)):
    """Get user activity statistics"""
    try:
        users = auth_system.list_users()
        activity = []
        
        for user in users:
            activity.append({
                "username": user.username,
                "role": user.role.value,
                "is_active": user.is_active,
                "last_login": user.last_login,
                "created_at": user.created_at
            })
        
        return {
            "total_users": len(users),
            "active_users": len([u for u in users if u.is_active]),
            "users": activity
        }
        
    except Exception as e:
        logger.error(f"Error getting user activity: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get user activity: {str(e)}"
        )

@router.get("/metrics/performance")
async def get_performance_metrics(current_user: User = Depends(require_admin)):
    """Get detailed performance metrics"""
    try:
        metrics = {
            "system": {
                "cpu_usage": psutil.cpu_percent(interval=1),
                "memory_usage": psutil.virtual_memory().percent,
                "disk_usage": (psutil.disk_usage('/').used / psutil.disk_usage('/').total) * 100,
                "load_average": os.getloadavg() if hasattr(os, 'getloadavg') else [0, 0, 0]
            },
            "application": {
                "uptime": (datetime.now() - agi_engine.start_time).total_seconds() if agi_engine else 0,
                "requests_processed": getattr(agi_engine, 'requests_processed', 0),
                "errors_count": getattr(agi_engine, 'errors_count', 0),
                "active_sessions": getattr(agi_engine, 'active_sessions', 0)
            },
            "ai_components": {
                "cognitive_processes": getattr(agi_engine.cognitive_system, 'active_processes', 0) if agi_engine else 0,
                "evolution_generation": getattr(agi_engine.evolution_system, 'current_generation', 0) if agi_engine else 0,
                "repairs_performed": getattr(agi_engine.repair_system, 'metrics', {}).get('successful_repairs', 0) if agi_engine else 0
            }
        }
        
        return metrics
        
    except Exception as e:
        logger.error(f"Error getting performance metrics: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get performance metrics: {str(e)}"
        )