import axios, { AxiosInstance } from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1'

class ApiService {
  private axiosInstance: AxiosInstance

  constructor() {
    this.axiosInstance = axios.create({
      baseURL: API_BASE_URL,
      headers: {
        'Content-Type': 'application/json',
      },
    })

    // Add token to requests if available
    this.axiosInstance.interceptors.request.use(
      (config) => {
        const token = localStorage.getItem('access_token')
        if (token) {
          config.headers.Authorization = `Bearer ${token}`
        }
        return config
      },
      (error) => Promise.reject(error)
    )

    // Handle token refresh on 401
    this.axiosInstance.interceptors.response.use(
      (response) => response,
      async (error) => {
        const originalRequest = error.config
        if (error.response?.status === 401 && !originalRequest._retry) {
          originalRequest._retry = true
          try {
            const refreshToken = localStorage.getItem('refresh_token')
            const response = await axios.post(`${API_BASE_URL}/auth/login/refresh/`, {
              refresh: refreshToken,
            })
            const { access } = response.data
            localStorage.setItem('access_token', access)
            originalRequest.headers.Authorization = `Bearer ${access}`
            return this.axiosInstance(originalRequest)
          } catch (err) {
            localStorage.removeItem('access_token')
            localStorage.removeItem('refresh_token')
            window.location.href = '/login'
            return Promise.reject(err)
          }
        }
        return Promise.reject(error)
      }
    )
  }

  // Auth endpoints
  async login(email: string, password: string) {
    const response = await this.axiosInstance.post('/auth/login/', { email, password })
    if (response.data.access) {
      localStorage.setItem('access_token', response.data.access)
      localStorage.setItem('refresh_token', response.data.refresh)
    }
    return response.data
  }

  async register(email: string, username: string, password: string, firstName: string, lastName: string, role: string = 'client') {
    const response = await this.axiosInstance.post('/auth/register/', {
      email,
      username,
      password,
      password_confirm: password,
      first_name: firstName,
      last_name: lastName,
      role,
    })
    if (response.data.access) {
      localStorage.setItem('access_token', response.data.access)
      localStorage.setItem('refresh_token', response.data.refresh)
    }
    return response.data
  }

  async logout() {
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
  }

  // User endpoints
  async getCurrentUser() {
    const response = await this.axiosInstance.get('/auth/users/me/')
    return response.data
  }

  async updateProfile(profileData: any) {
    const response = await this.axiosInstance.patch('/auth/users/me/', profileData)
    return response.data
  }

  async changePassword(oldPassword: string, newPassword: string) {
    const response = await this.axiosInstance.post('/auth/users/change_password/', {
      old_password: oldPassword,
      new_password: newPassword,
      new_password_confirm: newPassword,
    })
    return response.data
  }

  // MFA endpoints
  async setupMFA() {
    const response = await this.axiosInstance.post('/auth/users/setup_mfa/')
    return response.data
  }

  async verifyMFA(token: string) {
    const response = await this.axiosInstance.post('/auth/users/verify_mfa/', { token })
    return response.data
  }

  async disableMFA() {
    const response = await this.axiosInstance.post('/auth/users/disable_mfa/')
    return response.data
  }

  // Client endpoints
  async getClients(params?: any) {
    const response = await this.axiosInstance.get('/clients/', { params })
    return response.data
  }

  async getClient(id: string) {
    const response = await this.axiosInstance.get(`/clients/${id}/`)
    return response.data
  }

  async createClient(clientData: any) {
    const response = await this.axiosInstance.post('/clients/', clientData)
    return response.data
  }

  async updateClient(id: string, clientData: any) {
    const response = await this.axiosInstance.put(`/clients/${id}/`, clientData)
    return response.data
  }

  async deleteClient(id: string) {
    await this.axiosInstance.delete(`/clients/${id}/`)
  }

  async markClientOnboarded(id: string) {
    const response = await this.axiosInstance.post(`/clients/${id}/mark_onboarded/`)
    return response.data
  }

  async archiveClient(id: string) {
    const response = await this.axiosInstance.post(`/clients/${id}/archive/`)
    return response.data
  }

  // Document endpoints
  async getDocuments(params?: any) {
    const response = await this.axiosInstance.get('/documents/', { params })
    return response.data
  }

  async getDocument(id: string) {
    const response = await this.axiosInstance.get(`/documents/${id}/`)
    return response.data
  }

