import { Box, Container, Typography } from '@mui/material'

export default function Billing() {
  return (
    <Container>
      <Box sx={{ mt: 4 }}>
        <Typography variant="h4">Billing & Invoices</Typography>
        <Typography variant="body1" sx={{ mt: 2 }}>
          Invoice and billing management coming soon...
        </Typography>
      </Box>
    </Container>
  )
}
