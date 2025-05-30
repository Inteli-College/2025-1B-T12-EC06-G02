'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { supabase } from '../../backend/lib/supabase'
<<<<<<< HEAD
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
=======
import { Button } from "../(components)/ui/button";
import IconeServ from "../../../public/serv-icon.png";
import { useDadosStore } from '../(stores)/useDados';
import { useRouter } from 'next/navigation';


export default function ImagensApp({name}) {
  const [imagens, setImagens] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const router = useRouter()
  
    async function buscarImagensApp() {
        try {
        setLoading(true)
        setError(null)

        const { data, error } = await supabase
          .from('images')
          .select('file_path, id')
          .eq('app', true)
>>>>>>> 0c7be7a3ede4fcfba1acb5dc794f0c3ed7e536f2

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

<<<<<<< HEAD
      const dadosParaEnviar = {
        name: nome,
        selection: "servidor",
        images: imagensComUrl,
=======
        console.log('Imagens encontradas:', imagensComUrl)

        const dadosParaEnviar = { name, selection:'servidor', images: imagensComUrl };
        useDadosStore.getState().setDados(dadosParaEnviar);
        router.push("/upload");

      } catch (err) {
        console.error('Erro ao buscar imagens:', err.message)
        setError('Erro ao carregar imagens.')
      } finally {
        setLoading(false)
>>>>>>> 0c7be7a3ede4fcfba1acb5dc794f0c3ed7e536f2
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
        className="!h-auto w-1/3 !p-4 bg-[#00C939] text-white !text-2xl rounded hover:bg-[#00b033] transition-colors"
<<<<<<< HEAD
=======
        color = "#00C939"
>>>>>>> 0c7be7a3ede4fcfba1acb5dc794f0c3ed7e536f2
        onClick={buscarImagensApp}
        color = '#00C939'
      >
        <Image src={IconeServ} alt="Ícone Servidor" width={24} height={24} className="mr-2" />
        Carregar do servidor
      </Button>
      {error && <p className="text-red-600">{error}</p>}
    </div>
  )
}
