"""
Atulya Tantra AGI - Global Configuration System
Centralized configuration for all system components, paths, models, and variables
"""

import os
from pathlib import Path
from typing import Dict, Any, List
from dataclasses import dataclass
from enum import Enum

# Base project paths
PROJECT_ROOT = Path(__file__).parent.parent.absolute()
CONFIG_DIR = PROJECT_ROOT / "config"
MODELS_DIR = PROJECT_ROOT / "Models"
CORE_DIR = PROJECT_ROOT / "core"
WEBUI_DIR = PROJECT_ROOT / "webui"
DATA_DIR = PROJECT_ROOT / "data"
LOGS_DIR = DATA_DIR / "logs"
CACHE_DIR = DATA_DIR / "cache"
BACKUP_DIR = DATA_DIR / "backups"

class AGIMode(Enum):
    """AGI Operation Modes"""
    JARVIS = "jarvis"  # Helpful assistant mode
    SKYNET = "skynet"  # Autonomous evolution mode
    HYBRID = "hybrid"  # Combined mode

class ModelType(Enum):
    """AI Model Types"""
    OLLAMA = "ollama"
    LANGRAPH = "langraph"
    CUSTOM = "custom"
    PRETRAINED = "pretrained"

@dataclass
class ModelConfig:
    """Model Configuration"""
    name: str
    type: ModelType
    path: str
    version: str
    parameters: Dict[str, Any]
    enabled: bool = True

@dataclass
class SystemPaths:
    """System Path Configuration"""
    # Core directories
    project_root: str = str(PROJECT_ROOT)
    config_dir: str = str(CONFIG_DIR)
    models_dir: str = str(MODELS_DIR)
    core_dir: str = str(CORE_DIR)
    webui_dir: str = str(WEBUI_DIR)
    data_dir: str = str(DATA_DIR)
    
    # Model paths
    ollama_models: str = str(MODELS_DIR / "ollama")
    langraph_models: str = str(MODELS_DIR / "langraph")
    custom_models: str = str(MODELS_DIR / "custom")
    pretrained_models: str = str(MODELS_DIR / "pretrained")
    
    # Core component paths
    agi_engine: str = str(CORE_DIR / "agi_engine")
    memory_system: str = str(CORE_DIR / "memory")
    learning_system: str = str(CORE_DIR / "learning")
    reasoning_system: str = str(CORE_DIR / "reasoning")
    evolution_system: str = str(CORE_DIR / "evolution")
    repair_system: str = str(CORE_DIR / "repair_system")
    improvement_system: str = str(CORE_DIR / "self_improvement")
    
    # WebUI paths
    backend_path: str = str(WEBUI_DIR / "backend")
    frontend_path: str = str(WEBUI_DIR / "frontend")
    admin_path: str = str(WEBUI_DIR / "admin")
    
    # Data paths
    logs_path: str = str(LOGS_DIR)
    cache_path: str = str(CACHE_DIR)
    backup_path: str = str(BACKUP_DIR)
    knowledge_base: str = str(DATA_DIR / "knowledge_base")
    
    # Configuration files
    main_config: str = str(CONFIG_DIR / "config.yaml")
    model_config: str = str(CONFIG_DIR / "models.yaml")
    security_config: str = str(CONFIG_DIR / "security.yaml")

