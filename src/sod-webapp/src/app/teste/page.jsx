import ImagensApp from '@/app/components/ImagensApp'

export default function Page() {
  return (
    <main className="min-h-screen bg-gray-100 p-6">
      <div className="max-w-4xl mx-auto bg-white shadow-md rounded-xl p-6 space-y-6">
        <h1 className="text-3xl font-bold text-gray-800">Teste do Componente ImagensApp</h1>
        <p className="text-gray-600">
          Esta é uma página teste para testar se o componente de busca de imagens do Supabase está funcionando corretamente.
        </p>

        <ImagensApp />
      </div>
    </main>
  )
}
