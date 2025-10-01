import React, { useState, useRef, useEffect } from 'react';
import {
  Box,
  Paper,
  Typography,
  TextField,
  IconButton,
  Avatar,
  Chip,
  Divider,
  Button,
  Tooltip,
  CircularProgress,
} from '@mui/material';
import {
  Send as SendIcon,
  Psychology as PsychologyIcon,
  Memory as MemoryIcon,
  Clear as ClearIcon,
  SmartToy as SmartToyIcon,
} from '@mui/icons-material';
import { motion, AnimatePresence } from 'framer-motion';
import { useAGIStore } from '../../store/agiStore';
import { useAGI } from '../../contexts/AGIContext';
import { Message } from '../../types/api';

interface MessageBubbleProps {
  message: Message;
  isUser: boolean;
}

const MessageBubble: React.FC<MessageBubbleProps> = ({ message, isUser }) => {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -20 }}
      transition={{ duration: 0.3 }}
    >
      <Box
        sx={{
          display: 'flex',
          justifyContent: isUser ? 'flex-end' : 'flex-start',
          mb: 2,
        }}
      >
        <Box
          sx={{
            maxWidth: '70%',
            display: 'flex',
            flexDirection: isUser ? 'row-reverse' : 'row',
            alignItems: 'flex-start',
            gap: 1,
          }}
        >
          <Avatar
            sx={{
              bgcolor: isUser ? '#ff4081' : '#00e5ff',
              width: 32,
              height: 32,
            }}
          >
            {isUser ? 'U' : <SmartToyIcon />}
          </Avatar>
          
          <Paper
            elevation={2}
            sx={{
              p: 2,
              bgcolor: isUser ? '#1a1a2e' : '#16213e',
              border: `1px solid ${isUser ? '#ff4081' : '#00e5ff'}`,
              borderRadius: 2,
            }}
          >
            <Typography
              variant="body1"
              sx={{
                color: 'white',
                whiteSpace: 'pre-wrap',
                wordBreak: 'break-word',
              }}
            >
              {message.content}
            </Typography>
            
            {!isUser && message.metadata && (
              <Box sx={{ mt: 1, display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
                {message.metadata.reasoning_type && (
                  <Chip
                    icon={<PsychologyIcon />}
                    label={message.metadata.reasoning_type}
                    size="small"
                    sx={{
                      bgcolor: 'rgba(0, 229, 255, 0.1)',
                      color: '#00e5ff',
                      border: '1px solid rgba(0, 229, 255, 0.3)',
                    }}
                  />
                )}
                {message.metadata.memory_access && (
                  <Chip
                    icon={<MemoryIcon />}
                    label="Memory Access"
                    size="small"
                    sx={{
                      bgcolor: 'rgba(255, 64, 129, 0.1)',
                      color: '#ff4081',
                      border: '1px solid rgba(255, 64, 129, 0.3)',
                    }}
                  />
                )}
                {message.metadata.confidence && (
                  <Chip
                    label={`${Math.round(message.metadata.confidence * 100)}% confident`}
                    size="small"
                    sx={{
                      bgcolor: 'rgba(76, 175, 80, 0.1)',
                      color: '#4caf50',
                      border: '1px solid rgba(76, 175, 80, 0.3)',
                    }}
                  />
                )}
              </Box>
            )}
            
            <Typography
              variant="caption"
              sx={{
                color: 'rgba(255, 255, 255, 0.6)',
                display: 'block',
                mt: 1,
              }}
            >
              {new Date(message.timestamp).toLocaleTimeString()}
            </Typography>
          </Paper>
        </Box>
      </Box>
    </motion.div>
  );
};

const TypingIndicator: React.FC = () => {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -20 }}
      transition={{ duration: 0.3 }}
    >
      <Box
        sx={{
          display: 'flex',
          justifyContent: 'flex-start',
          mb: 2,
        }}
      >
        <Box
          sx={{
            display: 'flex',
            alignItems: 'flex-start',
            gap: 1,
          }}
        >
          <Avatar
            sx={{
              bgcolor: '#00e5ff',
              width: 32,
              height: 32,
            }}
          >
            <SmartToyIcon />
          </Avatar>
          
          <Paper
            elevation={2}
            sx={{
              p: 2,
              bgcolor: '#16213e',
              border: '1px solid #00e5ff',
              borderRadius: 2,
              display: 'flex',
              alignItems: 'center',
              gap: 1,
            }}
          >
            <CircularProgress size={16} sx={{ color: '#00e5ff' }} />
            <Typography variant="body2" sx={{ color: 'rgba(255, 255, 255, 0.7)' }}>
              AGI is thinking...
            </Typography>
          </Paper>
        </Box>
      </Box>
    </motion.div>
  );
};