  async uploadDocument(formData: FormData) {
    const response = await this.axiosInstance.post('/documents/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
    return response.data
  }

  async shareDocument(id: string, userIds: string[]) {
    const response = await this.axiosInstance.post(`/documents/${id}/share/`, { user_ids: userIds })
    return response.data
  }

  async uploadDocumentVersion(id: string, formData: FormData) {
    const response = await this.axiosInstance.post(`/documents/${id}/new_version/`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
    return response.data
  }

  async getDocumentVersions(id: string) {
    const response = await this.axiosInstance.get(`/documents/${id}/versions/`)
    return response.data
  }

  async getDocumentAccessLog(id: string) {
    const response = await this.axiosInstance.get(`/documents/${id}/access_log/`)
    return response.data
  }

  // Messaging endpoints
  async getConversations(params?: any) {
    const response = await this.axiosInstance.get('/messages/conversations/', { params })
    return response.data
  }

  async getConversation(id: string) {
    const response = await this.axiosInstance.get(`/messages/conversations/${id}/`)
    return response.data
  }

  async createConversation(conversationData: any) {
    const response = await this.axiosInstance.post('/messages/conversations/', conversationData)
    return response.data
  }

  async getMessages(conversationId: string, params?: any) {
    const response = await this.axiosInstance.get('/messages/messages/', {
      params: { conversation: conversationId, ...params },
    })
    return response.data
  }

  async sendMessage(conversationId: string, content: string, attachment?: File) {
    const formData = new FormData()
    formData.append('conversation', conversationId)
    formData.append('content', content)
    if (attachment) {
      formData.append('attachment', attachment)
    }

    const response = await this.axiosInstance.post('/messages/messages/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
    return response.data
  }

  async markMessageAsRead(id: string) {
    const response = await this.axiosInstance.post(`/messages/messages/${id}/mark_as_read/`)
    return response.data
  }

  async editMessage(id: string, content: string) {
    const response = await this.axiosInstance.post(`/messages/messages/${id}/edit/`, { content })
    return response.data
  }

  // Tax endpoints
  async getTaxReturns(params?: any) {
    const response = await this.axiosInstance.get('/tax/returns/', { params })
    return response.data
  }

  async getTaxReturn(id: string) {
    const response = await this.axiosInstance.get(`/tax/returns/${id}/`)
    return response.data
  }

  async createTaxReturn(returnData: any) {
    const response = await this.axiosInstance.post('/tax/returns/', returnData)
    return response.data
  }

  async uploadTaxDocument(returnId: string, formData: FormData) {
    formData.append('tax_return', returnId)
    const response = await this.axiosInstance.post('/tax/documents/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
    return response.data
  }

  async fileReturn(id: string) {
    const response = await this.axiosInstance.post(`/tax/returns/${id}/file_return/`)
    return response.data
  }

  // Investment endpoints
  async getPortfolio() {
    const response = await this.axiosInstance.get('/investments/portfolios/me/')
    return response.data
  }

  async getInvestments(params?: any) {
    const response = await this.axiosInstance.get('/investments/investments/', { params })
    return response.data
  }

  async addInvestment(investmentData: any) {
    const response = await this.axiosInstance.post('/investments/investments/', investmentData)
    return response.data
  }

  async updateInvestment(id: string, investmentData: any) {
    const response = await this.axiosInstance.put(`/investments/investments/${id}/`, investmentData)
    return response.data
  }

  // Billing endpoints
  async getInvoices(params?: any) {
    const response = await this.axiosInstance.get('/billing/invoices/', { params })
    return response.data
  }

  async getInvoice(id: string) {
    const response = await this.axiosInstance.get(`/billing/invoices/${id}/`)
    return response.data
  }

  async createInvoice(invoiceData: any) {
    const response = await this.axiosInstance.post('/billing/invoices/', invoiceData)
    return response.data
  }

  async markInvoiceAsPaid(id: string) {
    const response = await this.axiosInstance.post(`/billing/invoices/${id}/mark_as_paid/`)
    return response.data
  }

  async sendInvoice(id: string) {
    const response = await this.axiosInstance.post(`/billing/invoices/${id}/send_invoice/`)
    return response.data
  }

  async recordPayment(paymentData: any) {
    const response = await this.axiosInstance.post('/billing/payments/', paymentData)
    return response.data
  }

  // Dashboard endpoints
  async getDashboard() {
    const response = await this.axiosInstance.get('/reports/widgets/dashboard/')
    return response.data
  }

  async getReports(params?: any) {
    const response = await this.axiosInstance.get('/reports/reports/', { params })
    return response.data
  }

  // Generic request methods
  async get<T>(url: string, params?: any): Promise<T> {
    const response = await this.axiosInstance.get<T>(url, { params })
    return response.data
  }

  async post<T>(url: string, data?: any): Promise<T> {
    const response = await this.axiosInstance.post<T>(url, data)
    return response.data
  }

  async put<T>(url: string, data?: any): Promise<T> {
    const response = await this.axiosInstance.put<T>(url, data)
    return response.data
  }

  async patch<T>(url: string, data?: any): Promise<T> {
    const response = await this.axiosInstance.patch<T>(url, data)
    return response.data
  }

  async delete(url: string): Promise<void> {
    await this.axiosInstance.delete(url)
  }
}

export const apiService = new ApiService()
export default apiService
