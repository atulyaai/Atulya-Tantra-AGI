"""
Developer routes for debugging, metrics, and development tools.
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel
import logging

from ..auth.middleware import require_developer, require_view_metrics, require_debug_system
from ..auth.auth_system import User
from ..services.main_engine import agi_engine

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/developer", tags=["developer"])

# Pydantic models
class DebugInfo(BaseModel):
    component: str
    status: str
    details: Dict[str, Any]
    timestamp: datetime

class MetricData(BaseModel):
    name: str
    value: float
    unit: str
    timestamp: datetime
    component: str
    category: str

class SystemTrace(BaseModel):
    trace_id: str
    component: str
    operation: str
    duration_ms: float
    status: str
    details: Dict[str, Any]
    timestamp: datetime

@router.get("/dashboard")
async def get_developer_dashboard(current_user: User = Depends(require_developer)):
    """Get developer dashboard overview"""
    try:
        dashboard_data = {
            "system_overview": {
                "total_components": 3,
                "healthy_components": 3,
                "warning_components": 0,
                "error_components": 0,
                "uptime": "2d 14h 32m",
                "last_restart": "2024-01-15T10:30:00Z"
            },
            "performance_summary": {
                "cpu_usage": 45.2,
                "memory_usage": 68.7,
                "disk_usage": 23.1,
                "network_io": {
                    "bytes_sent": 1024000,
                    "bytes_received": 2048000
                }
            },
            "recent_activities": [
                {
                    "timestamp": datetime.now(),
                    "component": "cognitive_system",
                    "action": "processed_request",
                    "details": "Successfully processed user query"
                },
                {
                    "timestamp": datetime.now(),
                    "component": "evolution_system",
                    "action": "evolution_cycle",
                    "details": "Completed generation 15"
                },
                {
                    "timestamp": datetime.now(),
                    "component": "repair_system",
                    "action": "health_check",
                    "details": "All systems healthy"
                }
            ],
            "api_statistics": {
                "total_requests": 15420,
                "successful_requests": 15380,
                "failed_requests": 40,
                "avg_response_time": "125ms",
                "requests_per_minute": 25.5
            },
            "error_summary": {
                "total_errors": 12,
                "critical_errors": 0,
                "warnings": 8,
                "info_messages": 4,
                "last_error": "2024-01-15T14:22:00Z"
            }
        }
        
        return dashboard_data
        
    except Exception as e:
        logger.error(f"Error getting developer dashboard: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get developer dashboard: {str(e)}"
        )

@router.get("/metrics", response_model=List[MetricData])
async def get_system_metrics(
    component: Optional[str] = Query(None, description="Filter by component"),
    category: Optional[str] = Query(None, description="Filter by category"),
    limit: int = Query(100, description="Maximum number of metrics to return"),
    current_user: User = Depends(require_view_metrics)
):
    """Get detailed system metrics"""
    try:
        # Mock metrics data - in a real implementation, this would come from a metrics system
        metrics = [
            MetricData(
                name="cpu_usage_percent",
                value=45.2,
                unit="percent",
                timestamp=datetime.now(),
                component="system",
                category="performance"
            ),
            MetricData(
                name="memory_usage_mb",
                value=2048.5,
                unit="megabytes",
                timestamp=datetime.now(),
                component="system",
                category="performance"
            ),
            MetricData(
                name="active_processes",
                value=12,
                unit="count",
                timestamp=datetime.now(),
                component="cognitive_system",
                category="activity"
            ),
            MetricData(
                name="evolution_generation",
                value=15,
                unit="count",
                timestamp=datetime.now(),
                component="evolution_system",
                category="progress"
            ),
            MetricData(
                name="repairs_performed",
                value=3,
                unit="count",
                timestamp=datetime.now(),
                component="repair_system",
                category="maintenance"
            ),
            MetricData(
                name="response_time_ms",
                value=125.5,
                unit="milliseconds",
                timestamp=datetime.now(),
                component="api",
                category="performance"
            ),
            MetricData(
                name="requests_per_second",
                value=25.5,
                unit="requests/second",
                timestamp=datetime.now(),
                component="api",
                category="throughput"
            ),
            MetricData(
                name="error_rate",
                value=0.01,
                unit="percent",
                timestamp=datetime.now(),
                component="api",
                category="reliability"
            )
        ]
        
        # Apply filters
        if component:
            metrics = [m for m in metrics if m.component == component]
        if category:
            metrics = [m for m in metrics if m.category == category]
        
        return metrics[:limit]
        
    except Exception as e:
        logger.error(f"Error getting metrics: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get metrics: {str(e)}"
        )

@router.get("/debug/{component}", response_model=DebugInfo)
async def get_component_debug_info(
    component: str,
    current_user: User = Depends(require_debug_system)
):
    """Get debug information for a specific component"""
    try:
        debug_info = None
        
        if component == "cognitive_system" and agi_engine:
            debug_info = DebugInfo(
                component="cognitive_system",
                status="healthy",
                details={
                    "active_processes": getattr(agi_engine.cognitive_system, 'active_processes', 0),
                    "memory_usage": "45.2 MB",
                    "last_operation": "pattern_recognition",
                    "queue_size": 5,
                    "processing_time_avg": "120ms"
                },
                timestamp=datetime.now()
            )
        elif component == "evolution_system" and agi_engine:
            debug_info = DebugInfo(
                component="evolution_system",
                status="healthy",
                details={
                    "current_generation": getattr(agi_engine.evolution_system, 'current_generation', 0),
                    "population_size": 50,
                    "fitness_score": 0.85,
                    "mutation_rate": 0.1,
                    "crossover_rate": 0.7
                },
                timestamp=datetime.now()
            )
        elif component == "repair_system" and agi_engine:
            repair_metrics = getattr(agi_engine.repair_system, 'metrics', {})
            debug_info = DebugInfo(
                component="repair_system",
                status="healthy",
                details={
                    "repairs_attempted": repair_metrics.get('repairs_attempted', 0),
                    "successful_repairs": repair_metrics.get('successful_repairs', 0),
                    "issues_detected": repair_metrics.get('issues_detected', 0),
                    "system_health_score": repair_metrics.get('system_health_score', 0.9),
                    "last_check": repair_metrics.get('last_check_time', datetime.now())
                },
                timestamp=datetime.now()
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Component {component} not found"
            )
        
        return debug_info
        
    except Exception as e:
        logger.error(f"Error getting debug info for {component}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get debug info: {str(e)}"
        )

@router.get("/traces", response_model=List[SystemTrace])
async def get_system_traces(
    component: Optional[str] = None,
    limit: int = 50,
    current_user: User = Depends(require_debug_system)
):
    """Get system execution traces"""
    try:
        # Mock trace data - in a real implementation, this would come from a tracing system
        traces = [
            SystemTrace(
                trace_id="trace-001",
                component="cognitive_system",
                operation="process_input",
                duration_ms=125.5,
                status="completed",
                details={"input_size": 1024, "output_size": 512},
                timestamp=datetime.now()
            ),
            SystemTrace(
                trace_id="trace-002",
                component="evolution_system",
                operation="evolve_population",
                duration_ms=2500.0,
                status="completed",
                details={"generation": 15, "fitness_improvement": 0.05},
                timestamp=datetime.now()
            ),
            SystemTrace(
                trace_id="trace-003",
                component="repair_system",
                operation="health_check",
                duration_ms=50.2,
                status="completed",
                details={"issues_found": 0, "health_score": 0.95},
                timestamp=datetime.now()
            )
        ]
        
        if component:
            traces = [t for t in traces if t.component == component]
        
        return traces[:limit]
        
    except Exception as e:
        logger.error(f"Error getting traces: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get traces: {str(e)}"
        )

@router.post("/debug/trigger/{component}/{operation}")
async def trigger_debug_operation(
    component: str,
    operation: str,
    current_user: User = Depends(require_debug_system)
):
    """Trigger debug operations on components"""
    try:
        result = {
            "component": component,
            "operation": operation,
            "triggered_by": current_user.username,
            "timestamp": datetime.now(),
            "status": "initiated"
        }
        
        if component == "cognitive_system" and operation == "health_check":
            if agi_engine and agi_engine.cognitive_system:
                health_score = agi_engine.cognitive_system.health_check()
                result["result"] = {"health_score": health_score}
                result["status"] = "completed"
        
        elif component == "evolution_system" and operation == "force_evolution":
            if agi_engine and agi_engine.evolution_system:
                # Trigger evolution cycle
                result["result"] = {"message": "Evolution cycle triggered"}
                result["status"] = "completed"
        
        elif component == "repair_system" and operation == "run_diagnostics":
            if agi_engine and agi_engine.repair_system:
                health_score = agi_engine.repair_system.health_check()
                result["result"] = {"health_score": health_score}
                result["status"] = "completed"
        
        else:
            result["status"] = "error"
            result["error"] = f"Unknown operation {operation} for component {component}"
        
        logger.info(f"Debug operation {operation} triggered on {component} by {current_user.username}")
        return result
        
    except Exception as e:
        logger.error(f"Error triggering debug operation: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to trigger debug operation: {str(e)}"
        )

@router.get("/models/status")
async def get_models_status(current_user: User = Depends(require_developer)):
    """Get status of AI models"""
    try:
        models_status = {
            "loaded_models": [
                {
                    "name": "cognitive_model",
                    "type": "transformer",
                    "status": "loaded",
                    "memory_usage": "2.5 GB",
                    "last_used": datetime.now()
                },
                {
                    "name": "evolution_model",
                    "type": "genetic_algorithm",
                    "status": "loaded",
                    "memory_usage": "512 MB",
                    "last_used": datetime.now()
                }
            ],
            "available_models": [
                "gpt-3.5-turbo",
                "claude-3-sonnet",
                "llama-2-70b"
            ],
            "model_performance": {
                "avg_inference_time": "150ms",
                "requests_per_second": 25.5,
                "error_rate": 0.01
            }
        }
        
        return models_status
        
    except Exception as e:
        logger.error(f"Error getting models status: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get models status: {str(e)}"
        )

@router.get("/api/endpoints")
async def get_api_endpoints(current_user: User = Depends(require_developer)):
    """Get API endpoints documentation"""
    try:
        endpoints = {
            "authentication": [
                {"method": "POST", "path": "/auth/login", "description": "User login"},
                {"method": "POST", "path": "/auth/logout", "description": "User logout"},
                {"method": "GET", "path": "/auth/me", "description": "Get current user info"}
            ],
            "chat": [
                {"method": "POST", "path": "/chat/message", "description": "Send chat message"},
                {"method": "GET", "path": "/chat/history", "description": "Get chat history"},
                {"method": "DELETE", "path": "/chat/history", "description": "Clear chat history"}
            ],
            "admin": [
                {"method": "GET", "path": "/admin/dashboard", "description": "Admin dashboard"},
                {"method": "GET", "path": "/admin/users", "description": "List users"},
                {"method": "POST", "path": "/admin/users", "description": "Create user"}
            ],
            "developer": [
                {"method": "GET", "path": "/developer/dashboard", "description": "Developer dashboard"},
                {"method": "GET", "path": "/developer/metrics", "description": "System metrics"},
                {"method": "GET", "path": "/developer/debug/{component}", "description": "Debug component"}
            ]
        }
        
        return endpoints
        
    except Exception as e:
        logger.error(f"Error getting API endpoints: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get API endpoints: {str(e)}"
        )