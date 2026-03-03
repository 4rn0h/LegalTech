import { Outlet } from 'react-router-dom'
import PublicHeader from './PublicHeader'

export default function PublicLayout() {
  return (
    <div className="flex flex-col min-h-screen bg-white">
      <PublicHeader />
      <main className="flex-1">
        <Outlet />
      </main>
      <footer className="bg-gray-900 text-white mt-20">
        <div className="max-w-7xl mx-auto px-4 py-12">
          <div className="grid grid-cols-4 gap-8 mb-8">
            <div>
              <h3 className="text-xl font-bold mb-4">LegalTech</h3>
              <p className="text-gray-400">Your trusted legal technology partner</p>
            </div>
            <div>
              <h4 className="font-semibold mb-4">Company</h4>
              <ul className="space-y-2 text-gray-400">
                <li><a href="/about" className="hover:text-white">About Us</a></li>
                <li><a href="/services" className="hover:text-white">Services</a></li>
                <li><a href="#" className="hover:text-white">Blog</a></li>
                <li><a href="#" className="hover:text-white">Careers</a></li>
              </ul>
            </div>
            <div>
              <h4 className="font-semibold mb-4">Legal</h4>
              <ul className="space-y-2 text-gray-400">
                <li><a href="/privacy" className="hover:text-white">Privacy Policy</a></li>
                <li><a href="/terms" className="hover:text-white">Terms of Service</a></li>
                <li><a href="#" className="hover:text-white">Cookie Policy</a></li>
              </ul>
            </div>
            <div>
              <h4 className="font-semibold mb-4">Contact</h4>
              <ul className="space-y-2 text-gray-400">
                <li><a href="/contact" className="hover:text-white">Contact Us</a></li>
                <li><a href="mailto:info@legaltech.com" className="hover:text-white">info@legaltech.com</a></li>
                <li><a href="tel:+1234567890" className="hover:text-white">+1 (234) 567-890</a></li>
              </ul>
            </div>
          </div>
          <div className="border-t border-gray-800 pt-8 text-center text-gray-400">
            <p>&copy; 2026 LegalTech. All rights reserved.</p>
          </div>
        </div>
      </footer>
    </div>
  )
}