class GlobalConfig:
    """Global Configuration Manager"""
    
    # System Information
    SYSTEM_NAME = "Atulya Tantra AGI"
    VERSION = "1.0.0"
    DESCRIPTION = "Advanced AGI System with Jarvis and Skynet capabilities"
    
    # Paths
    PATHS = SystemPaths()
    
    # AGI Configuration
    AGI_CONFIG = {
        "mode": AGIMode.HYBRID,
        "intelligence_level": 1.0,
        "max_intelligence_level": 10.0,
        "learning_rate": 0.01,
        "evolution_rate": 0.001,
        "self_improvement_interval": 3600,  # 1 hour
        "evolution_interval": 7200,  # 2 hours
        "maintenance_interval": 300,  # 5 minutes
        "max_concurrent_tasks": 10,
        "memory_limit_gb": 16,
        "processing_timeout": 300,  # 5 minutes
    }
    
    # Model Configurations
    MODELS = {
        "ollama_gpt": ModelConfig(
            name="ollama-gpt-120b",
            type=ModelType.OLLAMA,
            path=str(MODELS_DIR / "ollama" / "gpt-120b"),
            version="latest",
            parameters={
                "temperature": 0.7,
                "max_tokens": 4096,
                "top_p": 0.9,
                "frequency_penalty": 0.0,
                "presence_penalty": 0.0,
                "context_window": 32768,
            }
        ),
        "langraph_agent": ModelConfig(
            name="langraph-agent",
            type=ModelType.LANGRAPH,
            path=str(MODELS_DIR / "langraph" / "agent"),
            version="latest",
            parameters={
                "max_iterations": 50,
                "recursion_limit": 100,
                "memory_size": 1000,
                "planning_depth": 5,
            }
        ),
        "reasoning_model": ModelConfig(
            name="reasoning-engine",
            type=ModelType.CUSTOM,
            path=str(MODELS_DIR / "custom" / "reasoning"),
            version="1.0.0",
            parameters={
                "logic_depth": 10,
                "inference_steps": 100,
                "confidence_threshold": 0.8,
            }
        ),
        "memory_model": ModelConfig(
            name="memory-system",
            type=ModelType.CUSTOM,
            path=str(MODELS_DIR / "custom" / "memory"),
            version="1.0.0",
            parameters={
                "vector_dimensions": 1536,
                "similarity_threshold": 0.7,
                "max_memories": 1000000,
                "compression_ratio": 0.1,
            }
        )
    }
    
    # Database Configuration
    DATABASE_CONFIG = {
        "type": "postgresql",
        "host": "localhost",
        "port": 5432,
        "database": "atulya_tantra_agi",
        "username": "agi_user",
        "password": "secure_password_123",
        "pool_size": 20,
        "max_overflow": 30,
        "pool_timeout": 30,
        "pool_recycle": 3600,
    }
    
    # Redis Configuration
    REDIS_CONFIG = {
        "host": "localhost",
        "port": 6379,
        "db": 0,
        "password": None,
        "max_connections": 100,
        "socket_timeout": 30,
        "socket_connect_timeout": 30,
        "retry_on_timeout": True,
    }
    
    # API Configuration
    API_CONFIG = {
        "host": "0.0.0.0",
        "port": 8000,
        "debug": False,
        "reload": False,
        "workers": 4,
        "max_request_size": 100 * 1024 * 1024,  # 100MB
        "timeout": 300,
        "cors_origins": ["*"],
        "rate_limit": {
            "requests_per_minute": 100,
            "burst_size": 200,
        }
    }
    
    # WebUI Configuration
    WEBUI_CONFIG = {
        "frontend": {
            "port": 3000,
            "build_path": str(WEBUI_DIR / "frontend" / "build"),
            "public_path": str(WEBUI_DIR / "frontend" / "public"),
        },
        "admin": {
            "port": 3001,
            "build_path": str(WEBUI_DIR / "admin" / "build"),
            "public_path": str(WEBUI_DIR / "admin" / "public"),
        }
    }
    
    # Security Configuration
    SECURITY_CONFIG = {
        "jwt_secret": "your-super-secret-jwt-key-change-this-in-production",
        "jwt_algorithm": "HS256",
        "jwt_expiration": 3600,  # 1 hour
        "bcrypt_rounds": 12,
        "max_login_attempts": 5,
        "lockout_duration": 900,  # 15 minutes
        "session_timeout": 7200,  # 2 hours
        "csrf_protection": True,
        "https_only": False,  # Set to True in production
    }
    
    # Monitoring Configuration
    MONITORING_CONFIG = {
        "metrics_enabled": True,
        "logging_level": "INFO",
        "log_rotation": "daily",
        "log_retention_days": 30,
        "performance_tracking": True,
        "error_tracking": True,
        "health_check_interval": 60,  # 1 minute
        "alerts": {
            "email_enabled": False,
            "slack_enabled": False,
            "webhook_url": None,
        }
    }
    
    # Learning Configuration
    LEARNING_CONFIG = {
        "continuous_learning": True,
        "batch_size": 32,
        "learning_rate": 0.001,
        "momentum": 0.9,
        "weight_decay": 0.0001,
        "gradient_clipping": 1.0,
        "validation_split": 0.2,
        "early_stopping_patience": 10,
        "checkpoint_interval": 1000,
        "max_epochs": 1000,
    }
    
    # Evolution Configuration
    EVOLUTION_CONFIG = {
        "population_size": 50,
        "mutation_rate": 0.1,
        "crossover_rate": 0.8,
        "selection_pressure": 2.0,
        "elitism_rate": 0.1,
        "diversity_threshold": 0.8,
        "fitness_function": "adaptive_intelligence",
        "max_generations": 1000,
        "convergence_threshold": 0.001,
    }
    
    # Memory Configuration
    MEMORY_CONFIG = {
        "short_term_capacity": 1000,
        "long_term_capacity": 1000000,
        "working_memory_size": 100,
        "episodic_memory_size": 10000,
        "semantic_memory_size": 100000,
        "procedural_memory_size": 50000,
        "memory_consolidation_interval": 3600,  # 1 hour
        "forgetting_curve_factor": 0.1,
        "importance_threshold": 0.5,
    }
    
    # Reasoning Configuration
    REASONING_CONFIG = {
        "max_reasoning_depth": 10,
        "confidence_threshold": 0.7,
        "logic_engine": "first_order_logic",
        "inference_methods": ["deduction", "induction", "abduction"],
        "uncertainty_handling": "bayesian",
        "causal_reasoning": True,
        "temporal_reasoning": True,
        "spatial_reasoning": True,
        "analogical_reasoning": True,
    }
    
    # Self-Improvement Configuration
    IMPROVEMENT_CONFIG = {
        "auto_improvement": True,
        "improvement_threshold": 0.05,
        "max_improvement_cycles": 100,
        "performance_metrics": [
            "accuracy", "speed", "efficiency", "adaptability"
        ],
        "improvement_strategies": [
            "parameter_tuning", "architecture_modification", 
            "training_optimization", "knowledge_integration"
        ],
        "safety_checks": True,
        "rollback_enabled": True,
        "backup_before_improvement": True,
    }
    
    # Repair System Configuration
    REPAIR_CONFIG = {
        "auto_repair": True,
        "diagnostic_interval": 300,  # 5 minutes
        "repair_strategies": [
            "restart_component", "reset_parameters", 
            "reload_model", "fallback_mode"
        ],
        "max_repair_attempts": 3,
        "escalation_threshold": 5,
        "backup_restoration": True,
        "health_check_timeout": 30,
    }
    
    # File Extensions and Types
    SUPPORTED_FORMATS = {
        "text": [".txt", ".md", ".json", ".yaml", ".yml", ".xml"],
        "code": [".py", ".js", ".ts", ".html", ".css", ".sql"],
        "data": [".csv", ".xlsx", ".parquet", ".h5", ".pkl"],
        "models": [".pkl", ".joblib", ".h5", ".onnx", ".pt", ".pth"],
        "images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg"],
        "audio": [".mp3", ".wav", ".flac", ".ogg"],
        "video": [".mp4", ".avi", ".mkv", ".mov"],
    }
    
    # Environment Variables
    ENV_VARS = {
        "ATULYA_AGI_MODE": AGI_CONFIG["mode"].value,
        "ATULYA_AGI_VERSION": VERSION,
        "ATULYA_AGI_ROOT": str(PROJECT_ROOT),
        "ATULYA_AGI_CONFIG": str(CONFIG_DIR),
        "ATULYA_AGI_MODELS": str(MODELS_DIR),
        "ATULYA_AGI_DATA": str(DATA_DIR),
        "ATULYA_AGI_LOGS": str(LOGS_DIR),
    }
    
    @classmethod
    def get_model_config(cls, model_name: str) -> ModelConfig:
        """Get configuration for a specific model"""
        return cls.MODELS.get(model_name)
    
    @classmethod
    def get_model_path(cls, model_name: str) -> str:
        """Get path for a specific model"""
        model_config = cls.get_model_config(model_name)
        return model_config.path if model_config else None
    
    @classmethod
    def get_component_path(cls, component: str) -> str:
        """Get path for a specific component"""
        return getattr(cls.PATHS, f"{component}_system", None)
    
    @classmethod
    def create_directories(cls):
        """Create all necessary directories"""
        directories = [
            cls.PATHS.models_dir,
            cls.PATHS.ollama_models,
            cls.PATHS.langraph_models,
            cls.PATHS.custom_models,
            cls.PATHS.pretrained_models,
            cls.PATHS.logs_path,
            cls.PATHS.cache_path,
            cls.PATHS.backup_path,
            cls.PATHS.knowledge_base,
        ]
        
        for directory in directories:
            Path(directory).mkdir(parents=True, exist_ok=True)
    
    @classmethod
    def set_environment_variables(cls):
        """Set environment variables"""
        for key, value in cls.ENV_VARS.items():
            os.environ[key] = str(value)
    
    @classmethod
    def validate_configuration(cls) -> Dict[str, bool]:
        """Validate all configuration settings"""
        validation_results = {}
        
        # Check if directories exist
        validation_results["directories"] = all([
            Path(cls.PATHS.project_root).exists(),
            Path(cls.PATHS.models_dir).exists(),
            Path(cls.PATHS.core_dir).exists(),
        ])
        
        # Check model configurations
        validation_results["models"] = all([
            model.enabled for model in cls.MODELS.values()
        ])
        
        # Check database configuration
        validation_results["database"] = all([
            cls.DATABASE_CONFIG.get("host"),
            cls.DATABASE_CONFIG.get("database"),
            cls.DATABASE_CONFIG.get("username"),
        ])
        
        return validation_results
    
    @classmethod
    def get_full_config(cls) -> Dict[str, Any]:
        """Get complete configuration as dictionary"""
        return {
            "system": {
                "name": cls.SYSTEM_NAME,
                "version": cls.VERSION,
                "description": cls.DESCRIPTION,
            },
            "paths": cls.PATHS.__dict__,
            "agi": cls.AGI_CONFIG,
            "models": {name: config.__dict__ for name, config in cls.MODELS.items()},
            "database": cls.DATABASE_CONFIG,
            "redis": cls.REDIS_CONFIG,
            "api": cls.API_CONFIG,
            "webui": cls.WEBUI_CONFIG,
            "security": cls.SECURITY_CONFIG,
            "monitoring": cls.MONITORING_CONFIG,
            "learning": cls.LEARNING_CONFIG,
            "evolution": cls.EVOLUTION_CONFIG,
            "memory": cls.MEMORY_CONFIG,
            "reasoning": cls.REASONING_CONFIG,
            "improvement": cls.IMPROVEMENT_CONFIG,
            "repair": cls.REPAIR_CONFIG,
        }

# Initialize configuration on import
GlobalConfig.create_directories()
GlobalConfig.set_environment_variables()

# Export commonly used configurations
CONFIG = GlobalConfig()
PATHS = GlobalConfig.PATHS
MODELS = GlobalConfig.MODELS
AGI_CONFIG = GlobalConfig.AGI_CONFIG