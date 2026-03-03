import { Box, Container, Typography } from '@mui/material'

export default function ForgotPassword() {
  return (
    <Container>
      <Box sx={{ mt: 4 }}>
        <Typography variant="h4">Forgot Password</Typography>
        <Typography variant="body1" sx={{ mt: 2 }}>
          Password reset coming soon...
        </Typography>
      </Box>
    </Container>
  )
}
