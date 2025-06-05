'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { supabase } from '../../backend/lib/supabase'
import { useDadosStore } from '../(stores)/useDados'
import { Button } from "../(components)/ui/button"
import Image from 'next/image'
import IconeServ from "../../../public/serv-icon.png"

export default function ImagensApp({ nome = "Usuário" }) {
  const [error, setError] = useState(null)
  const router = useRouter()

  async function buscarImagensApp() {
    try {
      setError(null)

      const { data, error } = await supabase
        .from('images')
        .select('file_path, id')
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

      const dadosParaEnviar = {
        name: nome,
        selection: "servidor",
        images: imagensComUrl,
      }

      useDadosStore.getState().setDados(dadosParaEnviar)
      router.push("/upload")

    } catch (err) {
      console.error('Erro ao buscar imagens:', err.message)
      setError('Erro ao carregar imagens.')
    } 
  }

  return (
    <div className="space-y-4 w-full flex items-center flex-col">
      <Button
        className="!h-auto !p-4 bg-[#204565] text-white !text-xl !md:text-2xl"
        variant="success"
        onClick={buscarImagensApp}
      >
        <Image src={IconeServ} alt="Ícone Servidor" width={24} height={24} className="mr-2" />
        Carregar do servidor
      </Button>
      {error && <p className="text-red-600">{error}</p>}
    </div>
  )
}
