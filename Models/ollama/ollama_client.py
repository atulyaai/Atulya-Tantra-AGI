"""
Atulya Tantra AGI - Ollama Client
Integration with Ollama GPT models including 120B Cloud
"""

import asyncio
import aiohttp
import json
import logging
import time
from typing import Dict, List, Any, Optional, AsyncGenerator
from dataclasses import dataclass
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from config.global_config import CONFIG, MODELS

@dataclass
class OllamaResponse:
    """Ollama API Response"""
    content: str
    model: str
    created_at: str
    done: bool
    total_duration: int
    load_duration: int
    prompt_eval_count: int
    prompt_eval_duration: int
    eval_count: int
    eval_duration: int
    context: List[int]

@dataclass
class ChatMessage:
    """Chat message structure"""
    role: str  # 'system', 'user', 'assistant'
    content: str
    timestamp: float = None

class OllamaClient:
    """
    Ollama Client for AGI Integration
    
    Supports:
    - Local Ollama models
    - Cloud-based models (120B GPT)
    - Streaming responses
    - Context management
    - Model switching
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or CONFIG.get_full_config().get("models", {}).get("ollama", {})
        
        # Connection settings
        self.base_url = self.config.get("base_url", "http://localhost:11434")
        self.cloud_url = self.config.get("cloud_url", "https://api.ollama.cloud")
        self.api_key = self.config.get("api_key", "")
        self.timeout = self.config.get("timeout", 300)
        
        # Model settings
        self.default_model = self.config.get("default_model", "llama2")
        self.cloud_model = self.config.get("cloud_model", "gpt-120b")
        self.available_models = []
        
        # Context management
        self.max_context_length = self.config.get("max_context_length", 4096)
        self.context_window = self.config.get("context_window", 2048)
        self.conversation_contexts = {}
        
        # Performance settings
        self.temperature = self.config.get("temperature", 0.7)
        self.top_p = self.config.get("top_p", 0.9)
        self.top_k = self.config.get("top_k", 40)
        self.repeat_penalty = self.config.get("repeat_penalty", 1.1)
        
        # Session management
        self.session = None
        self.is_connected = False
        self.last_health_check = 0
        
        logging.info("🦙 Ollama Client initialized")
    
    async def initialize(self):
        """Initialize Ollama client"""
        try:
            # Create HTTP session
            timeout = aiohttp.ClientTimeout(total=self.timeout)
            self.session = aiohttp.ClientSession(timeout=timeout)
            
            # Test connection
            await self._test_connection()
            
            # Load available models
            await self._load_available_models()
            
            self.is_connected = True
            logging.info("✅ Ollama client connected successfully")
            
        except Exception as e:
            logging.error(f"❌ Ollama client initialization failed: {e}")
            raise
    
    async def _test_connection(self):
        """Test connection to Ollama server"""
        try:
            async with self.session.get(f"{self.base_url}/api/tags") as response:
                if response.status == 200:
                    logging.info("🔗 Local Ollama connection successful")
                else:
                    logging.warning(f"⚠️ Local Ollama connection issue: {response.status}")
        except Exception as e:
            logging.warning(f"⚠️ Local Ollama not available: {e}")
            
        # Test cloud connection if API key available
        if self.api_key:
            try:
                headers = {"Authorization": f"Bearer {self.api_key}"}
                async with self.session.get(f"{self.cloud_url}/api/models", headers=headers) as response:
                    if response.status == 200:
                        logging.info("☁️ Ollama Cloud connection successful")
                    else:
                        logging.warning(f"⚠️ Ollama Cloud connection issue: {response.status}")
            except Exception as e:
                logging.warning(f"⚠️ Ollama Cloud not available: {e}")
    
    async def _load_available_models(self):
        """Load available models from Ollama"""
        try:
            # Load local models
            async with self.session.get(f"{self.base_url}/api/tags") as response:
                if response.status == 200:
                    data = await response.json()
                    local_models = [model["name"] for model in data.get("models", [])]
                    self.available_models.extend(local_models)
                    logging.info(f"📋 Local models loaded: {local_models}")
            
            # Load cloud models if available
            if self.api_key:
                headers = {"Authorization": f"Bearer {self.api_key}"}
                async with self.session.get(f"{self.cloud_url}/api/models", headers=headers) as response:
                    if response.status == 200:
                        data = await response.json()
                        cloud_models = [model["id"] for model in data.get("data", [])]
                        self.available_models.extend([f"cloud:{model}" for model in cloud_models])
                        logging.info(f"☁️ Cloud models loaded: {cloud_models}")
            
        except Exception as e:
            logging.error(f"❌ Failed to load models: {e}")
    
    async def generate(
        self,
        prompt: str,
        model: str = None,
        system_prompt: str = None,
        context: List[int] = None,
        stream: bool = False,
        **kwargs
    ) -> OllamaResponse:
        """Generate response from Ollama model"""
        try:
            model = model or self.default_model
            
            # Prepare request data
            data = {
                "model": model,
                "prompt": prompt,
                "stream": stream,
                "options": {
                    "temperature": kwargs.get("temperature", self.temperature),
                    "top_p": kwargs.get("top_p", self.top_p),
                    "top_k": kwargs.get("top_k", self.top_k),
                    "repeat_penalty": kwargs.get("repeat_penalty", self.repeat_penalty),
                }
            }
            
            if system_prompt:
                data["system"] = system_prompt
            
            if context:
                data["context"] = context
            
            # Choose endpoint based on model
            if model.startswith("cloud:"):
                url = f"{self.cloud_url}/api/generate"
                headers = {"Authorization": f"Bearer {self.api_key}"}
                data["model"] = model.replace("cloud:", "")
            else:
                url = f"{self.base_url}/api/generate"
                headers = {}
            
            # Make request
            async with self.session.post(url, json=data, headers=headers) as response:
                if response.status == 200:
                    if stream:
                        return self._handle_streaming_response(response)
                    else:
                        result = await response.json()
                        return OllamaResponse(**result)
                else:
                    error_text = await response.text()
                    raise Exception(f"Ollama API error {response.status}: {error_text}")
                    
        except Exception as e:
            logging.error(f"❌ Ollama generation failed: {e}")
            raise
    
    async def chat(
        self,
        messages: List[ChatMessage],
        model: str = None,
        conversation_id: str = "default",
        stream: bool = False,
        **kwargs
    ) -> OllamaResponse:
        """Chat with Ollama model using conversation context"""
        try:
            model = model or self.default_model
            
            # Prepare messages for API
            api_messages = []
            for msg in messages:
                api_messages.append({
                    "role": msg.role,
                    "content": msg.content
                })
            
            # Prepare request data
            data = {
                "model": model,
                "messages": api_messages,
                "stream": stream,
                "options": {
                    "temperature": kwargs.get("temperature", self.temperature),
                    "top_p": kwargs.get("top_p", self.top_p),
                    "top_k": kwargs.get("top_k", self.top_k),
                    "repeat_penalty": kwargs.get("repeat_penalty", self.repeat_penalty),
                }
            }
            
            # Add conversation context if available
            if conversation_id in self.conversation_contexts:
                data["context"] = self.conversation_contexts[conversation_id]
            
            # Choose endpoint based on model
            if model.startswith("cloud:"):
                url = f"{self.cloud_url}/api/chat"
                headers = {"Authorization": f"Bearer {self.api_key}"}
                data["model"] = model.replace("cloud:", "")
            else:
                url = f"{self.base_url}/api/chat"
                headers = {}
            
            # Make request
            async with self.session.post(url, json=data, headers=headers) as response:
                if response.status == 200:
                    if stream:
                        return self._handle_streaming_response(response)
                    else:
                        result = await response.json()
                        
                        # Update conversation context
                        if "context" in result:
                            self.conversation_contexts[conversation_id] = result["context"]
                        
                        return OllamaResponse(**result)
                else:
                    error_text = await response.text()
                    raise Exception(f"Ollama Chat API error {response.status}: {error_text}")
                    
        except Exception as e:
            logging.error(f"❌ Ollama chat failed: {e}")
            raise
    
    async def _handle_streaming_response(self, response) -> AsyncGenerator[str, None]:
        """Handle streaming response from Ollama"""
        async for line in response.content:
            if line:
                try:
                    data = json.loads(line.decode('utf-8'))
                    if "response" in data:
                        yield data["response"]
                except json.JSONDecodeError:
                    continue
    
    async def generate_cloud_120b(
        self,
        prompt: str,
        system_prompt: str = None,
        conversation_id: str = "default",
        **kwargs
    ) -> str:
        """Generate response using 120B cloud model"""
        try:
            if not self.api_key:
                raise Exception("API key required for cloud models")
            
            messages = []
            
            if system_prompt:
                messages.append(ChatMessage(
                    role="system",
                    content=system_prompt,
                    timestamp=time.time()
                ))
            
            messages.append(ChatMessage(
                role="user",
                content=prompt,
                timestamp=time.time()
            ))
            
            response = await self.chat(
                messages=messages,
                model=f"cloud:{self.cloud_model}",
                conversation_id=conversation_id,
                **kwargs
            )
            
            return response.content
            
        except Exception as e:
            logging.error(f"❌ 120B cloud generation failed: {e}")
            raise
    
    async def get_embeddings(self, text: str, model: str = "nomic-embed-text") -> List[float]:
        """Get text embeddings from Ollama"""
        try:
            data = {
                "model": model,
                "prompt": text
            }
            
            async with self.session.post(f"{self.base_url}/api/embeddings", json=data) as response:
                if response.status == 200:
                    result = await response.json()
                    return result.get("embedding", [])
                else:
                    error_text = await response.text()
                    raise Exception(f"Embeddings API error {response.status}: {error_text}")
                    
        except Exception as e:
            logging.error(f"❌ Embeddings generation failed: {e}")
            raise
    
    async def pull_model(self, model_name: str) -> bool:
        """Pull/download a model to local Ollama"""
        try:
            data = {"name": model_name}
            
            async with self.session.post(f"{self.base_url}/api/pull", json=data) as response:
                if response.status == 200:
                    # Handle streaming response for pull progress
                    async for line in response.content:
                        if line:
                            try:
                                progress = json.loads(line.decode('utf-8'))
                                if progress.get("status") == "success":
                                    logging.info(f"✅ Model {model_name} pulled successfully")
                                    return True
                                elif "error" in progress:
                                    logging.error(f"❌ Model pull error: {progress['error']}")
                                    return False
                            except json.JSONDecodeError:
                                continue
                else:
                    error_text = await response.text()
                    logging.error(f"❌ Model pull failed {response.status}: {error_text}")
                    return False
                    
        except Exception as e:
            logging.error(f"❌ Model pull failed: {e}")
            return False
    
    async def list_models(self) -> List[Dict[str, Any]]:
        """List all available models"""
        try:
            models = []
            
            # Local models
            async with self.session.get(f"{self.base_url}/api/tags") as response:
                if response.status == 200:
                    data = await response.json()
                    for model in data.get("models", []):
                        models.append({
                            "name": model["name"],
                            "size": model.get("size", 0),
                            "modified_at": model.get("modified_at", ""),
                            "type": "local"
                        })
            
            # Cloud models
            if self.api_key:
                headers = {"Authorization": f"Bearer {self.api_key}"}
                async with self.session.get(f"{self.cloud_url}/api/models", headers=headers) as response:
                    if response.status == 200:
                        data = await response.json()
                        for model in data.get("data", []):
                            models.append({
                                "name": f"cloud:{model['id']}",
                                "size": model.get("size", 0),
                                "modified_at": model.get("created", ""),
                                "type": "cloud"
                            })
            
            return models
            
        except Exception as e:
            logging.error(f"❌ Failed to list models: {e}")
            return []
    
    async def health_check(self) -> bool:
        """Check Ollama service health"""
        try:
            current_time = time.time()
            
            # Rate limit health checks
            if current_time - self.last_health_check < 30:
                return self.is_connected
            
            self.last_health_check = current_time
            
            # Test local connection
            async with self.session.get(f"{self.base_url}/api/tags") as response:
                local_healthy = response.status == 200
            
            # Test cloud connection if available
            cloud_healthy = True
            if self.api_key:
                try:
                    headers = {"Authorization": f"Bearer {self.api_key}"}
                    async with self.session.get(f"{self.cloud_url}/api/models", headers=headers) as response:
                        cloud_healthy = response.status == 200
                except:
                    cloud_healthy = False
            
            self.is_connected = local_healthy or cloud_healthy
            return self.is_connected
            
        except Exception as e:
            logging.error(f"❌ Ollama health check failed: {e}")
            self.is_connected = False
            return False
    
    async def clear_conversation(self, conversation_id: str = "default"):
        """Clear conversation context"""
        if conversation_id in self.conversation_contexts:
            del self.conversation_contexts[conversation_id]
            logging.info(f"🗑️ Conversation {conversation_id} context cleared")
    
    async def get_model_info(self, model_name: str) -> Dict[str, Any]:
        """Get detailed model information"""
        try:
            data = {"name": model_name}
            
            async with self.session.post(f"{self.base_url}/api/show", json=data) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    error_text = await response.text()
                    raise Exception(f"Model info API error {response.status}: {error_text}")
                    
        except Exception as e:
            logging.error(f"❌ Failed to get model info: {e}")
            return {}
    
    async def shutdown(self):
        """Shutdown Ollama client"""
        try:
            if self.session:
                await self.session.close()
            
            self.is_connected = False
            logging.info("🛑 Ollama client shutdown complete")
            
        except Exception as e:
            logging.error(f"❌ Ollama client shutdown error: {e}")

# Convenience functions
async def create_ollama_client(config: Dict[str, Any] = None) -> OllamaClient:
    """Create and initialize Ollama client"""
    client = OllamaClient(config)
    await client.initialize()
    return client

async def quick_generate(prompt: str, model: str = None, **kwargs) -> str:
    """Quick generation without managing client lifecycle"""
    client = await create_ollama_client()
    try:
        response = await client.generate(prompt, model, **kwargs)
        return response.content
    finally:
        await client.shutdown()

async def quick_chat(messages: List[ChatMessage], model: str = None, **kwargs) -> str:
    """Quick chat without managing client lifecycle"""
    client = await create_ollama_client()
    try:
        response = await client.chat(messages, model, **kwargs)
        return response.content
    finally:
        await client.shutdown()