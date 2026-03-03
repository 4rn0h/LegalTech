import { useState } from 'react'
import { useNavigate, Link as RouterLink } from 'react-router-dom'
import { useMutation } from '@tanstack/react-query'
import apiService from '../../services/api'
import toast from 'react-hot-toast'
import {
  Box,
  Button,
  TextField,
  Container,
  Typography,
  Link,
  CircularProgress,
  Paper,
  Card,
  CardContent,
  Divider,
  Alert,
  InputAdornment,
  IconButton,
  Grid,
} from '@mui/material'
import { Visibility, VisibilityOff, LockOutlined } from '@mui/icons-material'

export default function Login() {
  const navigate = useNavigate()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [showPassword, setShowPassword] = useState(false)
  const [errors, setErrors] = useState<Record<string, string>>({})

  const { mutate: handleLogin, isPending } = useMutation({
    mutationFn: () => apiService.login(email, password),
    onSuccess: (data) => {
      localStorage.setItem('access_token', data.access)
      localStorage.setItem('refresh_token', data.refresh)
      localStorage.setItem('user', JSON.stringify(data.user))
      toast.success('Logged in successfully')
      navigate('/dashboard')
    },
    onError: (error: any) => {
      const errorMessage = error.response?.data?.detail || error.message || 'Login failed'
      toast.error(errorMessage)
      if (error.response?.data?.errors) {
        setErrors(error.response.data.errors)
      }
    },
  })

  const validateForm = () => {
    const newErrors: Record<string, string> = {}
    if (!email) newErrors.email = 'Email is required'
    if (!password) newErrors.password = 'Password is required'
    if (email && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
      newErrors.email = 'Invalid email format'
    }
    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
  }

  const onSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (validateForm()) {
      handleLogin()
    }
  }

  return (
    <Box
      sx={{
        minHeight: '100vh',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        padding: 2,
      }}
    >
      <Container maxWidth="sm">
        <Card
          elevation={8}
          sx={{
            borderRadius: 3,
            overflow: 'hidden',
          }}
        >
          <Box
            sx={{
              background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
              color: 'white',
              padding: 3,
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
              gap: 1,
            }}
          >
            <Box
              sx={{
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                width: 56,
                height: 56,
                borderRadius: '50%',
                backgroundColor: 'rgba(255, 255, 255, 0.2)',
              }}
            >
              <LockOutlined sx={{ fontSize: 32 }} />
            </Box>
            <Typography variant="h4" component="h1" sx={{ fontWeight: 'bold' }}>
              Welcome Back
            </Typography>
            <Typography variant="body2" sx={{ opacity: 0.9 }}>
              DeltaOne Platform
            </Typography>
          </Box>

          <CardContent sx={{ p: 4 }}>
            <Box component="form" onSubmit={onSubmit} sx={{ mt: 1 }}>
              <TextField
                fullWidth
                id="email"
                label="Email Address"
                name="email"
                autoComplete="email"
                autoFocus
                value={email}
                onChange={(e) => {
                  setEmail(e.target.value)
                  if (errors.email) setErrors({ ...errors, email: '' })
                }}
                error={!!errors.email}
                helperText={errors.email}
                margin="normal"
                disabled={isPending}
                sx={{ mb: 2 }}
              />

              <TextField
                fullWidth
                name="password"
                label="Password"
                type={showPassword ? 'text' : 'password'}
                id="password"
                autoComplete="current-password"
                value={password}
                onChange={(e) => {
                  setPassword(e.target.value)
                  if (errors.password) setErrors({ ...errors, password: '' })
                }}
                error={!!errors.password}
                helperText={errors.password}
                margin="normal"
                disabled={isPending}
                InputProps={{
                  endAdornment: (
                    <InputAdornment position="end">
                      <IconButton
                        aria-label="toggle password visibility"
                        onClick={() => setShowPassword(!showPassword)}
                        edge="end"
                        disabled={isPending}
                      >
                        {showPassword ? <VisibilityOff /> : <Visibility />}
                      </IconButton>
                    </InputAdornment>
                  ),
                }}
                sx={{ mb: 3 }}
              />

              <Button
                fullWidth
                variant="contained"
                size="large"
                onClick={onSubmit}
                disabled={isPending || !email || !password}
                sx={{
                  background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                  py: 1.5,
                  fontSize: '1rem',
                  fontWeight: 'bold',
                  mb: 2,
                }}
              >
                {isPending ? (
                  <>
                    <CircularProgress size={20} sx={{ mr: 1, color: 'white' }} />
                    Logging in...
                  </>
                ) : (
                  'Sign In'
                )}
              </Button>

              <Link
                component={RouterLink}
                to="/forgot-password"
                sx={{
                  display: 'block',
                  textAlign: 'center',
                  color: '#667eea',
                  textDecoration: 'none',
                  fontWeight: 500,
                  '&:hover': { textDecoration: 'underline' },
                  mb: 2,
                }}
              >
                Forgot Password?
              </Link>

              <Divider sx={{ my: 2 }} />

              <Typography variant="body2" sx={{ textAlign: 'center', color: 'text.secondary' }}>
                Don't have an account?{' '}
                <Link
                  component={RouterLink}
                  to="/register"
                  sx={{
                    color: '#667eea',
                    textDecoration: 'none',
                    fontWeight: 'bold',
                    '&:hover': { textDecoration: 'underline' },
                  }}
                >
                  Sign Up
                </Link>
              </Typography>
            </Box>
          </CardContent>
        </Card>

        <Typography
          variant="caption"
          sx={{
            display: 'block',
            textAlign: 'center',
            mt: 3,
            color: 'rgba(255, 255, 255, 0.7)',
          }}
        >
          © 2024 DeltaOne. All rights reserved.
        </Typography>
      </Container>
    </Box>
  )
}
