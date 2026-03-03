import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import {
  Box,
  Container,
  Card,
  CardHeader,
  CardContent,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Button,
  TextField,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Chip,
  Avatar,
  Stack,
  IconButton,
  Menu,
  MenuItem,
  TablePagination,
  InputAdornment,
  Typography,
} from '@mui/material'
import {
  Add,
  Edit,
  Delete,
  MoreVert,
  Search,
  Phone,
  Email,
} from '@mui/icons-material'
import apiService from '../../services/api'
import toast from 'react-hot-toast'

interface Client {
  id: number
  first_name: string
  last_name: string
  email: string
  phone_number?: string
  company_name?: string
  relationship_status: string
  onboarding_completed: boolean
  created_at: string
}

export default function ClientsList() {
  const queryClient = useQueryClient()
  const [page, setPage] = useState(0)
  const [rowsPerPage, setRowsPerPage] = useState(10)
  const [searchTerm, setSearchTerm] = useState('')
  const [openDialog, setOpenDialog] = useState(false)
  const [editingClient, setEditingClient] = useState<Client | null>(null)
  const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null)
  const [selectedClient, setSelectedClient] = useState<Client | null>(null)
  const [formData, setFormData] = useState({
    first_name: '',
    last_name: '',
    email: '',
    phone_number: '',
    company_name: '',
  })

  const { data: clientsData, isLoading } = useQuery({
    queryKey: ['clients', page, searchTerm],
    queryFn: () => apiService.getClients({ search: searchTerm }),
  })

  const createClientMutation = useMutation({
    mutationFn: () => apiService.createClient(formData),
    onSuccess: () => {
      toast.success('Client created successfully')
      queryClient.invalidateQueries({ queryKey: ['clients'] })
      handleCloseDialog()
    },
    onError: (error: any) => {
      toast.error(error.response?.data?.detail || 'Failed to create client')
    },
  })

  const deleteClientMutation = useMutation({
    mutationFn: (id: number) => apiService.deleteClient(id),
    onSuccess: () => {
      toast.success('Client deleted successfully')
      queryClient.invalidateQueries({ queryKey: ['clients'] })
      handleMenuClose()
    },
    onError: (error: any) => {
      toast.error('Failed to delete client')
    },
  })

  const handleOpenDialog = (client?: Client) => {
    if (client) {
      setEditingClient(client)
      setFormData({
        first_name: client.first_name,
        last_name: client.last_name,
        email: client.email,
        phone_number: client.phone_number || '',
        company_name: client.company_name || '',
      })
    }
    setOpenDialog(true)
  }

  const handleCloseDialog = () => {
    setOpenDialog(false)
    setEditingClient(null)
    setFormData({
      first_name: '',
      last_name: '',
      email: '',
      phone_number: '',
      company_name: '',
    })
  }

  const handleMenuOpen = (event: React.MouseEvent<HTMLElement>, client: Client) => {
    setAnchorEl(event.currentTarget)
    setSelectedClient(client)
  }

  const handleMenuClose = () => {
    setAnchorEl(null)
    setSelectedClient(null)
  }

  const handlePageChange = (event: unknown, newPage: number) => {
    setPage(newPage)
  }

  const handleRowsPerPageChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setRowsPerPage(parseInt(event.target.value, 10))
    setPage(0)
  }

  const handleSaveClient = () => {
    if (!formData.first_name || !formData.last_name || !formData.email) {
      toast.error('Please fill in all required fields')
      return
    }
    createClientMutation.mutate()
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active':
        return 'success'
      case 'archived':
        return 'error'
      case 'prospective':
        return 'warning'
      default:
        return 'default'
    }
  }

  const clients = clientsData?.results || []

  return (
    <Container maxWidth="xl" sx={{ py: 4 }}>
      {/* Header */}
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 4 }}>
        <Box>
          <Typography variant="h3" sx={{ fontWeight: 'bold', mb: 1 }}>
            Clients
          </Typography>
          <Typography variant="body1" color="text.secondary">
            Manage your clients and their information
          </Typography>
        </Box>
        <Button
          variant="contained"
          startIcon={<Add />}
          onClick={() => handleOpenDialog()}
          sx={{
            background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
          }}
        >
          Add Client
        </Button>
      </Box>

      {/* Search Bar */}
      <Card sx={{ mb: 3 }}>
        <CardContent>
          <TextField
            fullWidth
            placeholder="Search clients by name, email, or company..."
            value={searchTerm}
            onChange={(e) => {
              setSearchTerm(e.target.value)
              setPage(0)
            }}
            InputProps={{
              startAdornment: (
                <InputAdornment position="start">
                  <Search />
                </InputAdornment>
              ),
            }}
          />
        </CardContent>
      </Card>

      {/* Clients Table */}
      <Card>
        <CardHeader title="Client List" />
        <TableContainer>
          <Table>
            <TableHead>
              <TableRow sx={{ backgroundColor: '#f5f5f5' }}>
                <TableCell sx={{ fontWeight: 'bold' }}>Name</TableCell>
                <TableCell sx={{ fontWeight: 'bold' }}>Email</TableCell>
                <TableCell sx={{ fontWeight: 'bold' }}>Company</TableCell>
                <TableCell sx={{ fontWeight: 'bold' }}>Phone</TableCell>
                <TableCell sx={{ fontWeight: 'bold' }}>Status</TableCell>
                <TableCell sx={{ fontWeight: 'bold' }}>Onboarding</TableCell>
                <TableCell align="right" sx={{ fontWeight: 'bold' }}>
                  Actions
                </TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {isLoading ? (
                <TableRow>
                  <TableCell colSpan={7} align="center" sx={{ py: 3 }}>
                    Loading...
                  </TableCell>
                </TableRow>
              ) : clients.length === 0 ? (
                <TableRow>
                  <TableCell colSpan={7} align="center" sx={{ py: 3 }}>
                    No clients found
                  </TableCell>
                </TableRow>
              ) : (
                clients.map((client: Client) => (
                  <TableRow key={client.id} hover>
                    <TableCell>
                      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                        <Avatar sx={{ bgcolor: '#667eea', width: 32, height: 32 }}>
                          {client.first_name[0]}
                        </Avatar>
                        {client.first_name} {client.last_name}
                      </Box>
                    </TableCell>
                    <TableCell>{client.email}</TableCell>
                    <TableCell>{client.company_name || '-'}</TableCell>
                    <TableCell>{client.phone_number || '-'}</TableCell>
                    <TableCell>
                      <Chip
                        label={client.relationship_status}
                        color={getStatusColor(client.relationship_status)}
                        size="small"
                      />
                    </TableCell>
                    <TableCell>
                      <Chip
                        label={client.onboarding_completed ? 'Completed' : 'Pending'}
                        variant={client.onboarding_completed ? 'filled' : 'outlined'}
                        size="small"
                        color={client.onboarding_completed ? 'success' : 'warning'}
                      />
                    </TableCell>
                    <TableCell align="right">
                      <IconButton
                        size="small"
                        onClick={(e) => handleMenuOpen(e, client)}
                      >
                        <MoreVert />
                      </IconButton>
                    </TableCell>
                  </TableRow>
                ))
              )}
            </TableBody>
          </Table>
        </TableContainer>
        {!isLoading && (
          <TablePagination
            rowsPerPageOptions={[5, 10, 25]}
            component="div"
            count={clientsData?.count || 0}
            rowsPerPage={rowsPerPage}
            page={page}
            onPageChange={handlePageChange}
            onRowsPerPageChange={handleRowsPerPageChange}
          />
        )}
      </Card>

      {/* Context Menu */}
      <Menu
        anchorEl={anchorEl}
        open={Boolean(anchorEl)}
        onClose={handleMenuClose}
      >
        <MenuItem onClick={() => handleOpenDialog(selectedClient!)}>
          <Edit sx={{ mr: 1, fontSize: 20 }} />
          Edit
        </MenuItem>
        <MenuItem
          onClick={() => {
            if (selectedClient) {
              deleteClientMutation.mutate(selectedClient.id)
            }
          }}
          sx={{ color: 'error.main' }}
        >
          <Delete sx={{ mr: 1, fontSize: 20 }} />
          Delete
        </MenuItem>
      </Menu>

      {/* Add/Edit Client Dialog */}
      <Dialog open={openDialog} onClose={handleCloseDialog} maxWidth="sm" fullWidth>
        <DialogTitle>
          {editingClient ? 'Edit Client' : 'Add New Client'}
        </DialogTitle>
        <DialogContent sx={{ pt: 2 }}>
          <Stack spacing={2}>
            <TextField
              fullWidth
              label="First Name"
              value={formData.first_name}
              onChange={(e) =>
                setFormData({ ...formData, first_name: e.target.value })
              }
              required
            />
            <TextField
              fullWidth
              label="Last Name"
              value={formData.last_name}
              onChange={(e) =>
                setFormData({ ...formData, last_name: e.target.value })
              }
              required
            />
            <TextField
              fullWidth
              type="email"
              label="Email"
              value={formData.email}
              onChange={(e) =>
                setFormData({ ...formData, email: e.target.value })
              }
              required
            />
            <TextField
              fullWidth
              label="Phone"
              value={formData.phone_number}
              onChange={(e) =>
                setFormData({ ...formData, phone_number: e.target.value })
              }
            />
            <TextField
              fullWidth
              label="Company"
              value={formData.company_name}
              onChange={(e) =>
                setFormData({ ...formData, company_name: e.target.value })
              }
            />
          </Stack>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseDialog}>Cancel</Button>
          <Button
            onClick={handleSaveClient}
            variant="contained"
            disabled={createClientMutation.isPending}
          >
            {createClientMutation.isPending ? 'Saving...' : 'Save'}
          </Button>
        </DialogActions>
      </Dialog>
    </Container>
  )
}
