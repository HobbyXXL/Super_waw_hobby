'use client'
import { useEffect, useState } from 'react'

interface Hobby {
  id: number
  name: string
  category: string
  description: string | null
  created_at: string | null  // ← строка, а не datetime — чтобы избежать ошибки
}

export default function HobbiesPage() {
  const [hobbies, setHobbies] = useState<Hobby[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchHobbies = async () => {
      try {
        const res = await fetch('http://localhost:8000/hobbies')
        if (!res.ok) throw new Error('Failed to load hobbies')
        const data: Hobby[] = await res.json()
        setHobbies(data)
      } catch (err) {
        console.error(err)
      } finally {
        setLoading(false)
      }
    }
    fetchHobbies()
  }, [])

  if (loading) return <div className="p-6">Загрузка...</div>

  return (
    <div className="p-6 max-w-4xl mx-auto">
      <h1 className="text-3xl font-bold mb-6">Твои хобби</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {hobbies.map((hobby) => (
          <div key={hobby.id} className="border rounded-lg p-4 shadow-sm">
            <h2 className="font-semibold text-lg">{hobby.name}</h2>
            <p className="text-gray-600 text-sm">{hobby.category}</p>
            {hobby.description && (
              <p className="mt-2 text-gray-800 text-sm line-clamp-2">{hobby.description}</p>
            )}
          </div>
        ))}
      </div>
    </div>
  )
}
