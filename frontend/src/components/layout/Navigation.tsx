import { Link } from 'react-router-dom'

export default function Navigation() {
  const handleLogout = () => {
    // Clear auth tokens
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    window.location.href = '/'
  }

  return (
    <nav className="bg-white shadow-md">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          {/* Logo */}
          <div className="flex items-center">
            <Link to="/dashboard" className="flex items-center">
              <span className="text-2xl font-bold text-blue-600">⚖️ LegalTech</span>
            </Link>
          </div>

          {/* Main Navigation Links */}
          <div className="flex items-center space-x-8">
            <Link to="/dashboard" className="text-gray-700 hover:text-blue-600 transition font-medium">
              Dashboard
            </Link>
            <Link to="/clients" className="text-gray-700 hover:text-blue-600 transition font-medium">
              Clients
            </Link>
            <Link to="/documents" className="text-gray-700 hover:text-blue-600 transition font-medium">
              Documents
            </Link>
            <Link to="/messages" className="text-gray-700 hover:text-blue-600 transition font-medium">
              Messages
            </Link>
            <Link to="/reports" className="text-gray-700 hover:text-blue-600 transition font-medium">
              Reports
            </Link>

            {/* Dropdown for Additional Features */}
            <div className="relative group">
              <button className="text-gray-700 hover:text-blue-600 transition font-medium">
                More ▼
              </button>
              <div className="absolute left-0 mt-0 w-48 bg-white rounded-lg shadow-lg hidden group-hover:block z-50">
                <Link
                  to="/tax"
                  className="block px-4 py-2 text-gray-700 hover:bg-blue-50 first:rounded-t-lg"
                >
                  Tax Management
                </Link>
                <Link
                  to="/investments"
                  className="block px-4 py-2 text-gray-700 hover:bg-blue-50"
                >
                  Investments
                </Link>
                <Link
                  to="/billing"
                  className="block px-4 py-2 text-gray-700 hover:bg-blue-50 last:rounded-b-lg"
                >
                  Billing
                </Link>
              </div>
            </div>

            {/* Settings & Logout */}
            <div className="relative group">
              <button className="text-gray-700 hover:text-blue-600 transition font-medium">
                Account ▼
              </button>
              <div className="absolute right-0 mt-0 w-48 bg-white rounded-lg shadow-lg hidden group-hover:block z-50">
                <Link
                  to="/settings"
                  className="block px-4 py-2 text-gray-700 hover:bg-blue-50 first:rounded-t-lg"
                >
                  Settings
                </Link>
                <button
                  onClick={handleLogout}
                  className="w-full text-left px-4 py-2 text-red-600 hover:bg-red-50 last:rounded-b-lg border-none bg-transparent cursor-pointer"
                >
                  Logout
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </nav>
  )
}
