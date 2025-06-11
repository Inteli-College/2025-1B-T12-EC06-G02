// src/app/images/upload/page.js
"use client";
import "../globals.css";
import { Inter } from "next/font/google";

const inter = Inter({
  subsets: ["latin"],
  variable: "--font-inter",
  display: "swap",
});

import React, { useState } from "react";
import BackgroundImage from "../(components)/BackgroundImage";
import Navbar from "../(components)/Navbar";
import { useDadosStore } from "../(stores)/useDados";
import Card from "../(components)/Card";
import Usuario from "../(components)/Usuario";
import MiniGaleria from "../(components)/miniGaleria"
import { Button } from "../(components)/ui/button";
import { useRouter } from "next/navigation";
import Loading from "../(components)/Loading";
import AuthGuard from "../(components)/AuthGuard";

export default function Upload() {
  const { name, selection, images } = useDadosStore((state) => state.dados);
  const [imagens, setImagens] = useState(images)
  const router = useRouter()
  const [loading, setLoading] = useState(false)
  
async function handleClick() {
  setLoading(true)
  try {
        // Converte um Blob (URL local) para base64
    const blobToBase64 = (blobUrl) => {
      return new Promise((resolve, reject) => {
        fetch(blobUrl)
          .then((res) => res.blob())
          .then((blob) => {
            const reader = new FileReader();
            reader.onloadend = () => resolve(reader.result);
            reader.onerror = reject;
            reader.readAsDataURL(blob);
          });
      });
    };

    // Mapeia as imagens: converte se tiver previewUrl tipo blob:
    const imagensConvertidas = await Promise.all(
      imagens.map(async (img) => {
        if (img.previewUrl?.startsWith("blob:")) {
          const base64 = await blobToBase64(img.previewUrl);
          return {
            ...img,
            previewUrl: base64, // substitui o blob por base64
          };
        }
        return img; // mantém a imagem original se não for blob
      })
    );
    const response = await fetch("http://127.0.0.1:5000/api/ia/classify", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        images: imagensConvertidas,
      }),
    });

    if (!response.ok) {
      throw new Error(`Erro na requisição: ${response.status}`);
    }

    const resultadoIA = await response.json();

    const dadosParaEnviar = { name, resultadoIA };
    useDadosStore.getState().setDados(dadosParaEnviar);
    router.push("/results");

  } catch (error) {
    console.error("Erro ao enviar dados para o backend:", error);
  }
}


  return (
    <AuthGuard>
    <div className={inter.className}>
      <BackgroundImage>
        <Navbar />
        <Card>
          { loading ? (<Loading />) :(<>
          <Usuario nome={name} />
          <MiniGaleria images={imagens} handleImages={setImagens} />

          <Button variant="success" onClick={handleClick}>
            Iniciar processamento
          
          </Button></>) }

        </Card>
      </BackgroundImage>
    </div>
  </AuthGuard>);
}
