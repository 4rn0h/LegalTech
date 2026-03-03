import { Outlet } from 'react-router-dom'
import { Box, Container } from '@mui/material'

export default function AuthLayout() {
  return (
    <Box
      sx={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        minHeight: '100vh',
        bgcolor: '#f5f5f5',
      }}
    >
      <Container maxWidth="sm">
        <Box
          sx={{
            bgcolor: 'white',
            borderRadius: 2,
            boxShadow: 3,
            p: 4,
          }}
        >
          <Outlet />
        </Box>
      </Container>
    </Box>
  )
}
