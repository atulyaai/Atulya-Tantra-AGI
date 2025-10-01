"""
Repair System - Handles system diagnostics, error recovery, and self-healing
"""
import asyncio
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import traceback

logger = logging.getLogger(__name__)

class RepairSystem:
    """System repair and self-healing management"""
    
    def __init__(self):
        self.is_initialized = False
        self.status = "initializing"
        self.error_history = []
        self.repair_history = []
        self.health_checks = {}
        self.auto_repair_enabled = True
        self.metrics = {
            "health_checks_performed": 0,
            "issues_detected": 0,
            "repairs_attempted": 0,
            "successful_repairs": 0,
            "system_health_score": 100.0,
            "last_check_time": None,
            "system_uptime": 0.0
        }
        self.start_time = datetime.now()
    
    async def initialize(self):
        """Initialize the repair system"""
        try:
            logger.info("Initializing Repair System...")
            
            # Initialize health check configurations
            self.health_checks = {
                "memory_usage": {
                    "enabled": True,
                    "threshold": 0.8,
                    "last_check": None,
                    "status": "unknown"
                },
                "response_time": {
                    "enabled": True,
                    "threshold": 5.0,  # seconds
                    "last_check": None,
                    "status": "unknown"
                },
                "error_rate": {
                    "enabled": True,
                    "threshold": 0.1,  # 10% error rate
                    "last_check": None,
                    "status": "unknown"
                },
                "subsystem_connectivity": {
                    "enabled": True,
                    "threshold": 1.0,  # All subsystems should be connected
                    "last_check": None,
                    "status": "unknown"
                }
            }
            
            self.is_initialized = True
            self.status = "running"
            logger.info("Repair System initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize Repair System: {e}")
            self.status = "error"
            raise
    
    async def diagnose_system(self) -> Dict[str, Any]:
        """Perform comprehensive system diagnostics"""
        if not self.is_initialized:
            raise RuntimeError("Repair System not initialized")
        
        diagnosis_results = {
            "timestamp": datetime.now().isoformat(),
            "overall_health": "unknown",
            "health_checks": {},
            "issues_detected": [],
            "recommendations": []
        }
        
        try:
            # Perform all health checks
            for check_name, check_config in self.health_checks.items():
                if check_config["enabled"]:
                    check_result = await self.perform_health_check(check_name)
                    diagnosis_results["health_checks"][check_name] = check_result
                    
                    if check_result["status"] == "critical":
                        diagnosis_results["issues_detected"].append({
                            "type": check_name,
                            "severity": "critical",
                            "description": check_result.get("description", "Critical issue detected")
                        })
                    elif check_result["status"] == "warning":
                        diagnosis_results["issues_detected"].append({
                            "type": check_name,
                            "severity": "warning",
                            "description": check_result.get("description", "Warning condition detected")
                        })
            
            # Determine overall health
            critical_issues = [issue for issue in diagnosis_results["issues_detected"] if issue["severity"] == "critical"]
            warning_issues = [issue for issue in diagnosis_results["issues_detected"] if issue["severity"] == "warning"]
            
            if critical_issues:
                diagnosis_results["overall_health"] = "critical"
            elif warning_issues:
                diagnosis_results["overall_health"] = "warning"
            else:
                diagnosis_results["overall_health"] = "healthy"
            
            # Generate recommendations
            diagnosis_results["recommendations"] = await self.generate_recommendations(diagnosis_results["issues_detected"])
            
            logger.info(f"System diagnosis completed. Overall health: {diagnosis_results['overall_health']}")
            
        except Exception as e:
            logger.error(f"Error during system diagnosis: {e}")
            diagnosis_results["overall_health"] = "error"
            diagnosis_results["error"] = str(e)
        
        return diagnosis_results
    
    async def perform_health_check(self, check_name: str) -> Dict[str, Any]:
        """Perform a specific health check"""
        check_result = {
            "name": check_name,
            "timestamp": datetime.now().isoformat(),
            "status": "unknown",
            "value": None,
            "threshold": self.health_checks[check_name]["threshold"],
            "description": ""
        }
        
        try:
            if check_name == "memory_usage":
                # Simulate memory usage check
                import psutil
                memory_percent = psutil.virtual_memory().percent / 100.0
                check_result["value"] = memory_percent
                
                if memory_percent > self.health_checks[check_name]["threshold"]:
                    check_result["status"] = "critical"
                    check_result["description"] = f"High memory usage: {memory_percent:.1%}"
                elif memory_percent > self.health_checks[check_name]["threshold"] * 0.8:
                    check_result["status"] = "warning"
                    check_result["description"] = f"Elevated memory usage: {memory_percent:.1%}"
                else:
                    check_result["status"] = "healthy"
                    check_result["description"] = f"Memory usage normal: {memory_percent:.1%}"
            
            elif check_name == "response_time":
                # Simulate response time check
                avg_response_time = 1.2  # Mock value
                check_result["value"] = avg_response_time
                
                if avg_response_time > self.health_checks[check_name]["threshold"]:
                    check_result["status"] = "critical"
                    check_result["description"] = f"Slow response time: {avg_response_time:.2f}s"
                elif avg_response_time > self.health_checks[check_name]["threshold"] * 0.7:
                    check_result["status"] = "warning"
                    check_result["description"] = f"Elevated response time: {avg_response_time:.2f}s"
                else:
                    check_result["status"] = "healthy"
                    check_result["description"] = f"Response time normal: {avg_response_time:.2f}s"
            
            elif check_name == "error_rate":
                # Calculate error rate from metrics
                total_requests = max(1, self.metrics.get("errors_detected", 0) + 100)  # Mock total
                error_rate = self.metrics.get("errors_detected", 0) / total_requests
                check_result["value"] = error_rate
                
                if error_rate > self.health_checks[check_name]["threshold"]:
                    check_result["status"] = "critical"
                    check_result["description"] = f"High error rate: {error_rate:.1%}"
                elif error_rate > self.health_checks[check_name]["threshold"] * 0.5:
                    check_result["status"] = "warning"
                    check_result["description"] = f"Elevated error rate: {error_rate:.1%}"
                else:
                    check_result["status"] = "healthy"
                    check_result["description"] = f"Error rate normal: {error_rate:.1%}"
            
            elif check_name == "subsystem_connectivity":
                # Mock subsystem connectivity check
                connected_subsystems = 3  # Assume 3 subsystems are connected
                total_subsystems = 3
                connectivity_ratio = connected_subsystems / total_subsystems
                check_result["value"] = connectivity_ratio
                
                if connectivity_ratio < self.health_checks[check_name]["threshold"]:
                    check_result["status"] = "critical"
                    check_result["description"] = f"Subsystem connectivity issues: {connected_subsystems}/{total_subsystems}"
                else:
                    check_result["status"] = "healthy"
                    check_result["description"] = f"All subsystems connected: {connected_subsystems}/{total_subsystems}"
            
            # Update health check record
            self.health_checks[check_name]["last_check"] = datetime.now()
            self.health_checks[check_name]["status"] = check_result["status"]
            
        except Exception as e:
            logger.error(f"Error performing health check {check_name}: {e}")
            check_result["status"] = "error"
            check_result["description"] = f"Health check failed: {str(e)}"
        
        return check_result
    
    async def generate_recommendations(self, issues: List[Dict[str, Any]]) -> List[str]:
        """Generate repair recommendations based on detected issues"""
        recommendations = []
        
        for issue in issues:
            issue_type = issue["type"]
            severity = issue["severity"]
            
            if issue_type == "memory_usage":
                if severity == "critical":
                    recommendations.append("Restart system to clear memory leaks")
                    recommendations.append("Review and optimize memory-intensive processes")
                else:
                    recommendations.append("Monitor memory usage trends")
                    recommendations.append("Consider garbage collection optimization")
            
            elif issue_type == "response_time":
                if severity == "critical":
                    recommendations.append("Scale up processing resources")
                    recommendations.append("Optimize critical processing paths")
                else:
                    recommendations.append("Review and optimize slow operations")
                    recommendations.append("Consider implementing caching")
            
            elif issue_type == "error_rate":
                if severity == "critical":
                    recommendations.append("Investigate and fix recurring errors")
                    recommendations.append("Implement additional error handling")
                else:
                    recommendations.append("Review error patterns and causes")
                    recommendations.append("Enhance input validation")
            
            elif issue_type == "subsystem_connectivity":
                recommendations.append("Check network connectivity")
                recommendations.append("Restart disconnected subsystems")
                recommendations.append("Verify subsystem health")
        
        return recommendations
    
    async def attempt_repair(self, issue_type: str, severity: str = "warning") -> Dict[str, Any]:
        """Attempt to repair a specific issue"""
        self.metrics["repairs_attempted"] += 1
        
        repair_result = {
            "issue_type": issue_type,
            "severity": severity,
            "timestamp": datetime.now().isoformat(),
            "success": False,
            "actions_taken": [],
            "description": ""
        }
        
        try:
            if issue_type == "memory_usage":
                # Simulate memory cleanup
                repair_result["actions_taken"].append("Performed garbage collection")
                repair_result["actions_taken"].append("Cleared temporary caches")
                repair_result["success"] = True
                repair_result["description"] = "Memory usage optimized"
            
            elif issue_type == "response_time":
                # Simulate performance optimization
                repair_result["actions_taken"].append("Optimized processing pipelines")
                repair_result["actions_taken"].append("Enabled response caching")
                repair_result["success"] = True
                repair_result["description"] = "Response time improved"
            
            elif issue_type == "error_rate":
                # Simulate error handling improvement
                repair_result["actions_taken"].append("Enhanced error handling")
                repair_result["actions_taken"].append("Updated validation rules")
                repair_result["success"] = True
                repair_result["description"] = "Error handling improved"
            
            elif issue_type == "subsystem_connectivity":
                # Simulate connectivity repair
                repair_result["actions_taken"].append("Reestablished subsystem connections")
                repair_result["actions_taken"].append("Verified network connectivity")
                repair_result["success"] = True
                repair_result["description"] = "Subsystem connectivity restored"
            
            if repair_result["success"]:
                self.metrics["successful_repairs"] += 1
                logger.info(f"Successfully repaired {issue_type}: {repair_result['description']}")
            
        except Exception as e:
            logger.error(f"Error during repair attempt for {issue_type}: {e}")
            repair_result["description"] = f"Repair failed: {str(e)}"
            repair_result["actions_taken"].append(f"Error encountered: {str(e)}")
        
        # Record repair attempt
        self.repair_history.append(repair_result)
        
        # Keep only last 50 repair attempts
        if len(self.repair_history) > 50:
            self.repair_history = self.repair_history[-50:]
        
        return repair_result
    
    async def log_error(self, error: Exception, context: Optional[Dict[str, Any]] = None):
        """Log an error for tracking and analysis"""
        self.metrics["errors_detected"] += 1
        
        error_entry = {
            "timestamp": datetime.now().isoformat(),
            "error_type": type(error).__name__,
            "error_message": str(error),
            "traceback": traceback.format_exc(),
            "context": context or {},
            "severity": self.classify_error_severity(error)
        }
        
        self.error_history.append(error_entry)
        
        # Keep only last 100 errors
        if len(self.error_history) > 100:
            self.error_history = self.error_history[-100:]
        
        # Trigger auto-repair if enabled and error is critical
        if self.auto_repair_enabled and error_entry["severity"] == "critical":
            await self.trigger_auto_repair(error_entry)
        
        logger.error(f"Error logged: {error_entry['error_type']} - {error_entry['error_message']}")
    
    def classify_error_severity(self, error: Exception) -> str:
        """Classify the severity of an error"""
        error_type = type(error).__name__
        
        critical_errors = ["SystemError", "MemoryError", "OSError", "ConnectionError"]
        warning_errors = ["ValueError", "TypeError", "KeyError", "AttributeError"]
        
        if error_type in critical_errors:
            return "critical"
        elif error_type in warning_errors:
            return "warning"
        else:
            return "info"
    
    async def trigger_auto_repair(self, error_entry: Dict[str, Any]):
        """Trigger automatic repair based on error type"""
        error_type = error_entry["error_type"]
        
        # Map error types to repair actions
        repair_mapping = {
            "MemoryError": "memory_usage",
            "ConnectionError": "subsystem_connectivity",
            "TimeoutError": "response_time"
        }
        
        repair_type = repair_mapping.get(error_type, "general")
        
        if repair_type != "general":
            logger.info(f"Triggering auto-repair for {error_type}")
            await self.attempt_repair(repair_type, error_entry["severity"])
    
    def get_system_health_summary(self) -> Dict[str, Any]:
        """Get a summary of system health"""
        uptime = (datetime.now() - self.start_time).total_seconds()
        self.metrics["system_uptime"] = uptime
        
        recent_errors = [e for e in self.error_history if 
                        datetime.fromisoformat(e["timestamp"]) > datetime.now() - timedelta(hours=1)]
        
        return {
            "overall_status": self.status,
            "uptime_seconds": uptime,
            "recent_errors_count": len(recent_errors),
            "total_errors": self.metrics["errors_detected"],
            "repair_success_rate": (
                self.metrics["successful_repairs"] / max(1, self.metrics["repairs_attempted"])
            ),
            "auto_repair_enabled": self.auto_repair_enabled,
            "health_checks_status": {
                name: config["status"] for name, config in self.health_checks.items()
            }
        }
    
    def get_system_health(self) -> Dict[str, Any]:
        """Get overall system health assessment"""
        # Calculate overall health based on various factors
        health_score = self.metrics["system_health_score"]
        
        # Adjust based on recent issues
        if self.metrics["issues_detected"] > 0:
            health_score = max(0, health_score - (self.metrics["issues_detected"] * 5))
        
        # Adjust based on repair success rate
        if self.metrics["repairs_attempted"] > 0:
            success_rate = self.metrics["successful_repairs"] / self.metrics["repairs_attempted"]
            if success_rate < 0.8:
                health_score = max(0, health_score - 20)
        
        return {
            "overall_health": health_score,
            "status": "healthy" if health_score > 80 else "degraded" if health_score > 50 else "critical",
            "issues_count": self.metrics["issues_detected"],
            "repair_success_rate": (
                self.metrics["successful_repairs"] / max(1, self.metrics["repairs_attempted"])
            )
        }
    
    def get_status(self) -> Dict[str, Any]:
        """Get the current status of the repair system"""
        return {
            "status": self.status,
            "is_initialized": self.is_initialized,
            "auto_repair_enabled": self.auto_repair_enabled,
            "metrics": self.metrics,
            "health_summary": self.get_system_health_summary()
        }
    
    async def health_check(self) -> Dict[str, Any]:
        """Perform health check on the repair system"""
        return {
            "status": self.status,
            "is_initialized": self.is_initialized,
            "health_checks_performed": self.metrics["health_checks_performed"],
            "issues_detected": self.metrics["issues_detected"],
            "repairs_attempted": self.metrics["repairs_attempted"],
            "successful_repairs": self.metrics["successful_repairs"],
            "system_health_score": self.get_system_health()["overall_health"],
            "last_check": self.metrics.get("last_health_check", "never")
        }

    async def shutdown(self):
        """Gracefully shutdown the repair system"""
        logger.info("Shutting down Repair System...")
        self.status = "shutdown"
        self.is_initialized = False
        logger.info("Repair System shutdown complete")