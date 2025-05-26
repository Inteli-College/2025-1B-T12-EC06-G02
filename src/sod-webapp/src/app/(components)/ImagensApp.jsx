'use client'

import { useEffect, useState } from 'react'
import { supabase } from '@/utils/supabase/client'

export default function ImagensApp() {
  const [imagens, setImagens] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => { 
    async function buscarImagensApp() {
      try {
        setLoading(true)
        setError(null)

        const { data, error } = await supabase
          .from('imagem')
          .select('path')
          .eq('app', true)

        if (error) throw error

        const imagensComUrl = data.map((img) => {
          const { data: publicUrlData } = supabase
            .storage
            .from('Imagens-de-Fissuras')
            .getPublicUrl(img.path)

          return {
            path: img.path,
            url: publicUrlData.publicUrl,
          }
        })

        console.log('Imagens encontradas:', imagensComUrl)

        setImagens(imagensComUrl)
      } catch (err) {
        console.error('Erro ao buscar imagens:', err.message)
        setError('Erro ao carregar imagens.')
      } finally {
        setLoading(false)
      }
    }

    buscarImagensApp()
  }, [])

  return (
    <div className="space-y-4">
      <h2 className="text-xl font-semibold">Imagens com app = true</h2>

      {loading && <p>Carregando imagens...</p>}
      {error && <p className="text-red-600">{error}</p>}

      <div className="grid grid-cols-2 gap-4">
        {imagens.map((img, idx) => (
          <img
            key={idx}
            src={img.url}
            alt={`Imagem ${idx}`}
            className="rounded-md shadow"
          />
        ))}
      </div>
    </div>
  )
}