const ChatInterface: React.FC = () => {
  const [inputMessage, setInputMessage] = useState('');
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const { messages, isTyping, clearMessages } = useAGIStore();
  const { sendMessage, isConnected } = useAGI();

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isTyping]);

  const handleSendMessage = async () => {
    if (!inputMessage.trim() || !isConnected) return;

    const messageContent = inputMessage.trim();
    setInputMessage('');

    try {
      await sendMessage(messageContent);
    } catch (error) {
      console.error('Failed to send message:', error);
    }
  };

  const handleKeyPress = (event: React.KeyboardEvent) => {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault();
      handleSendMessage();
    }
  };

  const handleClearChat = () => {
    clearMessages();
  };

  return (
    <Box
      sx={
        height: '100%',
        display: 'flex',
        flexDirection: 'column',
        bgcolor: '#0f0f23',
      }
    >
      {/* Header */}
      <Paper
        elevation={2}
        sx={
          p: 2,
          bgcolor: '#1a1a2e',
          borderBottom: '1px solid rgba(255, 255, 255, 0.1)',
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
        }
      >
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
          <Avatar sx={{ bgcolor: '#00e5ff' }}>
            <SmartToyIcon />
          </Avatar>
          <Box>
            <Typography variant="h6" sx={{ color: 'white' }}>
              AGI Assistant
            </Typography>
            <Typography variant="caption" sx={{ color: 'rgba(255, 255, 255, 0.6)' }}>
              {isConnected ? 'Connected' : 'Disconnected'}
            </Typography>
          </Box>
        </Box>
        
        <Tooltip title="Clear Chat">
          <IconButton
            onClick={handleClearChat}
            sx={{
              color: '#ff4081',
              '&:hover': {
                bgcolor: 'rgba(255, 64, 129, 0.1)',
              },
            }}
          >
            <ClearIcon />
          </IconButton>
        </Tooltip>
      </Paper>

      {/* Messages */}
      <Box
        sx={
          flex: 1,
          overflow: 'auto',
          p: 2,
          '&::-webkit-scrollbar': {
            width: '8px',
          },
          '&::-webkit-scrollbar-track': {
            bgcolor: 'rgba(255, 255, 255, 0.1)',
            borderRadius: '4px',
          },
          '&::-webkit-scrollbar-thumb': {
            bgcolor: 'rgba(0, 229, 255, 0.5)',
            borderRadius: '4px',
            '&:hover': {
              bgcolor: 'rgba(0, 229, 255, 0.7)',
            },
          },
        }
      >
        <AnimatePresence>
          {messages.length === 0 ? (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ duration: 0.5 }}
            >
              <Box
                sx={
                  display: 'flex',
                  flexDirection: 'column',
                  alignItems: 'center',
                  justifyContent: 'center',
                  height: '100%',
                  textAlign: 'center',
                  color: 'rgba(255, 255, 255, 0.6)',
                }
              >
                <SmartToyIcon sx={{ fontSize: 64, mb: 2, color: '#00e5ff' }} />
                <Typography variant="h5" sx={{ mb: 1 }}>
                  Welcome to AGI Chat
                </Typography>
                <Typography variant="body1">
                  Start a conversation with the AGI assistant
                </Typography>
              </Box>
            </motion.div>
          ) : (
            messages.map((message) => (
              <MessageBubble
                key={message.id}
                message={message}
                isUser={message.role === 'user'}
              />
            ))
          )}
          
          {isTyping && <TypingIndicator />}
        </AnimatePresence>
        
        <div ref={messagesEndRef} />
      </Box>

      {/* Input */}
      <Paper
        elevation={2}
        sx={
          p: 2,
          bgcolor: '#1a1a2e',
          borderTop: '1px solid rgba(255, 255, 255, 0.1)',
        }
      >
        <Box sx={{ display: 'flex', gap: 1, alignItems: 'flex-end' }}>
          <TextField
            fullWidth
            multiline
            maxRows={4}
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Type your message..."
            disabled={!isConnected}
            variant="outlined"
            sx={
              '& .MuiOutlinedInput-root': {
                bgcolor: '#0f0f23',
                color: 'white',
                '& fieldset': {
                  borderColor: 'rgba(255, 255, 255, 0.3)',
                },
                '&:hover fieldset': {
                  borderColor: 'rgba(0, 229, 255, 0.5)',
                },
                '&.Mui-focused fieldset': {
                  borderColor: '#00e5ff',
                },
                '&.Mui-disabled': {
                  bgcolor: 'rgba(255, 255, 255, 0.05)',
                },
              },
              '& .MuiInputBase-input::placeholder': {
                color: 'rgba(255, 255, 255, 0.5)',
              },
            }
          />
          
          <IconButton
            onClick={handleSendMessage}
            disabled={!inputMessage.trim() || !isConnected}
            sx={
              bgcolor: '#00e5ff',
              color: 'white',
              '&:hover': {
                bgcolor: '#00b2cc',
              },
              '&:disabled': {
                bgcolor: 'rgba(255, 255, 255, 0.1)',
                color: 'rgba(255, 255, 255, 0.3)',
              },
            }
          >
            <SendIcon />
          </IconButton>
        </Box>
      </Paper>
    </Box>
  );
};

export default ChatInterface;