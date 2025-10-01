import React from 'react';
import {
  Drawer,
  List,
  ListItem,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  Typography,
  Box,
  Divider,
  Chip,
  useTheme,
  alpha,
} from '@mui/material';
import {
  Chat,
  Dashboard,
  Memory,
  Psychology,
  School,
  Evolution,
  MonitorHeart,
  AdminPanelSettings,
  Circle,
} from '@mui/icons-material';
import { motion } from 'framer-motion';
import { useLocation, useNavigate } from 'react-router-dom';
import { useAGI } from '../../contexts/AGIContext';
import { useAGIStore } from '../../store/agiStore';

interface SidebarProps {
  open: boolean;
  onClose: () => void;
}

const drawerWidth = 280;

const menuItems = [
  {
    text: 'Chat',
    icon: <Chat />,
    path: '/chat',
    description: 'Interact with AGI',
  },
  {
    text: 'Dashboard',
    icon: <Dashboard />,
    path: '/dashboard',
    description: 'System Overview',
  },
  {
    text: 'Memory',
    icon: <Memory />,
    path: '/memory',
    description: 'Knowledge Base',
  },
  {
    text: 'Reasoning',
    icon: <Psychology />,
    path: '/reasoning',
    description: 'Cognitive Analysis',
  },
  {
    text: 'Learning',
    icon: <School />,
    path: '/learning',
    description: 'Adaptive Intelligence',
  },
  {
    text: 'Evolution',
    icon: <Evolution />,
    path: '/evolution',
    description: 'System Evolution',
  },
  {
    text: 'System',
    icon: <MonitorHeart />,
    path: '/system',
    description: 'Health & Monitoring',
  },
  {
    text: 'Admin',
    icon: <AdminPanelSettings />,
    path: '/admin',
    description: 'Administration',
  },
];

