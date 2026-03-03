import { useState, useEffect } from 'react'
import { useParams } from 'react-router-dom'

interface Interaction {
  id: string
  type: string
  description: string
  date: string
  user: string
  status: string
}

interface ClientDetail {
  id: string
  name: string
  email: string
  phone: string
  address: string
  status: string
}

export default function ClientDetail() {
  const { id } = useParams<{ id: string }>()
  const [client, setClient] = useState<ClientDetail | null>(null)
  const [interactions, setInteractions] = useState<Interaction[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchClientData = async () => {
      try {
        const [clientRes, interactionsRes] = await Promise.all([
          fetch(`/api/v1/clients/${id}/`, {
            headers: {
              Authorization: `Bearer ${localStorage.getItem('access_token')}`,
            },
          }),
          fetch(`/api/v1/clients/${id}/interactions/`, {
            headers: {
              Authorization: `Bearer ${localStorage.getItem('access_token')}`,
            },
          }),
        ])

        const clientData = await clientRes.json()
        const interactionsData = await interactionsRes.json()

        setClient(clientData)
        setInteractions(interactionsData.results || interactionsData)
      } catch (error) {
        console.error('Error fetching client data:', error)
      } finally {
        setLoading(false)
      }
    }

    if (id) {
      fetchClientData()
    }
  }, [id])

  if (loading) {
    return <div className="p-8">Loading client details...</div>
  }

  if (!client) {
    return <div className="p-8 text-red-600">Client not found</div>
  }

  return (
    <div className="p-8">
      <button className="text-blue-600 hover:underline mb-6">← Back to Clients</button>

      <div className="grid grid-cols-3 gap-8 mb-8">
        {/* Client Info Card */}
        <div className="col-span-1 border rounded-lg p-6">
          <h1 className="text-2xl font-bold mb-4">{client.name}</h1>
          <div className="space-y-3 text-sm">
            <div>
              <label className="font-semibold text-gray-600">Email:</label>
              <p>{client.email}</p>
            </div>
            <div>
              <label className="font-semibold text-gray-600">Phone:</label>
              <p>{client.phone}</p>
            </div>
            <div>
              <label className="font-semibold text-gray-600">Address:</label>
              <p>{client.address}</p>
            </div>
            <div>
              <label className="font-semibold text-gray-600">Status:</label>
              <p>
                <span
                  className={`px-3 py-1 rounded-full text-xs font-semibold ${
                    client.status === 'active'
                      ? 'bg-green-100 text-green-800'
                      : 'bg-yellow-100 text-yellow-800'
                  }`}
                >
                  {client.status}
                </span>
              </p>
            </div>
          </div>
          <div className="mt-6 flex gap-2">
            <button className="flex-1 bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700">
              Edit
            </button>
            <button className="flex-1 border border-gray-300 px-4 py-2 rounded hover:bg-gray-50">
              Message
            </button>
          </div>
        </div>

        {/* Quick Stats */}
        <div className="col-span-2 space-y-4">
          <div className="border rounded-lg p-6">
            <h2 className="text-xl font-bold mb-4">Quick Stats</h2>
            <div className="grid grid-cols-3 gap-4">
              <div className="text-center">
                <div className="text-3xl font-bold text-blue-600">12</div>
                <p className="text-gray-600 text-sm">Documents</p>
              </div>
              <div className="text-center">
                <div className="text-3xl font-bold text-green-600">5</div>
                <p className="text-gray-600 text-sm">Interactions</p>
              </div>
              <div className="text-center">
                <div className="text-3xl font-bold text-orange-600">$15,000</div>
                <p className="text-gray-600 text-sm">Total Transactions</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Interactions Timeline */}
      <div className="border rounded-lg p-6">
        <div className="flex justify-between items-center mb-6">
          <h2 className="text-xl font-bold">Interaction History</h2>
          <button className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700">
            Add Interaction
          </button>
        </div>

        <div className="space-y-4">
          {interactions.length === 0 ? (
            <div className="text-center text-gray-500 py-8">No interactions recorded</div>
          ) : (
            interactions.map((interaction) => (
              <div key={interaction.id} className="border rounded p-4 hover:bg-gray-50">
                <div className="flex justify-between items-start">
                  <div>
                    <h3 className="font-semibold text-lg">{interaction.type}</h3>
                    <p className="text-gray-600">{interaction.description}</p>
                  </div>
                  <div className="text-right text-sm text-gray-500">
                    <p>{new Date(interaction.date).toLocaleDateString()}</p>
                    <p className="text-gray-400">{interaction.user}</p>
                  </div>
                </div>
                <div className="mt-2">
                  <span
                    className={`px-3 py-1 rounded-full text-xs ${
                      interaction.status === 'completed'
                        ? 'bg-green-100 text-green-800'
                        : 'bg-yellow-100 text-yellow-800'
                    }`}
                  >
                    {interaction.status}
                  </span>
                </div>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  )
}
