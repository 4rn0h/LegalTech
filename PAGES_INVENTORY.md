# Frontend Pages Inventory

## Currently Accessible Pages

### Authentication Routes (Public)
| Path | Component | Status |
|------|-----------|--------|
| `/login` | Login.tsx | ✅ Implemented |
| `/register` | Register.tsx | ✅ Implemented |
| `/mfa-verify` | MFAVerify.tsx | ✅ Implemented |
| `/forgot-password` | ForgotPassword.tsx | ✅ Implemented |

### Protected Routes (Authenticated Users)
| Path | Component | Status | Backend Endpoint |
|------|-----------|--------|-----------------|
| `/dashboard` | Dashboard.tsx | ✅ Implemented | `/api/v1/reports/widgets` |
| `/clients` | Clients.tsx | ✅ Implemented | `/api/v1/clients/` |
| `/documents` | Documents.tsx | ✅ Implemented | `/api/v1/documents/` |
| `/tax` | Tax.tsx | ✅ Implemented | `/api/v1/tax/` |
| `/investments` | Investments.tsx | ✅ Implemented | `/api/v1/investments/` |
| `/billing` | Billing.tsx | ✅ Implemented | `/api/v1/billing/` |
| `/settings` | Settings.tsx | ✅ Implemented | N/A |

## Missing Frontend Pages (Backend Endpoints Exist)
| Path | Purpose | Backend Endpoint | Status |
|------|---------|-----------------|--------|
| `/messages` | Messaging/Communications | `/api/v1/messages/` | ❌ TODO |
| `/reports` | Reports & Analytics | `/api/v1/reports/reports` | ❌ TODO |
| `/clients/:id/interactions` | Client Interactions/Activity | `/api/v1/clients/interactions` | ❌ TODO |

## Backend API Endpoints Summary
- `POST /api/v1/auth/login/` - User login
- `POST /api/v1/auth/login/refresh/` - Refresh token
- `POST /api/v1/auth/register/` - User registration
- `GET/POST /api/v1/clients/` - List/Create clients
- `GET /api/v1/clients/{id}/interactions/` - Client interactions
- `GET /api/v1/documents/` - List documents
- `GET /api/v1/messages/` - List messages
- `GET /api/v1/tax/` - Tax information
- `GET /api/v1/investments/` - Investment information
- `GET /api/v1/billing/` - Billing information
- `GET /api/v1/reports/reports/` - Reports list
- `GET /api/v1/reports/widgets/` - Dashboard widgets
