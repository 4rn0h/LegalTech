import { Box, Container, Typography } from '@mui/material'

export default function MFAVerify() {
  return (
    <Container>
      <Box sx={{ mt: 4 }}>
        <Typography variant="h4">Multi-Factor Authentication</Typography>
        <Typography variant="body1" sx={{ mt: 2 }}>
          MFA verification coming soon...
        </Typography>
      </Box>
    </Container>
  )
}
