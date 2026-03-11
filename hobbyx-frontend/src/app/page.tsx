export default function Home() {
  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-4xl font-bold mb-6">HobbyX</h1>
        <p className="text-lg mb-8">Платформа для развития хобби с измеримым прогрессом</p>
        <a
          href="/hobbies"
          className="inline-block bg-blue-600 text-white px-6 py-3 rounded-lg-blue-700 transition"
        >
          Посмотреть хобби
        </a>
      </div>
    </div>
  )
}
