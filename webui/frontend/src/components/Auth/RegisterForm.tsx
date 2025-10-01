import React, { useState } from 'react';
import {
  Box,
  Card,
  CardContent,
  TextField,
  Button,
  Typography,
  Link,
  InputAdornment,
  IconButton,
  CircularProgress,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  SelectChangeEvent,
} from '@mui/material';
import {
  Person as PersonIcon,
  Email as EmailIcon,
  Lock,
  Visibility,
  VisibilityOff,
  AdminPanelSettings,
} from '@mui/icons-material';
import { motion } from 'framer-motion';
import { useForm, Controller } from 'react-hook-form';
import { useAuth } from '../../contexts/AuthContext';

interface RegisterFormData {
  username: string;
  email: string;
  password: string;
  confirmPassword: string;
  role: 'user' | 'developer' | 'admin';
}

interface RegisterFormProps {
  onSwitchToLogin: () => void;
}

const RegisterForm: React.FC<RegisterFormProps> = ({ onSwitchToLogin }) => {
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const { register: registerUser } = useAuth();
  
  const {
    register,
    handleSubmit,
    formState: { errors },
    setError,
    watch,
    control,
  } = useForm<RegisterFormData>({
    defaultValues: {
      role: 'user',
    },
  });

  const password = watch('password');

  const onSubmit = async (data: RegisterFormData) => {
    setIsLoading(true);
    try {
      await registerUser(data.username, data.email, data.password, data.role);
    } catch (error: any) {
      setError('root', {
        type: 'manual',
        message: error.message || 'Registration failed. Please try again.',
      });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -20 }}
      transition={{ duration: 0.3 }}
    >
      <Card
        sx={
          maxWidth: 400,
          mx: 'auto',
          mt: 8,
          bgcolor: 'rgba(26, 26, 46, 0.9)',
          backdropFilter: 'blur(10px)',
          border: '1px solid rgba(255, 255, 255, 0.1)',
        }
      >
        <CardContent sx={{ p: 4 }}>
          <Box textAlign="center" mb={3}>
            <Typography
              variant="h4"
              component="h1"
              sx={
                background: 'linear-gradient(45deg, #00e5ff, #ff4081)',
                backgroundClip: 'text',
                WebkitBackgroundClip: 'text',
                WebkitTextFillColor: 'transparent',
                fontWeight: 'bold',
                mb: 1,
              }
            >
              Join AGI
            </Typography>
            <Typography variant="body1" color="text.secondary">
              Create your account to get started
            </Typography>
          </Box>

          <Box component="form" onSubmit={handleSubmit(onSubmit)}>
            {errors.root && (
              <Typography
                variant="body2"
                color="error"
                sx={{ mb: 2, textAlign: 'center' }}
              >
                {errors.root.message}
              </Typography>
            )}

            <TextField
              fullWidth
              label="Username"
              variant="outlined"
              margin="normal"
              {...register('username', {
                required: 'Username is required',
                minLength: {
                  value: 3,
                  message: 'Username must be at least 3 characters',
                },
                pattern: {
                  value: /^[a-zA-Z0-9_]+$/,
                  message: 'Username can only contain letters, numbers, and underscores',
                },
              })}
              error={!!errors.username}
              helperText={errors.username?.message}
              InputProps={
                startAdornment: (
                  <InputAdornment position="start">
                    <PersonIcon color="primary" />
                  </InputAdornment>
                ),
              }
              sx={
                '& .MuiOutlinedInput-root': {
                  '& fieldset': {
                    borderColor: 'rgba(255, 255, 255, 0.3)',
                  },
                  '&:hover fieldset': {
                    borderColor: 'rgba(0, 229, 255, 0.5)',
                  },
                  '&.Mui-focused fieldset': {
                    borderColor: '#00e5ff',
                  },
                },
              }
            />

            <TextField
              fullWidth
              label="Email"
              type="email"
              variant="outlined"
              margin="normal"
              {...register('email', {
                required: 'Email is required',
                pattern: {
                  value: /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i,
                  message: 'Please enter a valid email address',
                },
              })}
              error={!!errors.email}
              helperText={errors.email?.message}
              InputProps={
                startAdornment: (
                  <InputAdornment position="start">
                    <EmailIcon color="primary" />
                  </InputAdornment>
                ),
              }
              sx={
                '& .MuiOutlinedInput-root': {
                  '& fieldset': {
                    borderColor: 'rgba(255, 255, 255, 0.3)',
                  },
                  '&:hover fieldset': {
                    borderColor: 'rgba(0, 229, 255, 0.5)',
                  },
                  '&.Mui-focused fieldset': {
                    borderColor: '#00e5ff',
                  },
                },
              }
            />

            <FormControl
              fullWidth
              margin="normal"
              sx={
                '& .MuiOutlinedInput-root': {
                  '& fieldset': {
                    borderColor: 'rgba(255, 255, 255, 0.3)',
                  },
                  '&:hover fieldset': {
                    borderColor: 'rgba(0, 229, 255, 0.5)',
                  },
                  '&.Mui-focused fieldset': {
                    borderColor: '#00e5ff',
                  },
                },
              }
            >
              <InputLabel>Role</InputLabel>
              <Controller
                name="role"
                control={control}
                render={({ field }) => (
                  <Select
                    {...field}
                    label="Role"
                    startAdornment={
                      <InputAdornment position="start">
                        <AdminPanelSettings color="primary" />
                      </InputAdornment>
                    }
                  >
                    <MenuItem value="user">User</MenuItem>
                    <MenuItem value="developer">Developer</MenuItem>
                    <MenuItem value="admin">Admin</MenuItem>
                  </Select>
                )}
              />
            </FormControl>

            <TextField
              fullWidth
              label="Password"
              type={showPassword ? 'text' : 'password'}
              variant="outlined"
              margin="normal"
              {...register('password', {
                required: 'Password is required',
                minLength: {
                  value: 8,
                  message: 'Password must be at least 8 characters',
                },
                pattern: {
                  value: /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)/,
                  message: 'Password must contain at least one uppercase letter, one lowercase letter, and one number',
                },
              })}
              error={!!errors.password}
              helperText={errors.password?.message}
              InputProps={
                startAdornment: (
                  <InputAdornment position="start">
                    <Lock color="primary" />
                  </InputAdornment>
                ),
                endAdornment: (
                  <InputAdornment position="end">
                    <IconButton
                      onClick={() => setShowPassword(!showPassword)}
                      edge="end"
                    >
                      {showPassword ? <VisibilityOff /> : <Visibility />}
                    </IconButton>
                  </InputAdornment>
                ),
              }
              sx={
                '& .MuiOutlinedInput-root': {
                  '& fieldset': {
                    borderColor: 'rgba(255, 255, 255, 0.3)',
                  },
                  '&:hover fieldset': {
                    borderColor: 'rgba(0, 229, 255, 0.5)',
                  },
                  '&.Mui-focused fieldset': {
                    borderColor: '#00e5ff',
                  },
                },
              }
            />

            <TextField
              fullWidth
              label="Confirm Password"
              type={showConfirmPassword ? 'text' : 'password'}
              variant="outlined"
              margin="normal"
              {...register('confirmPassword', {
                required: 'Please confirm your password',
                validate: (value) =>
                  value === password || 'Passwords do not match',
              })}
              error={!!errors.confirmPassword}
              helperText={errors.confirmPassword?.message}
              InputProps={
                startAdornment: (
                  <InputAdornment position="start">
                    <Lock color="primary" />
                  </InputAdornment>
                ),
                endAdornment: (
                  <InputAdornment position="end">
                    <IconButton
                      onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                      edge="end"
                    >
                      {showConfirmPassword ? <VisibilityOff /> : <Visibility />}
                    </IconButton>
                  </InputAdornment>
                ),
              }
              sx={
                '& .MuiOutlinedInput-root': {
                  '& fieldset': {
                    borderColor: 'rgba(255, 255, 255, 0.3)',
                  },
                  '&:hover fieldset': {
                    borderColor: 'rgba(0, 229, 255, 0.5)',
                  },
                  '&.Mui-focused fieldset': {
                    borderColor: '#00e5ff',
                  },
                },
              }
            />

            <Button
              type="submit"
              fullWidth
              variant="contained"
              disabled={isLoading}
              sx={
                mt: 3,
                mb: 2,
                py: 1.5,
                background: 'linear-gradient(45deg, #00e5ff, #ff4081)',
                '&:hover': {
                  background: 'linear-gradient(45deg, #00b2cc, #c60055)',
                },
                '&:disabled': {
                  background: 'rgba(255, 255, 255, 0.1)',
                },
              }
            >
              {isLoading ? (
                <CircularProgress size={24} color="inherit" />
              ) : (
                'Create Account'
              )}
            </Button>

            <Box textAlign="center">
              <Typography variant="body2" color="text.secondary">
                Already have an account?{' '}
                <Link
                  component="button"
                  type="button"
                  onClick={onSwitchToLogin}
                  sx={
                    color: '#00e5ff',
                    textDecoration: 'none',
                    '&:hover': {
                      textDecoration: 'underline',
                    },
                  }
                >
                  Sign in here
                </Link>
              </Typography>
            </Box>
          </Box>
        </CardContent>
      </Card>
    </motion.div>
  );
};

export default RegisterForm;