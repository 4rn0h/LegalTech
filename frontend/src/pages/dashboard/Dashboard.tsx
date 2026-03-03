import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import {
  Box,
  Container,
  Grid,
  Card,
  CardContent,
  CardHeader,
  Typography,
  Button,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  Avatar,
  Chip,
  Stack,
  Divider,
} from '@mui/material'
import {
  TrendingUp,
  FileText,
  Users,
  DollarSign,
  ArrowUpward,
  ArrowDownward,
  PersonAdd,
  FileTextOutlined,
  AttachMoneyOutlined,
  Clock,
} from '@mui/icons-material'
import {
  LineChart,
  Line,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
} from 'recharts'
import apiService from '../../services/api'

interface MetricCard {
  title: string
  value: string | number
  change: number
  icon: React.ReactNode
  color: string
}

const chartData = [
  { month: 'Jan', value: 4000 },
  { month: 'Feb', value: 3000 },
  { month: 'Mar', value: 2000 },
  { month: 'Apr', value: 2780 },
  { month: 'May', value: 1890 },
  { month: 'Jun', value: 2390 },
]

const pieData = [
  { name: 'Active', value: 400, color: '#667eea' },
  { name: 'Archived', value: 100, color: '#f093fb' },
  { name: 'Prospective', value: 150, color: '#4facfe' },
]

