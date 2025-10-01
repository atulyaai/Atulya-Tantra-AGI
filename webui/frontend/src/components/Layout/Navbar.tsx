import React, { useState } from 'react';
import {
  AppBar,
  Toolbar,
  Typography,
  Box,
  IconButton,
  Avatar,
  Menu,
  MenuItem,
  Chip,
  Badge,
  Tooltip,
  Button,
  useTheme,
  alpha,
} from '@mui/material';
import {
  Menu as MenuIcon,
  AccountCircle,
  Settings,
  Logout,
  Notifications,
  WifiOff,
  Wifi,
  Circle,
  Psychology,
  AdminPanelSettings,
  DeveloperMode,
} from '@mui/icons-material';
import { motion, AnimatePresence } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';
import { useAGI } from '../../contexts/AGIContext';
import { useAGIStore } from '../../store/agiStore';

interface NavbarProps {
  onMenuClick: () => void;
}

const Navbar: React.FC<NavbarProps> = ({ onMenuClick }) => {
  const theme = useTheme();
  const navigate = useNavigate();
  const { user, logout, hasRole } = useAuth();
  const { isConnected } = useAGI();
  const { systemStatus, isTyping } = useAGIStore();
  
  const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null);
  const [notificationAnchor, setNotificationAnchor] = useState<null | HTMLElement>(null);

  const handleProfileMenuOpen = (event: React.MouseEvent<HTMLElement>) => {
    setAnchorEl(event.currentTarget);
  };

  const handleMenuClose = () => {
    setAnchorEl(null);
  };

  const handleNotificationClick = (event: React.MouseEvent<HTMLElement>) => {
    setNotificationAnchor(event.currentTarget);
  };

  const handleNotificationClose = () => {
    setNotificationAnchor(null);
  };

  const handleLogout = async () => {
    await logout();
    handleMenuClose();
    navigate('/auth');
  };

  const getStatusColor = () => {
    if (!isConnected) return theme.palette.error.main;
    switch (systemStatus?.status) {
      case 'healthy':
        return theme.palette.success.main;
      case 'warning':
        return theme.palette.warning.main;
      case 'error':
        return theme.palette.error.main;
      default:
        return theme.palette.grey[500];
    }
  };

  const getStatusText = () => {
    if (!isConnected) return 'Offline';
    switch (systemStatus?.status) {
      case 'healthy':
        return 'Healthy';
      case 'warning':
        return 'Warning';
      case 'error':
        return 'Error';
      default:
        return 'Unknown';
    }
  };

  const getConnectionStatus = () => {
    if (isConnected) {
      return {
        icon: <Wifi sx={{ fontSize: 16 }} />,
        text: 'Online',
        color: theme.palette.success.main,
      };
    } else {
      return {
        icon: <WifiOff sx={{ fontSize: 16 }} />,
        text: 'Offline',
        color: theme.palette.error.main,
      };
    }
  };

  const connectionStatus = getConnectionStatus();

  return (
    <AppBar
      position="fixed"
      sx={{
        zIndex: theme.zIndex.drawer + 1,
        backgroundColor: alpha(theme.palette.background.paper, 0.8),
        backdropFilter: 'blur(20px)',
        borderBottom: `1px solid ${alpha(theme.palette.divider, 0.1)}`,
        boxShadow: 'none',
      }}
    >
      <Toolbar sx={{ justifyContent: 'space-between' }}>
        {/* Left Section */}
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
          <IconButton
            edge="start"
            color="inherit"
            aria-label="menu"
            onClick={onMenuClick}
            sx={{
              color: theme.palette.text.primary,
              '&:hover': {
                backgroundColor: alpha(theme.palette.primary.main, 0.1),
              },
            }}
          >
            <MenuIcon />
          </IconButton>
          
          <Typography
            variant="h6"
            component="div"
            sx={{
              fontWeight: 700,
              background: `linear-gradient(45deg, ${theme.palette.primary.main}, ${theme.palette.secondary.main})`,
              backgroundClip: 'text',
              WebkitBackgroundClip: 'text',
              WebkitTextFillColor: 'transparent',
            }}
          >
            Atulya Tantra AGI
          </Typography>

          {/* System Status */}
          <Chip
            icon={<Circle sx={{ fontSize: 12 }} />}
            label={getStatusText()}
            size="small"
            sx={{
              backgroundColor: alpha(getStatusColor(), 0.1),
              color: getStatusColor(),
              border: `1px solid ${alpha(getStatusColor(), 0.3)}`,
              '& .MuiChip-icon': {
                color: getStatusColor(),
              },
            }}
          />

          {/* Connection Status */}
          <Chip
            icon={connectionStatus.icon}
            label={connectionStatus.text}
            size="small"
            sx={{
              backgroundColor: alpha(connectionStatus.color, 0.1),
              color: connectionStatus.color,
              border: `1px solid ${alpha(connectionStatus.color, 0.3)}`,
              '& .MuiChip-icon': {
                color: connectionStatus.color,
              },
            }}
          />

          {/* AGI Typing Indicator */}
          <AnimatePresence>
            {isTyping && (
              <motion.div
                initial={{ opacity: 0, scale: 0.8 }}
                animate={{ opacity: 1, scale: 1 }}
                exit={{ opacity: 0, scale: 0.8 }}
                transition={{ duration: 0.2 }}
              >
                <Chip
                  icon={<Psychology sx={{ fontSize: 16 }} />}
                  label="AGI is thinking..."
                  size="small"
                  sx={{
                    backgroundColor: alpha(theme.palette.primary.main, 0.1),
                    color: theme.palette.primary.main,
                    border: `1px solid ${alpha(theme.palette.primary.main, 0.3)}`,
                    '& .MuiChip-icon': {
                      color: theme.palette.primary.main,
                      animation: 'pulse 1.5s ease-in-out infinite',
                    },
                    '@keyframes pulse': {
                      '0%': {
                        opacity: 1,
                      },
                      '50%': {
                        opacity: 0.5,
                      },
                      '100%': {
                        opacity: 1,
                      },
                    },
                  }}
                />
              </motion.div>
            )}
          </AnimatePresence>
        </Box>

        {/* Right Section */}
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
          {/* Notifications */}
          <Tooltip title="Notifications">
            <IconButton
              color="inherit"
              onClick={handleNotificationClick}
              sx={{
                color: theme.palette.text.primary,
                '&:hover': {
                  backgroundColor: alpha(theme.palette.primary.main, 0.1),
                },
              }}
            >
              <Badge badgeContent={3} color="error">
                <Notifications />
              </Badge>
            </IconButton>
          </Tooltip>

          {/* User Authentication */}
          {user ? (
            <>
              {/* Role Badges */}
              {hasRole('admin') && (
                <Chip
                  icon={<AdminPanelSettings sx={{ fontSize: 16 }} />}
                  label="Admin"
                  size="small"
                  color="error"
                  variant="outlined"
                />
              )}
              {hasRole('developer') && (
                <Chip
                  icon={<DeveloperMode sx={{ fontSize: 16 }} />}
                  label="Dev"
                  size="small"
                  color="info"
                  variant="outlined"
                />
              )}

              {/* User Menu */}
              <Tooltip title="Account settings">
                <IconButton
                  onClick={handleProfileMenuOpen}
                  sx={{
                    color: theme.palette.text.primary,
                    '&:hover': {
                      backgroundColor: alpha(theme.palette.primary.main, 0.1),
                    },
                  }}
                >
                  <Avatar
                    sx={{
                      width: 32,
                      height: 32,
                      backgroundColor: theme.palette.primary.main,
                      fontSize: 14,
                    }}
                  >
                    {user.username?.charAt(0).toUpperCase()}
                  </Avatar>
                </IconButton>
              </Tooltip>
            </>
          ) : (
            <Button
              variant="contained"
              onClick={() => navigate('/auth')}
              sx={{
                borderRadius: 2,
                textTransform: 'none',
                fontWeight: 600,
              }}
            >
              Sign In
            </Button>
          )}
        </Box>
      </Toolbar>

      {/* User Menu */}
      <Menu
        anchorEl={anchorEl}
        open={Boolean(anchorEl)}
        onClose={handleMenuClose}
        onClick={handleMenuClose}
        PaperProps={{
          elevation: 0,
          sx: {
            overflow: 'visible',
            filter: 'drop-shadow(0px 2px 8px rgba(0,0,0,0.32))',
            mt: 1.5,
            backgroundColor: alpha(theme.palette.background.paper, 0.9),
            backdropFilter: 'blur(20px)',
            border: `1px solid ${alpha(theme.palette.divider, 0.1)}`,
            '& .MuiAvatar-root': {
              width: 32,
              height: 32,
              ml: -0.5,
              mr: 1,
            },
            '&:before': {
              content: '""',
              display: 'block',
              position: 'absolute',
              top: 0,
              right: 14,
              width: 10,
              height: 10,
              bgcolor: 'background.paper',
              transform: 'translateY(-50%) rotate(45deg)',
              zIndex: 0,
            },
          },
        }}
        transformOrigin={{ horizontal: 'right', vertical: 'top' }}
        anchorOrigin={{ horizontal: 'right', vertical: 'bottom' }}
      >
        <MenuItem onClick={() => navigate('/profile')}>
          <AccountCircle sx={{ mr: 2 }} />
          Profile
        </MenuItem>
        <MenuItem onClick={() => navigate('/settings')}>
          <Settings sx={{ mr: 2 }} />
          Settings
        </MenuItem>
        <MenuItem onClick={handleLogout}>
          <Logout sx={{ mr: 2 }} />
          Logout
        </MenuItem>
      </Menu>

      {/* Notifications Menu */}
      <Menu
        anchorEl={notificationAnchor}
        open={Boolean(notificationAnchor)}
        onClose={handleNotificationClose}
        PaperProps={{
          elevation: 0,
          sx: {
            overflow: 'visible',
            filter: 'drop-shadow(0px 2px 8px rgba(0,0,0,0.32))',
            mt: 1.5,
            backgroundColor: alpha(theme.palette.background.paper, 0.9),
            backdropFilter: 'blur(20px)',
            border: `1px solid ${alpha(theme.palette.divider, 0.1)}`,
            minWidth: 300,
          },
        }}
        transformOrigin={{ horizontal: 'right', vertical: 'top' }}
        anchorOrigin={{ horizontal: 'right', vertical: 'bottom' }}
      >
        <MenuItem>
          <Box>
            <Typography variant="body2" sx={{ fontWeight: 600 }}>
              System Update Available
            </Typography>
            <Typography variant="caption" sx={{ color: 'text.secondary' }}>
              2 minutes ago
            </Typography>
          </Box>
        </MenuItem>
        <MenuItem>
          <Box>
            <Typography variant="body2" sx={{ fontWeight: 600 }}>
              Memory Optimization Complete
            </Typography>
            <Typography variant="caption" sx={{ color: 'text.secondary' }}>
              15 minutes ago
            </Typography>
          </Box>
        </MenuItem>
        <MenuItem>
          <Box>
            <Typography variant="body2" sx={{ fontWeight: 600 }}>
              Evolution Cycle Started
            </Typography>
            <Typography variant="caption" sx={{ color: 'text.secondary' }}>
              1 hour ago
            </Typography>
          </Box>
        </MenuItem>
      </Menu>
    </AppBar>
  );
};

export default Navbar;