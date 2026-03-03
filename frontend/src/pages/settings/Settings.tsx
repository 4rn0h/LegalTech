import { Box, Container, Typography } from '@mui/material'

export default function Settings() {
  return (
    <Container>
      <Box sx={{ mt: 4 }}>
        <Typography variant="h4">Settings</Typography>
        <Typography variant="body1" sx={{ mt: 2 }}>
          User settings and preferences coming soon...
        </Typography>
      </Box>
    </Container>
  )
}