const Sidebar: React.FC<SidebarProps> = ({ open, onClose }) => {
  const theme = useTheme();
  const location = useLocation();
  const navigate = useNavigate();
  const { isConnected } = useAGI();
  const { systemStatus } = useAGIStore();

  const handleNavigation = (path: string) => {
    navigate(path);
    onClose();
  };

  const getConnectionStatusColor = () => {
    if (!isConnected) return theme.palette.error.main;
    return theme.palette.success.main;
  };

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.1,
      },
    },
  };

  const itemVariants = {
    hidden: { x: -20, opacity: 0 },
    visible: {
      x: 0,
      opacity: 1,
      transition: {
        type: 'spring',
        stiffness: 300,
        damping: 24,
      },
    },
  };

  const drawerContent = (
    <Box
      sx={{
        width: drawerWidth,
        height: '100%',
        background: `linear-gradient(180deg, 
          ${alpha(theme.palette.background.paper, 0.95)} 0%, 
          ${alpha(theme.palette.background.default, 0.95)} 100%)`,
        backdropFilter: 'blur(20px)',
        borderRight: `1px solid ${alpha(theme.palette.divider, 0.1)}`,
      }}
    >
      {/* Header */}
      <Box
        sx={{
          p: 3,
          pt: 10, // Account for AppBar height
          borderBottom: `1px solid ${alpha(theme.palette.divider, 0.1)}`,
        }}
      >
        <Typography
          variant="h5"
          sx={{
            fontWeight: 700,
            background: `linear-gradient(45deg, ${theme.palette.primary.main}, ${theme.palette.secondary.main})`,
            backgroundClip: 'text',
            WebkitBackgroundClip: 'text',
            WebkitTextFillColor: 'transparent',
            mb: 1,
          }}
        >
          AGI System
        </Typography>
        
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
          <Circle
            sx={{
              fontSize: 8,
              color: getConnectionStatusColor(),
            }}
          />
          <Typography
            variant="caption"
            sx={{
              color: 'text.secondary',
              fontWeight: 500,
            }}
          >
            {isConnected ? 'Connected' : 'Disconnected'}
          </Typography>
          {systemStatus?.status && (
            <Chip
              label={systemStatus.status}
              size="small"
              sx={{
                height: 20,
                fontSize: '0.7rem',
                backgroundColor: alpha(
                  systemStatus.status === 'healthy'
                    ? theme.palette.success.main
                    : systemStatus.status === 'warning'
                    ? theme.palette.warning.main
                    : theme.palette.error.main,
                  0.1
                ),
                color:
                  systemStatus.status === 'healthy'
                    ? theme.palette.success.main
                    : systemStatus.status === 'warning'
                    ? theme.palette.warning.main
                    : theme.palette.error.main,
              }}
            />
          )}
        </Box>
      </Box>

      {/* Navigation */}
      <Box sx={{ flex: 1, overflow: 'auto' }}>
        <motion.div
          variants={containerVariants}
          initial="hidden"
          animate="visible"
        >
          <List sx={{ p: 2 }}>
            {menuItems.map((item, index) => {
              const isActive = location.pathname === item.path;
              
              return (
                <motion.div key={item.path} variants={itemVariants}>
                  <ListItem
                    disablePadding
                    sx={{
                      mb: 1,
                      borderRadius: 2,
                      overflow: 'hidden',
                    }}
                  >
                    <ListItemButton
                      onClick={() => handleNavigation(item.path)}
                      sx={{
                        borderRadius: 2,
                        py: 1.5,
                        px: 2,
                        backgroundColor: isActive
                          ? alpha(theme.palette.primary.main, 0.1)
                          : 'transparent',
                        border: isActive
                          ? `1px solid ${alpha(theme.palette.primary.main, 0.3)}`
                          : '1px solid transparent',
                        '&:hover': {
                          backgroundColor: alpha(theme.palette.primary.main, 0.05),
                          border: `1px solid ${alpha(theme.palette.primary.main, 0.2)}`,
                        },
                        transition: 'all 0.2s ease-in-out',
                      }}
                    >
                      <ListItemIcon
                        sx={{
                          color: isActive
                            ? theme.palette.primary.main
                            : theme.palette.text.secondary,
                          minWidth: 40,
                          transition: 'color 0.2s ease-in-out',
                        }}
                      >
                        {item.icon}
                      </ListItemIcon>
                      <ListItemText
                        primary={
                          <Typography
                            variant="body1"
                            sx={{
                              fontWeight: isActive ? 600 : 500,
                              color: isActive
                                ? theme.palette.primary.main
                                : theme.palette.text.primary,
                              transition: 'all 0.2s ease-in-out',
                            }}
                          >
                            {item.text}
                          </Typography>
                        }
                        secondary={
                          <Typography
                            variant="caption"
                            sx={{
                              color: theme.palette.text.secondary,
                              fontSize: '0.7rem',
                            }}
                          >
                            {item.description}
                          </Typography>
                        }
                      />
                    </ListItemButton>
                  </ListItem>
                </motion.div>
              );
            })}
          </List>
        </motion.div>
      </Box>

      {/* Footer */}
      <Box
        sx={
          p: 2,
          borderTop: `1px solid ${alpha(theme.palette.divider, 0.1)}`,
        }
      >
        <Typography
          variant="caption"
          sx={{
            color: 'text.secondary',
            display: 'block',
            textAlign: 'center',
          }}
        >
          Atulya Tantra AGI v1.0.0
        </Typography>
        <Typography
          variant="caption"
          sx={{
            color: 'text.secondary',
            display: 'block',
            textAlign: 'center',
            mt: 0.5,
          }}
        >
          © 2024 Atulya AI
        </Typography>
      </Box>
    </Box>
  );

  return (
    <Drawer
      variant="temporary"
      open={open}
      onClose={onClose}
      ModalProps={{
        keepMounted: true, // Better open performance on mobile.
      }}
      sx={{
        display: { xs: 'block', sm: 'none' },
        '& .MuiDrawer-paper': {
          boxSizing: 'border-box',
          width: drawerWidth,
          backgroundColor: 'transparent',
          border: 'none',
        },
      }}
    >
      {drawerContent}
    </Drawer>
  );
};

export default Sidebar;