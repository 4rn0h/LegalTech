import { Routes, Route, Navigate } from 'react-router-dom'
import { useAuth } from './hooks/useAuth'

// Layouts
import MainLayout from './components/layout/MainLayout'
import AuthLayout from './components/layout/AuthLayout'
import PublicLayout from './components/layout/PublicLayout'

// Public pages
import Home from './pages/public/Home'
import AboutUs from './pages/public/AboutUs'
import Services from './pages/public/Services'
import ContactUs from './pages/public/ContactUs'
import PrivacyPolicy from './pages/public/PrivacyPolicy'
import TermsOfService from './pages/public/TermsOfService'

// Auth pages
import Login from './pages/auth/Login'
import Register from './pages/auth/Register'
import MFAVerify from './pages/auth/MFAVerify'
import ForgotPassword from './pages/auth/ForgotPassword'

// Dashboard pages
import Dashboard from './pages/dashboard/Dashboard'

// Feature pages
import Clients from './pages/clients/Clients'
import ClientDetail from './pages/clients/ClientDetail'
import Documents from './pages/documents/Documents'
import Tax from './pages/tax/Tax'
import Investments from './pages/investments/Investments'
import Billing from './pages/billing/Billing'
import Settings from './pages/settings/Settings'
import Messages from './pages/messaging/Messages'
import Reports from './pages/reporting/Reports'

function App() {
  const { isAuthenticated, isLoading } = useAuth()

  if (isLoading) {
    return <div>Loading...</div>
  }

  return (
    <Routes>
      {/* Public Marketing Pages */}
      <Route element={<PublicLayout />}>
        <Route path="/" element={<Home />} />
        <Route path="/about" element={<AboutUs />} />
        <Route path="/services" element={<Services />} />
        <Route path="/contact" element={<ContactUs />} />
        <Route path="/privacy" element={<PrivacyPolicy />} />
        <Route path="/terms" element={<TermsOfService />} />
      </Route>

      {/* Auth Pages */}
      <Route element={<AuthLayout />}>
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/mfa-verify" element={<MFAVerify />} />
        <Route path="/forgot-password" element={<ForgotPassword />} />
      </Route>

      {/* Protected routes */}
      <Route element={<MainLayout />}>
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/clients" element={<Clients />} />
        <Route path="/clients/:id" element={<ClientDetail />} />
        <Route path="/documents" element={<Documents />} />
        <Route path="/tax" element={<Tax />} />
        <Route path="/investments" element={<Investments />} />
        <Route path="/billing" element={<Billing />} />
        <Route path="/messages" element={<Messages />} />
        <Route path="/reports" element={<Reports />} />
        <Route path="/settings" element={<Settings />} />
      </Route>

      {/* Redirect unknown routes */}
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  )
}

export default App
