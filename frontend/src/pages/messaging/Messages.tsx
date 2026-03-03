import { useState, useEffect } from 'react'

interface Message {
  id: string
  sender: string
  recipient: string
  subject: string
  body: string
  timestamp: string
  read: boolean
}

export default function Messages() {
  const [messages, setMessages] = useState<Message[]>([])
  const [loading, setLoading] = useState(true)
  const [selectedMessage, setSelectedMessage] = useState<Message | null>(null)

  useEffect(() => {
    const fetchMessages = async () => {
      try {
        const response = await fetch('/api/v1/messages/', {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('access_token')}`,
          },
        })
        const data = await response.json()
        setMessages(data.results || data)
      } catch (error) {
        console.error('Error fetching messages:', error)
      } finally {
        setLoading(false)
      }
    }

    fetchMessages()
  }, [])

  if (loading) {
    return <div className="p-8">Loading messages...</div>
  }

  return (
    <div className="p-8">
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold">Messages</h1>
        <button className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700">
          New Message
        </button>
      </div>

      <div className="grid grid-cols-3 gap-8">
        {/* Message List */}
        <div className="col-span-1 border rounded-lg">
          <div className="border-b p-4">
            <input
              type="text"
              placeholder="Search messages..."
              className="w-full p-2 border rounded"
            />
          </div>
          <div>
            {messages.length === 0 ? (
              <div className="p-4 text-center text-gray-500">No messages</div>
            ) : (
              messages.map((msg) => (
                <div
                  key={msg.id}
                  onClick={() => setSelectedMessage(msg)}
                  className={`p-4 border-b cursor-pointer hover:bg-gray-50 ${
                    selectedMessage?.id === msg.id ? 'bg-blue-50' : ''
                  }`}
                >
                  <div className="flex justify-between items-start">
                    <h3 className="font-semibold text-sm">{msg.sender}</h3>
                    <span className="text-xs text-gray-500">
                      {new Date(msg.timestamp).toLocaleDateString()}
                    </span>
                  </div>
                  <p className="text-sm text-gray-600 truncate">{msg.subject}</p>
                </div>
              ))
            )}
          </div>
        </div>

        {/* Message Details */}
        <div className="col-span-2 border rounded-lg p-6">
          {selectedMessage ? (
            <div>
              <div className="mb-6">
                <h2 className="text-2xl font-bold mb-2">{selectedMessage.subject}</h2>
                <div className="flex justify-between text-sm text-gray-600">
                  <span>From: {selectedMessage.sender}</span>
                  <span>{new Date(selectedMessage.timestamp).toLocaleString()}</span>
                </div>
              </div>
              <div className="prose prose-sm max-w-none mb-6">
                <p>{selectedMessage.body}</p>
              </div>
              <div className="flex gap-4">
                <button className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700">
                  Reply
                </button>
                <button className="border border-red-600 text-red-600 px-4 py-2 rounded hover:bg-red-50">
                  Delete
                </button>
              </div>
            </div>
          ) : (
            <div className="flex items-center justify-center h-full text-gray-500">
              Select a message to view details
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
