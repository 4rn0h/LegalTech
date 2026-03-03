export default function AboutUs() {
  return (
    <div className="space-y-16">
      {/* Hero Section */}
      <section className="max-w-7xl mx-auto px-4 py-16">
        <h1 className="text-5xl font-bold text-gray-900 mb-6">About LegalTech</h1>
        <p className="text-xl text-gray-600 max-w-3xl">
          We're on a mission to revolutionize the legal industry by making sophisticated
          technology accessible and affordable for law firms of all sizes.
        </p>
      </section>

      {/* Mission Section */}
      <section className="bg-blue-50 py-16">
        <div className="max-w-7xl mx-auto px-4">
          <h2 className="text-4xl font-bold mb-8">Our Mission</h2>
          <div className="grid grid-cols-3 gap-8">
            <div>
              <h3 className="text-2xl font-bold mb-4 text-blue-600">Empower</h3>
              <p className="text-gray-700">
                We empower legal professionals with tools that streamline workflows and increase
                efficiency, allowing them to focus on what matters most: their clients.
              </p>
            </div>
            <div>
              <h3 className="text-2xl font-bold mb-4 text-blue-600">Innovate</h3>
              <p className="text-gray-700">
                We continuously innovate and improve our platform with cutting-edge technology
                and features based on real-world legal practice needs.
              </p>
            </div>
            <div>
              <h3 className="text-2xl font-bold mb-4 text-blue-600">Secure</h3>
              <p className="text-gray-700">
                We maintain the highest standards of security and confidentiality, ensuring
                sensitive legal information is always protected.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Team Section */}
      <section className="max-w-7xl mx-auto px-4 py-16">
        <h2 className="text-4xl font-bold mb-12">Our Team</h2>
        <div className="grid grid-cols-4 gap-8">
          {[
            { name: 'John Smith', role: 'CEO & Co-founder', image: '👨‍💼' },
            { name: 'Sarah Johnson', role: 'CTO & Co-founder', image: '👩‍💻' },
            { name: 'Michael Chen', role: 'Head of Legal', image: '👨‍⚖️' },
            { name: 'Emma Williams', role: 'Head of Customer Success', image: '👩‍💼' },
          ].map((member) => (
            <div key={member.name} className="bg-white rounded-lg shadow p-8 text-center">
              <div className="text-6xl mb-4">{member.image}</div>
              <h3 className="text-xl font-bold">{member.name}</h3>
              <p className="text-gray-600">{member.role}</p>
            </div>
          ))}
        </div>
      </section>

      {/* Stats Section */}
      <section className="bg-gray-900 text-white py-16">
        <div className="max-w-7xl mx-auto px-4">
          <div className="grid grid-cols-4 gap-8 text-center">
            <div>
              <div className="text-5xl font-bold mb-2">500+</div>
              <p className="text-gray-400">Active Firms</p>
            </div>
            <div>
              <div className="text-5xl font-bold mb-2">10,000+</div>
              <p className="text-gray-400">Users</p>
            </div>
            <div>
              <div className="text-5xl font-bold mb-2">1M+</div>
              <p className="text-gray-400">Documents Managed</p>
            </div>
            <div>
              <div className="text-5xl font-bold mb-2">99.9%</div>
              <p className="text-gray-400">Uptime</p>
            </div>
          </div>
        </div>
      </section>

      {/* Values Section */}
      <section className="max-w-7xl mx-auto px-4 py-16">
        <h2 className="text-4xl font-bold mb-12">Our Values</h2>
        <div className="space-y-4">
          <div className="border-l-4 border-blue-600 pl-6 py-4">
            <h3 className="text-2xl font-bold mb-2">Client-Centric</h3>
            <p className="text-gray-600">We prioritize the needs of our users and continuously seek their feedback to improve our platform.</p>
          </div>
          <div className="border-l-4 border-blue-600 pl-6 py-4">
            <h3 className="text-2xl font-bold mb-2">Integrity</h3>
            <p className="text-gray-600">We operate with transparency and honesty in all our interactions and business practices.</p>
          </div>
          <div className="border-l-4 border-blue-600 pl-6 py-4">
            <h3 className="text-2xl font-bold mb-2">Excellence</h3>
            <p className="text-gray-600">We strive for excellence in everything we do, from product development to customer service.</p>
          </div>
        </div>
      </section>
    </div>
  )
}
