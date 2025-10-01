"""
Cognitive System - Handles reasoning, memory, and learning processes
"""
import asyncio
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime
import json

logger = logging.getLogger(__name__)

class CognitiveSystem:
    """Cognitive processing system for reasoning and memory management"""
    
    def __init__(self, model_integration=None):
        self.is_initialized = False
        self.status = "initializing"
        self.memory_store = {}
        self.reasoning_cache = {}
        self.learning_history = []
        self.model_integration = model_integration
        self.metrics = {
            "memory_operations": 0,
            "reasoning_requests": 0,
            "learning_sessions": 0
        }
    
    async def initialize(self):
        """Initialize the cognitive system"""
        try:
            logger.info("Initializing Cognitive System...")
            
            # Initialize memory subsystems
            self.memory_store = {
                "short_term": {},
                "long_term": {},
                "episodic": [],
                "semantic": {}
            }
            
            self.is_initialized = True
            self.status = "running"
            logger.info("Cognitive System initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize Cognitive System: {e}")
            self.status = "error"
            raise
    
    async def process(self, message: str, context: Optional[Dict[str, Any]] = None) -> str:
        """Process a message through cognitive reasoning"""
        if not self.is_initialized:
            raise RuntimeError("Cognitive System not initialized")
        
        try:
            # Store the interaction in episodic memory
            await self.store_memory("episodic", {
                "message": message,
                "context": context,
                "timestamp": datetime.now().isoformat()
            })
            
            # Perform reasoning
            reasoning_result = await self.reason_about(message, context)
            
            # Generate response based on reasoning
            response = await self.generate_response(reasoning_result, message, context)
            
            return response
            
        except Exception as e:
            logger.error(f"Error in cognitive processing: {e}")
            return f"I apologize, but I encountered an error while processing your request: {str(e)}"
    
    async def reason_about(self, message: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Perform reasoning about the given message"""
        self.metrics["reasoning_requests"] += 1
        
        # Simple reasoning simulation
        reasoning_result = {
            "intent": self._analyze_intent(message),
            "entities": self._extract_entities(message),
            "sentiment": self._analyze_sentiment(message),
            "context_relevance": self._assess_context_relevance(context),
            "confidence": 0.85
        }
        
        # Cache the reasoning result
        cache_key = f"{hash(message)}_{hash(str(context))}"
        self.reasoning_cache[cache_key] = reasoning_result
        
        return reasoning_result
    
    async def generate_response(self, reasoning: Dict[str, Any], message: str, context: Optional[Dict[str, Any]] = None) -> str:
        """Generate a response based on reasoning results"""
        intent = reasoning.get("intent", "unknown")
        confidence = reasoning.get("confidence", 0.5)
        
        if intent == "greeting":
            return "Hello! I'm the Atulya Tantra AGI system. How can I assist you today?"
        elif intent == "question":
            return f"That's an interesting question about '{message}'. Based on my analysis (confidence: {confidence:.2f}), I believe this relates to your inquiry. Let me help you explore this further."
        elif intent == "request":
            return f"I understand you're requesting something. I'll do my best to help with: {message}"
        elif intent == "conversation":
            return f"I appreciate our conversation. Regarding '{message}', I find this topic quite engaging. What would you like to explore further?"
        else:
            return f"I've processed your message: '{message}'. While I'm still learning to understand all nuances, I'm here to help however I can."
    
    def process_input(self, message: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Process input message and return response (synchronous wrapper for async process)"""
        try:
            # If we have model integration, use the real LLM
            if self.model_integration:
                import asyncio
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                try:
                    # Generate response using real LLM
                    llm_result = loop.run_until_complete(
                        self.model_integration.generate_response(message)
                    )
                    
                    if llm_result.get("success", False):
                        response = llm_result.get("response", "I'm processing your request.")
                    else:
                        response = "I'm experiencing some technical difficulties with the AI model. Please try again."
                    
                    # Store interaction in memory
                    loop.run_until_complete(self.store_memory("episodic", {
                        "message": message,
                        "response": response,
                        "context": context,
                        "timestamp": datetime.now().isoformat(),
                        "model_used": "ollama",
                        "success": llm_result.get("success", False)
                    }))
                    
                    return {
                        "response": response,
                        "model_used": "ollama",
                        "processing_time": llm_result.get("response_time", 0),
                        "success": llm_result.get("success", False)
                    }
                finally:
                    loop.close()
            else:
                # Fallback to simple cognitive processing
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                try:
                    response = loop.run_until_complete(self.process(message, context))
                    return {
                        "response": response,
                        "model_used": "cognitive_fallback",
                        "success": True
                    }
                finally:
                    loop.close()
                    
        except Exception as e:
            logger.error(f"Error in process_input: {e}")
            return {
                "response": f"I apologize, but I encountered an error: {str(e)}",
                "model_used": "error_fallback",
                "success": False,
                "error": str(e)
            }
    
    def _analyze_intent(self, message: str) -> str:
        """Simple intent analysis"""
        message_lower = message.lower()
        
        if any(word in message_lower for word in ["hello", "hi", "hey", "greetings"]):
            return "greeting"
        elif any(word in message_lower for word in ["what", "how", "why", "when", "where", "?"]):
            return "question"
        elif any(word in message_lower for word in ["please", "can you", "could you", "help me"]):
            return "request"
        else:
            return "conversation"
    
    def _extract_entities(self, message: str) -> List[str]:
        """Simple entity extraction"""
        # This is a mock implementation
        words = message.split()
        entities = [word for word in words if word.istitle() and len(word) > 2]
        return entities
    
    def _analyze_sentiment(self, message: str) -> str:
        """Simple sentiment analysis"""
        positive_words = ["good", "great", "excellent", "amazing", "wonderful", "love", "like"]
        negative_words = ["bad", "terrible", "awful", "hate", "dislike", "horrible"]
        
        message_lower = message.lower()
        positive_count = sum(1 for word in positive_words if word in message_lower)
        negative_count = sum(1 for word in negative_words if word in message_lower)
        
        if positive_count > negative_count:
            return "positive"
        elif negative_count > positive_count:
            return "negative"
        else:
            return "neutral"
    
    def _assess_context_relevance(self, context: Optional[Dict[str, Any]]) -> float:
        """Assess the relevance of provided context"""
        if not context:
            return 0.0
        
        # Simple relevance scoring based on context richness
        relevance_score = min(len(context) * 0.1, 1.0)
        return relevance_score
    
    async def store_memory(self, memory_type: str, data: Any, key: Optional[str] = None):
        """Store data in the specified memory type"""
        self.metrics["memory_operations"] += 1
        
        if memory_type == "episodic":
            self.memory_store["episodic"].append(data)
            # Keep only last 100 episodic memories
            if len(self.memory_store["episodic"]) > 100:
                self.memory_store["episodic"] = self.memory_store["episodic"][-100:]
        else:
            if key is None:
                key = f"auto_key_{datetime.now().timestamp()}"
            self.memory_store[memory_type][key] = data
    
    async def retrieve_memory(self, memory_type: str, key: Optional[str] = None) -> Any:
        """Retrieve data from the specified memory type"""
        self.metrics["memory_operations"] += 1
        
        if memory_type == "episodic":
            return self.memory_store["episodic"]
        elif key:
            return self.memory_store.get(memory_type, {}).get(key)
        else:
            return self.memory_store.get(memory_type, {})
    
    def get_memory_stats(self) -> Dict[str, Any]:
        """Get memory usage statistics"""
        return {
            "short_term_count": len(self.memory_store.get("short_term", {})),
            "long_term_count": len(self.memory_store.get("long_term", {})),
            "episodic_count": len(self.memory_store.get("episodic", [])),
            "semantic_count": len(self.memory_store.get("semantic", {})),
            "total_operations": self.metrics["memory_operations"]
        }
    
    async def learn_from_experience(self, experience: Dict[str, Any]):
        """Learn from a given experience"""
        self.metrics["learning_sessions"] += 1
        
        learning_entry = {
            "experience": experience,
            "timestamp": datetime.now().isoformat(),
            "learning_type": "experiential"
        }
        
        self.learning_history.append(learning_entry)
        
        # Store in long-term memory
        await self.store_memory("long_term", learning_entry, f"learning_{len(self.learning_history)}")
    
    def get_learning_stats(self) -> Dict[str, Any]:
        """Get learning statistics"""
        return {
            "total_learning_sessions": self.metrics["learning_sessions"],
            "learning_history_count": len(self.learning_history),
            "recent_learning": self.learning_history[-5:] if self.learning_history else []
        }
    
    def get_status(self) -> Dict[str, Any]:
        """Get the current status of the cognitive system"""
        return {
            "status": self.status,
            "is_initialized": self.is_initialized,
            "metrics": self.metrics,
            "memory_stats": self.get_memory_stats(),
            "learning_stats": self.get_learning_stats()
        }
    
    async def health_check(self) -> Dict[str, Any]:
        """Perform health check on the cognitive system"""
        return {
            "status": self.status,
            "is_initialized": self.is_initialized,
            "memory_operations": self.metrics["memory_operations"],
            "reasoning_requests": self.metrics["reasoning_requests"],
            "learning_sessions": self.metrics["learning_sessions"],
            "memory_stats": self.get_memory_stats(),
            "learning_stats": self.get_learning_stats()
        }

    async def shutdown(self):
        """Gracefully shutdown the cognitive system"""
        logger.info("Shutting down Cognitive System...")
        self.status = "shutdown"
        self.is_initialized = False
        logger.info("Cognitive System shutdown complete")