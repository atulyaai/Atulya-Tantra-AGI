import React, { useEffect, useState } from 'react';
import {
  Box,
  Grid,
  Card,
  CardContent,
  Typography,
  LinearProgress,
  Chip,
  IconButton,
  Paper,
  useTheme,
  alpha,
} from '@mui/material';
import {
  Memory,
  Psychology,
  School,
  Evolution as EvolutionIcon,
  MonitorHeart,
  Refresh as RefreshIcon,
  TrendingUp,
  Storage,
  Speed,
} from '@mui/icons-material';
import { motion } from 'framer-motion';
import {
  LineChart,
  Line,
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from 'recharts';
import { useAGIStore } from '../../store/agiStore';
import { agiApi } from '../../api/api';

const Dashboard: React.FC = () => {
  const theme = useTheme();
  const {
    systemStatus,
    memoryStats,
    learningStats,
    evolutionStatus,
    setSystemStatus,
    setMemoryStats,
    setLearningStats,
    setEvolutionStatus,
  } = useAGIStore();

  const [performanceData, setPerformanceData] = useState([
    { time: '00:00', cpu: 45, memory: 62, responses: 23 },
    { time: '04:00', cpu: 52, memory: 58, responses: 31 },
    { time: '08:00', cpu: 38, memory: 65, responses: 45 },
    { time: '12:00', cpu: 71, memory: 72, responses: 67 },
    { time: '16:00', cpu: 65, memory: 68, responses: 52 },
    { time: '20:00', cpu: 43, memory: 61, responses: 38 },
  ]);

  const [learningData, setLearningData] = useState([
    { day: 'Mon', knowledge: 85, adaptation: 72, evolution: 45 },
    { day: 'Tue', knowledge: 88, adaptation: 75, evolution: 48 },
    { day: 'Wed', knowledge: 92, adaptation: 78, evolution: 52 },
    { day: 'Thu', knowledge: 89, adaptation: 82, evolution: 55 },
    { day: 'Fri', knowledge: 95, adaptation: 85, evolution: 58 },
    { day: 'Sat', knowledge: 98, adaptation: 88, evolution: 62 },
    { day: 'Sun', knowledge: 100, adaptation: 92, evolution: 65 },
  ]);

  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        const [systemRes, memoryRes, learningRes, evolutionRes] = await Promise.all([
          agiApi.getSystemStatus(),
          agiApi.getMemoryStats(),
          agiApi.getLearningStats(),
          agiApi.getEvolutionStatus(),
        ]);

        setSystemStatus(systemRes.data);
        setMemoryStats(memoryRes.data);
        setLearningStats(learningRes.data);
        setEvolutionStatus(evolutionRes.data);
      } catch (error) {
        console.error('Failed to fetch dashboard data:', error);
      }
    };

    fetchDashboardData();
    const interval = setInterval(fetchDashboardData, 30000); // Refresh every 30 seconds

    return () => clearInterval(interval);
  }, [setSystemStatus, setMemoryStats, setLearningStats, setEvolutionStatus]);

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
    hidden: { y: 20, opacity: 0 },
    visible: {
      y: 0,
      opacity: 1,
      transition: {
        type: 'spring',
        stiffness: 300,
        damping: 24,
      },
    },
  };

  const getHealthColor = (value: number) => {
    if (value >= 80) return theme.palette.success.main;
    if (value >= 60) return theme.palette.warning.main;
    return theme.palette.error.main;
  };

  return (
    <motion.div
      variants={containerVariants}
      initial="hidden"
      animate="visible"
      style={{ padding: theme.spacing(3) }}
    >
      <Typography
        variant="h4"
        sx={{
          fontWeight: 700,
          mb: 3,
          background: `linear-gradient(45deg, ${theme.palette.primary.main}, ${theme.palette.secondary.main})`,
          backgroundClip: 'text',
          WebkitBackgroundClip: 'text',
          WebkitTextFillColor: 'transparent',
        }}
      >
        AGI System Dashboard
      </Typography>

      <Grid container spacing={3}>
        {/* System Health */}
        <Grid item xs={12} md={6} lg={3}>
          <motion.div variants={itemVariants}>
            <Card sx={{ height: '100%' }}>
              <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', mb: 2 }}>
                  <Typography variant="h6" sx={{ fontWeight: 600 }}>
                    System Health
                  </Typography>
                  <MonitorHeart sx={{ color: 'primary.main' }} />
                </Box>
                
                <Typography variant="h4" sx={{ fontWeight: 700, mb: 1 }}>
                  {systemStatus?.cpu_usage?.toFixed(1) || '0.0'}%
                </Typography>
                <Typography variant="body2" sx={{ color: 'text.secondary', mb: 2 }}>
                  CPU Usage
                </Typography>

                <LinearProgress
                  variant="determinate"
                  value={systemStatus?.cpu_usage || 0}
                  sx={{
                    height: 8,
                    borderRadius: 4,
                    mb: 2,
                    backgroundColor: alpha(theme.palette.primary.main, 0.1),
                    '& .MuiLinearProgress-bar': {
                      backgroundColor: getHealthColor(100 - (systemStatus?.cpu_usage || 0)),
                      borderRadius: 4,
                    },
                  }}
                />

                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <Typography variant="body2" sx={{ color: 'text.secondary' }}>
                    Memory: {systemStatus?.memory_usage?.toFixed(1) || '0.0'}%
                  </Typography>
                  <Typography variant="body2" sx={{ color: 'text.secondary' }}>
                    Uptime: {systemStatus?.uptime || '0h'}
                  </Typography>
                </Box>
              </CardContent>
            </Card>
          </motion.div>
        </Grid>

        {/* Memory System */}
        <Grid item xs={12} md={6} lg={3}>
          <motion.div variants={itemVariants}>
            <Card sx={{ height: '100%' }}>
              <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', mb: 2 }}>
                  <Typography variant="h6" sx={{ fontWeight: 600 }}>
                    Memory System
                  </Typography>
                  <Memory sx={{ color: 'primary.main' }} />
                </Box>
                
                <Typography variant="h4" sx={{ fontWeight: 700, mb: 1 }}>
                  {memoryStats?.total_memories || 0}
                </Typography>
                <Typography variant="body2" sx={{ color: 'text.secondary', mb: 2 }}>
                  Total Memories
                </Typography>

                <Typography variant="body2" sx={{ color: 'text.secondary' }}>
                  Recent: {memoryStats?.recent_memories || 0}
                </Typography>
                <Typography variant="body2" sx={{ color: 'text.secondary' }}>
                  Storage: {memoryStats?.storage_size || '0 MB'}
                </Typography>
              </CardContent>
            </Card>
          </motion.div>
        </Grid>

        {/* Learning Progress */}
        <Grid item xs={12} md={6} lg={3}>
          <motion.div variants={itemVariants}>
            <Card sx={{ height: '100%' }}>
              <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', mb: 2 }}>
                  <Typography variant="h6" sx={{ fontWeight: 600 }}>
                    Learning Progress
                  </Typography>
                  <School sx={{ color: 'primary.main' }} />
                </Box>
                
                <Typography variant="h4" sx={{ fontWeight: 700, mb: 1 }}>
                  {learningStats?.adaptation_score?.toFixed(1) || '0.0'}%
                </Typography>
                <Typography variant="body2" sx={{ color: 'text.secondary', mb: 2 }}>
                  Adaptation Score
                </Typography>

                <LinearProgress
                  variant="determinate"
                  value={learningStats?.adaptation_score || 0}
                  sx={{
                    height: 8,
                    borderRadius: 4,
                    mb: 2,
                    backgroundColor: alpha(theme.palette.secondary.main, 0.1),
                    '& .MuiLinearProgress-bar': {
                      backgroundColor: theme.palette.secondary.main,
                      borderRadius: 4,
                    },
                  }}
                />

                <Typography variant="body2" sx={{ color: 'text.secondary' }}>
                  Experiences: {learningStats?.total_experiences || 0}
                </Typography>
                <Typography variant="body2" sx={{ color: 'text.secondary' }}>
                  Knowledge Growth: +{learningStats?.knowledge_growth?.toFixed(1) || '0.0'}%
                </Typography>
              </CardContent>
            </Card>
          </motion.div>
        </Grid>

        {/* Evolution Status */}
        <Grid item xs={12} md={6} lg={3}>
          <motion.div variants={itemVariants}>
            <Card sx={{ height: '100%' }}>
              <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', mb: 2 }}>
                  <Typography variant="h6" sx={{ fontWeight: 600 }}>
                    Evolution Status
                  </Typography>
                  <EvolutionIcon sx={{ color: 'primary.main' }} />
                </Box>
                
                <Typography variant="h4" sx={{ fontWeight: 700, mb: 1 }}>
                  Gen {evolutionStatus?.generation || 0}
                </Typography>
                <Typography variant="body2" sx={{ color: 'text.secondary', mb: 2 }}>
                  Current Generation
                </Typography>

                <Typography variant="body2" sx={{ color: 'text.secondary' }}>
                  Fitness: {evolutionStatus?.fitness_score?.toFixed(2) || '0.00'}
                </Typography>
                <Typography variant="body2" sx={{ color: 'text.secondary' }}>
                  Mutations: {evolutionStatus?.mutations || 0}
                </Typography>
              </CardContent>
            </Card>
          </motion.div>
        </Grid>

        {/* Performance Chart */}
        <Grid item xs={12} lg={8}>
          <motion.div variants={itemVariants}>
            <Card>
              <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', mb: 3 }}>
                  <Typography variant="h6" sx={{ fontWeight: 600 }}>
                    System Performance (24h)
                  </Typography>
                  <IconButton size="small">
                    <RefreshIcon />
                  </IconButton>
                </Box>
                
                <Box sx={{ height: 300 }}>
                  <ResponsiveContainer width="100%" height="100%">
                    <LineChart data={performanceData}>
                      <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
                      <XAxis dataKey="time" stroke="#b0b0b0" />
                      <YAxis stroke="#b0b0b0" />
                      <Tooltip
                        contentStyle={{
                          backgroundColor: 'rgba(26, 26, 26, 0.95)',
                          border: '1px solid rgba(255, 255, 255, 0.1)',
                          borderRadius: 8,
                        }}
                      />
                      <Line
                        type="monotone"
                        dataKey="cpu"
                        stroke="#00e5ff"
                        strokeWidth={2}
                        dot={{ fill: '#00e5ff', strokeWidth: 2, r: 4 }}
                        name="CPU %"
                      />
                      <Line
                        type="monotone"
                        dataKey="memory"
                        stroke="#ff4081"
                        strokeWidth={2}
                        dot={{ fill: '#ff4081', strokeWidth: 2, r: 4 }}
                        name="Memory %"
                      />
                      <Line
                        type="monotone"
                        dataKey="responses"
                        stroke="#4caf50"
                        strokeWidth={2}
                        dot={{ fill: '#4caf50', strokeWidth: 2, r: 4 }}
                        name="Responses/h"
                      />
                    </LineChart>
                  </ResponsiveContainer>
                </Box>
              </CardContent>
            </Card>
          </motion.div>
        </Grid>

        {/* Learning Progress Chart */}
        <Grid item xs={12} lg={4}>
          <motion.div variants={itemVariants}>
            <Card>
              <CardContent>
                <Typography variant="h6" sx={{ fontWeight: 600, mb: 3 }}>
                  Learning Progress (7d)
                </Typography>
                
                <Box sx={{ height: 300 }}>
                  <ResponsiveContainer width="100%" height="100%">
                    <AreaChart data={learningData}>
                      <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
                      <XAxis dataKey="day" stroke="#b0b0b0" />
                      <YAxis stroke="#b0b0b0" />
                      <Tooltip
                        contentStyle={{
                          backgroundColor: 'rgba(26, 26, 26, 0.95)',
                          border: '1px solid rgba(255, 255, 255, 0.1)',
                          borderRadius: 8,
                        }}
                      />
                      <Area
                        type="monotone"
                        dataKey="knowledge"
                        stackId="1"
                        stroke="#00e5ff"
                        fill="rgba(0, 229, 255, 0.3)"
                        name="Knowledge"
                      />
                      <Area
                        type="monotone"
                        dataKey="adaptation"
                        stackId="2"
                        stroke="#ff4081"
                        fill="rgba(255, 64, 129, 0.3)"
                        name="Adaptation"
                      />
                      <Area
                        type="monotone"
                        dataKey="evolution"
                        stackId="3"
                        stroke="#4caf50"
                        fill="rgba(76, 175, 80, 0.3)"
                        name="Evolution"
                      />
                    </AreaChart>
                  </ResponsiveContainer>
                </Box>
              </CardContent>
            </Card>
          </motion.div>
        </Grid>

        {/* Recent Activities */}
        <Grid item xs={12}>
          <motion.div variants={itemVariants}>
            <Card>
              <CardContent>
                <Typography variant="h6" sx={{ fontWeight: 600, mb: 3 }}>
                  Recent System Activities
                </Typography>
                
                <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
                  {[
                    { time: '2 minutes ago', event: 'Neural network optimization completed', type: 'success' },
                    { time: '15 minutes ago', event: 'Memory consolidation process started', type: 'info' },
                    { time: '1 hour ago', event: 'Evolution cycle triggered - Generation 47', type: 'warning' },
                    { time: '3 hours ago', event: 'Learning adaptation threshold reached', type: 'success' },
                    { time: '6 hours ago', event: 'System health check completed', type: 'info' },
                  ].map((activity, index) => (
                    <Paper
                      key={index}
                      sx={{
                        p: 2,
                        backgroundColor: 'rgba(255, 255, 255, 0.02)',
                        border: '1px solid rgba(255, 255, 255, 0.1)',
                      }}
                    >
                      <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                        <Typography variant="body1">{activity.event}</Typography>
                        <Typography variant="caption" sx={{ color: 'text.secondary' }}>
                          {activity.time}
                        </Typography>
                      </Box>
                    </Paper>
                  ))}
                </Box>
              </CardContent>
            </Card>
          </motion.div>
        </Grid>
      </Grid>
    </motion.div>
  );
};

export default Dashboard;