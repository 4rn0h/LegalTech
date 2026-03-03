import { Link } from 'react-router-dom'

export default function Services() {
  const services = [
    {
      icon: '📋',
      title: 'Document Management',
      description: 'Centralized repository for all legal documents with version control, search, and collaboration features.',
      features: ['Version control', 'Full-text search', 'Collaboration tools', 'Audit trails'],
    },
    {
      icon: '👥',
      title: 'Client Management',
      description: 'Complete client relationship management with contact details, history, and interaction tracking.',
      features: ['Client profiles', 'Interaction history', 'Contact management', 'Client portal'],
    },
    {
      icon: '📊',
      title: 'Analytics & Reporting',
      description: 'Comprehensive insights into your practice with customizable dashboards and detailed reports.',
      features: ['Custom dashboards', 'Performance metrics', 'Export reports', 'Data visualization'],
    },
    {
      icon: '💰',
      title: 'Time & Billing',
      description: 'Track billable hours, manage invoices, and streamline your billing process.',
      features: ['Time tracking', 'Invoice generation', 'Payment tracking', 'Billing reports'],
    },
    {
      icon: '💼',
      title: 'Matter Management',
      description: 'Organize cases and matters with tasks, deadlines, and team collaboration features.',
      features: ['Case tracking', 'Task management', 'Deadline alerts', 'Team collaboration'],
    },
    {
      icon: '💬',
      title: 'Secure Communication',
      description: 'Encrypted messaging and communication channels for attorney-client privilege.',
      features: ['End-to-end encryption', 'Message history', 'File sharing', 'Compliance ready'],
    },
    {
      icon: '📈',
      title: 'Investment Management',
      description: 'Track and manage client investments with detailed portfolio analysis.',
      features: ['Portfolio tracking', 'Performance analysis', 'Risk assessment', 'Reporting'],
    },
    {
      icon: '🧾',
      title: 'Tax Planning',
      description: 'Integrated tax planning tools and resources for tax professionals.',
      features: ['Tax calendars', 'Compliance tracking', 'Document templates', 'Deadline alerts'],
    },
  ]

  return (
    <div className="space-y-16">
      {/* Hero Section */}
      <section className="max-w-7xl mx-auto px-4 py-16">
        <h1 className="text-5xl font-bold text-gray-900 mb-6">Our Services</h1>
        <p className="text-xl text-gray-600 max-w-3xl">
          Comprehensive solutions designed to address every aspect of modern legal practice.
        </p>
      </section>

      {/* Services Grid */}
      <section className="max-w-7xl mx-auto px-4">
        <div className="grid grid-cols-2 gap-8">
          {services.map((service, index) => (
            <div key={index} className="bg-white border rounded-lg p-8 hover:shadow-lg transition">
              <div className="text-5xl mb-4">{service.icon}</div>
              <h3 className="text-2xl font-bold mb-3">{service.title}</h3>
              <p className="text-gray-600 mb-6">{service.description}</p>
              <div className="mb-6">
                <p className="font-semibold text-sm text-gray-700 mb-3">Key Features:</p>
                <ul className="space-y-2">
                  {service.features.map((feature, idx) => (
                    <li key={idx} className="flex items-center text-sm text-gray-600">
                      <span className="w-2 h-2 bg-blue-600 rounded-full mr-3"></span>
                      {feature}
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* Pricing Section */}
      <section className="bg-gray-50 py-16">
        <div className="max-w-7xl mx-auto px-4">
          <h2 className="text-4xl font-bold text-center mb-12">Simple Transparent Pricing</h2>
          <div className="grid grid-cols-3 gap-8">
            {[
              { name: 'Starter', price: '$99', users: 'Up to 5 users', features: ['Document Management', 'Client Management', 'Basic Reports'] },
              { name: 'Professional', price: '$299', users: 'Up to 20 users', features: ['All Starter features', 'Time & Billing', 'Advanced Analytics', 'Priority Support'] },
              { name: 'Enterprise', price: 'Custom', users: 'Unlimited users', features: ['All features', 'Custom integrations', 'Dedicated support', 'SLA guarantee'] },
            ].map((plan, index) => (
              <div
                key={index}
                className={`rounded-lg p-8 text-center ${
                  index === 1 ? 'bg-blue-600 text-white shadow-lg scale-105' : 'bg-white'
                }`}
              >
                <h3 className={`text-2xl font-bold mb-2 ${index === 1 ? 'text-white' : ''}`}>
                  {plan.name}
                </h3>
                <p className={`text-4xl font-bold mb-2 ${index === 1 ? 'text-white' : ''}`}>
                  {plan.price}
                </p>
                <p className={`text-sm mb-6 ${index === 1 ? 'text-blue-100' : 'text-gray-600'}`}>
                  {plan.users}
                </p>
                <ul className={`space-y-3 mb-8 text-left ${index === 1 ? 'text-blue-50' : 'text-gray-600'}`}>
                  {plan.features.map((feature, idx) => (
                    <li key={idx} className="flex items-center">
                      <span className={`w-2 h-2 rounded-full mr-3 ${index === 1 ? 'bg-white' : 'bg-blue-600'}`}></span>
                      {feature}
                    </li>
                  ))}
                </ul>
                <Link
                  to="/register"
                  className={`inline-block px-6 py-2 rounded-lg font-semibold transition ${
                    index === 1
                      ? 'bg-white text-blue-600 hover:bg-gray-100'
                      : 'border-2 border-blue-600 text-blue-600 hover:bg-blue-50'
                  }`}
                >
                  Get Started
                </Link>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="max-w-7xl mx-auto px-4 py-16 text-center">
        <h2 className="text-4xl font-bold mb-6">Schedule a Demo</h2>
        <p className="text-xl text-gray-600 mb-8">
          See how LegalTech can transform your practice. Get a personalized demo from our team.
        </p>
        <Link
          to="/contact"
          className="bg-blue-600 text-white px-8 py-3 rounded-lg hover:bg-blue-700 transition font-semibold inline-block"
        >
          Contact Us Today
        </Link>
      </section>
    </div>
  )
}
