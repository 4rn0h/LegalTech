import { Link } from 'react-router-dom'

export default function Home() {
  return (
    <div className="space-y-20">
      {/* Hero Section */}
      <section className="max-w-7xl mx-auto px-4 py-20">
        <div className="grid grid-cols-2 gap-12 items-center">
          <div>
            <h1 className="text-5xl font-bold text-gray-900 mb-6">
              Modern Legal Technology Solutions
            </h1>
            <p className="text-xl text-gray-600 mb-8">
              Streamline your legal practice with our comprehensive platform designed for legal professionals, law firms, and in-house counsel.
            </p>
            <div className="flex gap-4">
              <Link
                to="/register"
                className="bg-blue-600 text-white px-8 py-3 rounded-lg hover:bg-blue-700 transition font-semibold"
              >
                Get Started Free
              </Link>
              <Link
                to="/about"
                className="border-2 border-blue-600 text-blue-600 px-8 py-3 rounded-lg hover:bg-blue-50 transition font-semibold"
              >
                Learn More
              </Link>
            </div>
          </div>
          <div className="bg-gradient-to-br from-blue-100 to-indigo-100 rounded-lg h-96 flex items-center justify-center">
            <div className="text-6xl">⚖️</div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="bg-gray-50 py-20">
        <div className="max-w-7xl mx-auto px-4">
          <h2 className="text-4xl font-bold text-center mb-12">Key Features</h2>
          <div className="grid grid-cols-3 gap-8">
            <div className="bg-white p-8 rounded-lg shadow">
              <div className="text-4xl mb-4">📋</div>
              <h3 className="text-xl font-bold mb-3">Document Management</h3>
              <p className="text-gray-600">
                Organize, version control, and collaborate on legal documents with advanced search and tagging capabilities.
              </p>
            </div>
            <div className="bg-white p-8 rounded-lg shadow">
              <div className="text-4xl mb-4">💼</div>
              <h3 className="text-xl font-bold mb-3">Client Management</h3>
              <p className="text-gray-600">
                Maintain detailed client profiles, track interactions, and manage relationships efficiently.
              </p>
            </div>
            <div className="bg-white p-8 rounded-lg shadow">
              <div className="text-4xl mb-4">📊</div>
              <h3 className="text-xl font-bold mb-3">Analytics & Reports</h3>
              <p className="text-gray-600">
                Generate comprehensive reports and gain insights into your practice with advanced analytics.
              </p>
            </div>
            <div className="bg-white p-8 rounded-lg shadow">
              <div className="text-4xl mb-4">💰</div>
              <h3 className="text-xl font-bold mb-3">Billing & Invoicing</h3>
              <p className="text-gray-600">
                Track time, manage billing hours, and create professional invoices automatically.
              </p>
            </div>
            <div className="bg-white p-8 rounded-lg shadow">
              <div className="text-4xl mb-4">💬</div>
              <h3 className="text-xl font-bold mb-3">Secure Messaging</h3>
              <p className="text-gray-600">
                Communicate securely with clients and team members with encrypted messaging.
              </p>
            </div>
            <div className="bg-white p-8 rounded-lg shadow">
              <div className="text-4xl mb-4">🔒</div>
              <h3 className="text-xl font-bold mb-3">Security & Compliance</h3>
              <p className="text-gray-600">
                Enterprise-grade security with data encryption and compliance with legal standards.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="max-w-7xl mx-auto px-4 py-20 text-center">
        <h2 className="text-4xl font-bold mb-6">Ready to Transform Your Practice?</h2>
        <p className="text-xl text-gray-600 mb-8">
          Join hundreds of law firms already using LegalTech to streamline their operations.
        </p>
        <Link
          to="/register"
          className="bg-blue-600 text-white px-8 py-3 rounded-lg hover:bg-blue-700 transition font-semibold inline-block"
        >
          Start Your Free Trial
        </Link>
      </section>
    </div>
  )
}