export default function Dashboard() {
  const { data: user } = useQuery({
    queryKey: ['currentUser'],
    queryFn: () => apiService.getCurrentUser(),
  })

  const metrics: MetricCard[] = [
    {
      title: 'Total Clients',
      value: '28',
      change: 12,
      icon: <Users sx={{ fontSize: 32, color: '#667eea' }} />,
      color: '#667eea',
    },
    {
      title: 'Active Documents',
      value: '156',
      change: 8,
      icon: <FileText sx={{ fontSize: 32, color: '#f093fb' }} />,
      color: '#f093fb',
    },
    {
      title: 'Revenue (This Month)',
      value: '$24,500',
      change: 15,
      icon: <DollarSign sx={{ fontSize: 32, color: '#4facfe' }} />,
      color: '#4facfe',
    },
    {
      title: 'Pending Tasks',
      value: '12',
      change: -5,
      icon: <TrendingUp sx={{ fontSize: 32, color: '#43e97b' }} />,
      color: '#43e97b',
    },
  ]

  const recentActivities = [
    {
      id: 1,
      type: 'client',
      name: 'John Smith',
      action: 'New client added',
      time: '2 hours ago',
      avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=John',
    },
    {
      id: 2,
      type: 'document',
      name: 'Tax Return 2024',
      action: 'Document uploaded',
      time: '4 hours ago',
      avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=doc1',
    },
    {
      id: 3,
      type: 'invoice',
      name: 'Invoice #INV-2024-001',
      action: 'Invoice created',
      time: '1 day ago',
      avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=inv1',
    },
    {
      id: 4,
      type: 'client',
      name: 'Jane Doe',
      action: 'Profile updated',
      time: '2 days ago',
      avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=Jane',
    },
  ]

  const getActivityIcon = (type: string) => {
    switch (type) {
      case 'client':
        return <PersonAdd sx={{ color: '#667eea' }} />
      case 'document':
        return <FileTextOutlined sx={{ color: '#f093fb' }} />
      case 'invoice':
        return <AttachMoneyOutlined sx={{ color: '#43e97b' }} />
      default:
        return <Clock />
    }
  }

  return (
    <Container maxWidth="xl" sx={{ py: 4 }}>
      {/* Header */}
      <Box sx={{ mb: 4 }}>
        <Typography variant="h3" sx={{ fontWeight: 'bold', mb: 1 }}>
          Welcome back, {user?.first_name}!
        </Typography>
        <Typography variant="body1" color="text.secondary">
          Here's what's happening with your platform today.
        </Typography>
      </Box>

      {/* Metrics Grid */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        {metrics.map((metric, index) => (
          <Grid item xs={12} sm={6} md={3} key={index}>
            <Card
              sx={{
                background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                color: 'white',
                position: 'relative',
                overflow: 'hidden',
                '&::before': {
                  content: '""',
                  position: 'absolute',
                  top: -50,
                  right: -50,
                  width: 150,
                  height: 150,
                  borderRadius: '50%',
                  opacity: 0.1,
                },
              }}
            >
              <CardContent sx={{ position: 'relative', zIndex: 1 }}>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                  <Box>
                    <Typography variant="body2" sx={{ opacity: 0.9, mb: 1 }}>
                      {metric.title}
                    </Typography>
                    <Typography variant="h4" sx={{ fontWeight: 'bold', mb: 1 }}>
                      {metric.value}
                    </Typography>
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5 }}>
                      {metric.change > 0 ? (
                        <ArrowUpward sx={{ fontSize: 16 }} />
                      ) : (
                        <ArrowDownward sx={{ fontSize: 16 }} />
                      )}
                      <Typography variant="caption">
                        {Math.abs(metric.change)}% {metric.change > 0 ? 'increase' : 'decrease'}
                      </Typography>
                    </Box>
                  </Box>
                  <Box
                    sx={{
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      width: 60,
                      height: 60,
                      borderRadius: '12px',
                      backgroundColor: 'rgba(255, 255, 255, 0.2)',
                    }}
                  >
                    {metric.icon}
                  </Box>
                </Box>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      {/* Charts Section */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} md={7}>
          <Card>
            <CardHeader title="Revenue Trend" subheader="Last 6 months" sx={{ pb: 0 }} />
            <CardContent>
              <ResponsiveContainer width="100%" height={300}>
                <LineChart data={chartData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="month" />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <Line type="monotone" dataKey="value" stroke="#667eea" strokeWidth={2} />
                </LineChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={5}>
          <Card>
            <CardHeader title="Client Distribution" subheader="By status" sx={{ pb: 0 }} />
            <CardContent sx={{ display: 'flex', justifyContent: 'center' }}>
              <ResponsiveContainer width="100%" height={250}>
                <PieChart>
                  <Pie
                    data={pieData}
                    cx="50%"
                    cy="50%"
                    labelLine={false}
                    label={({ name, value }) => `${name}: ${value}`}
                    outerRadius={80}
                    fill="#8884d8"
                    dataKey="value"
                  >
                    {pieData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color} />
                    ))}
                  </Pie>
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Quick Actions and Recent Activity */}
      <Grid container spacing={3}>
        <Grid item xs={12} md={4}>
          <Card>
            <CardHeader title="Quick Actions" sx={{ pb: 2 }} />
            <CardContent>
              <Stack spacing={2}>
                <Button
                  fullWidth
                  variant="contained"
                  startIcon={<PersonAdd />}
                  sx={{
                    background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                    textTransform: 'none',
                    fontSize: '1rem',
                  }}
                >
                  Add Client
                </Button>
                <Button
                  fullWidth
                  variant="outlined"
                  startIcon={<FileTextOutlined />}
                  sx={{ textTransform: 'none', fontSize: '1rem' }}
                >
                  Upload Document
                </Button>
                <Button
                  fullWidth
                  variant="outlined"
                  startIcon={<AttachMoneyOutlined />}
                  sx={{ textTransform: 'none', fontSize: '1rem' }}
                >
                  Create Invoice
                </Button>
              </Stack>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={8}>
          <Card>
            <CardHeader title="Recent Activity" subheader="Latest updates" sx={{ pb: 1 }} />
            <List>
              {recentActivities.map((activity, index) => (
                <Box key={activity.id}>
                  <ListItem>
                    <ListItemIcon>
                      <Avatar src={activity.avatar} sx={{ width: 40, height: 40 }} />
                    </ListItemIcon>
                    <ListItemText
                      primary={
                        <Typography variant="body2" sx={{ fontWeight: 500 }}>
                          {activity.action}
                        </Typography>
                      }
                      secondary={
                        <Box>
                          <Typography variant="body2" color="text.primary" sx={{ fontWeight: 500, mt: 0.5 }}>
                            {activity.name}
                          </Typography>
                          <Typography variant="caption" color="text.secondary">
                            {activity.time}
                          </Typography>
                        </Box>
                      }
                    />
                    <Chip
                      label={activity.type}
                      size="small"
                      variant="outlined"
                      sx={{
                        bgcolor:
                          activity.type === 'client'
                            ? '#e3f2fd'
                            : activity.type === 'document'
                              ? '#f3e5f5'
                              : '#e8f5e9',
                        color:
                          activity.type === 'client'
                            ? '#667eea'
                            : activity.type === 'document'
                              ? '#f093fb'
                              : '#43e97b',
                      }}
                    />
                  </ListItem>
                  {index < recentActivities.length - 1 && <Divider />}
                </Box>
              ))}
            </List>
          </Card>
        </Grid>
      </Grid>
    </Container>
  )
}
