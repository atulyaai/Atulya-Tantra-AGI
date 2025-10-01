# Atulya Tantra AGI 🧠🤖

## Advanced Artificial General Intelligence System

Atulya Tantra AGI is an advanced AI system featuring voice-first interactions, intelligent automation, and multi-modal capabilities. Built with modern technologies and designed for scalability.

## 🚀 Current Features (v0.1.0)

### ✅ Implemented
- **FastAPI Backend**: RESTful API with authentication and authorization
- **React Frontend**: Modern web interface with Material-UI
- **Ollama Integration**: Local LLM support with llama3.2:1b model
- **Chat Interface**: Real-time conversation capabilities
- **Cognitive System**: Advanced message processing and reasoning
- **Memory System**: Episodic and semantic memory storage
- **Metrics & Monitoring**: System performance tracking

### 🔄 In Development
- **Audio Processing**: Speech-to-Text and Text-to-Speech
- **Vision Capabilities**: Image and video processing
- **Agent Workflows**: LangGraph-based automation
- **Real-time Communication**: WebSocket support

## 📋 Project Structure

```
Atulya-Tantra-AGI/
├── Models/                     # AI Models and Integration
│   ├── ollama/                # Ollama client and configuration
│   └── langraph/              # LangGraph agent workflows
├── webui/                     # Web Application
│   ├── backend/               # FastAPI Backend
│   │   ├── routes/           # API endpoints
│   │   ├── services/         # Business logic
│   │   ├── models/           # Data models
│   │   └── utils/            # Utilities
│   └── frontend/             # React Frontend
│       ├── src/              # Source code
│       ├── public/           # Static assets
│       └── package.json      # Dependencies
├── config/                    # Configuration files
├── requirements.txt           # Python dependencies
├── README.md                  # This file
└── ROADMAP.md                # Development roadmap
```

## 🛠️ Installation

### Prerequisites
- Python 3.8+
- Node.js 16+
- Ollama (for local LLM support)

### Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/atulyaai/Atulya-Tantra-AGI.git
   cd Atulya-Tantra-AGI
   ```

2. **Install Ollama**
   ```bash
   curl -fsSL https://ollama.ai/install.sh | sh
   ollama pull llama3.2:1b
   ```

3. **Setup Backend**
   ```bash
   cd webui/backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r ../../requirements.txt
   python main.py
   ```

4. **Setup Frontend**
   ```bash
   cd webui/frontend
   npm install
   npm start
   ```

5. **Access the Application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

## 🎯 Usage

### Chat Interface
1. Open the web interface at http://localhost:3000
2. Register a new account or login
3. Start chatting with the AI system
4. The system uses the local Ollama LLM for responses

### API Usage
```python
import requests

# Send a message to the AI
response = requests.post("http://localhost:8000/api/message", 
    json={"message": "Hello, how are you?"},
    headers={"Authorization": "Bearer YOUR_TOKEN"}
)
print(response.json())
```

## 🏗️ Architecture

### Backend (FastAPI)
- **Authentication**: JWT-based user authentication
- **Chat Routes**: Message processing and response generation
- **Cognitive System**: Advanced reasoning and memory
- **Model Integration**: Ollama LLM integration
- **Metrics**: Performance monitoring

### Frontend (React)
- **Material-UI**: Modern component library
- **Chat Interface**: Real-time messaging
- **Authentication**: Login/register forms
- **Responsive Design**: Mobile-friendly interface

### AI Models
- **Ollama**: Local LLM hosting (llama3.2:1b)
- **LangGraph**: Agent workflow orchestration (planned)
- **Cognitive Processing**: Intent analysis, entity extraction

## 📊 Development Status

See [ROADMAP.md](ROADMAP.md) for detailed development plans and milestones.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

This is an experimental AI system. Use responsibly and in accordance with AI safety guidelines.

---

**"The future is not something we enter. The future is something we create."** - Leonard I. Sweet