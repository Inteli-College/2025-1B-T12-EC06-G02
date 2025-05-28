'use client'

import { useEffect, useState } from 'react'
import { supabase } from '../../backend/lib/supabase'
import MiniGaleria from "../(components)/miniGaleria"
import { Button } from "../(components)/ui/button";
import IconeServ from "../../../public/serv-icon.png";


export default function ImagensApp() {
  const [imagens, setImagens] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  
    async function buscarImagensApp() {
        try {
        setLoading(true)
        setError(null)

        const { data, error } = await supabase
          .from('images')
          .select('file_path')
          .eq('app', true)

        if (error) throw error

        const imagensComUrl = data.map((img) => {
          const { data: publicUrlData } = supabase
            .storage
            .from('imagens')
            .getPublicUrl(img.file_path)

          return {
            id: img.id,
            path: img.file_path,
            previewUrl: publicUrlData.publicUrl,
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

  return (
    <div className="space-y-4 w-full flex items-center flex-col">
      <Button
        className="!h-auto w-1/3 !p-4 bg-[#00C939] text-white !text-2xl rounded hover:bg-[#00b033] transition-colors"
        
        onClick={buscarImagensApp}
      >
        <img src={IconeServ.src}></img>Carregar do servidor
      </Button>
      {error && <p className="text-red-600">{error}</p>}
      {!loading && <MiniGaleria images={imagens} />}
    </div>
  )
}
