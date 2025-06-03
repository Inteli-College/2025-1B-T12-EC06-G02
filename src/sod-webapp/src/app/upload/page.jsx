// src/app/upload/page.jsx
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
import MiniGaleria from "../(components)/miniGaleria";
import OrganizadorImagens from "../(components)/OrganizadorImagens";
import { Button } from "../(components)/ui/button";
import { useRouter } from "next/navigation";
import Loading from "../(components)/Loading";

export default function Upload() {
  const { name, selection, images } = useDadosStore((state) => state.dados);
  const [imagens, setImagens] = useState(images);
  const router = useRouter();
  const [loading, setLoading] = useState(false);
  const [mostrarOrganizador, setMostrarOrganizador] = useState(false);

  async function handleOrganizadorSubmit(gruposOrganizados) {
    setLoading(true);
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

      // Processa cada grupo
      const gruposProcessados = await Promise.all(
        gruposOrganizados.map(async (grupo) => {
          const imagensConvertidas = await Promise.all(
            grupo.imagens.map(async (img) => {
              if (img.previewUrl?.startsWith("blob:")) {
                const base64 = await blobToBase64(img.previewUrl);
                return {
                  ...img,
                  previewUrl: base64,
                };
              }
              return img;
            })
          );

          return {
            andar: grupo.andar,
            direcao: grupo.direcao,
            imagens: imagensConvertidas,
          };
        })
      );

      const response = await fetch("http://127.0.0.1:5000/api/ia/classify", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          grupos: gruposProcessados, // Enviando os grupos organizados
        }),
      });

      if (!response.ok) {
        throw new Error(`Erro na requisição: ${response.status}`);
      }

      const resultadoIA = await response.json();

      const dadosParaEnviar = { name, resultadoIA, gruposOrganizados };
      useDadosStore.getState().setDados(dadosParaEnviar);
      router.push("/results");

      setMostrarOrganizador(false);
    } catch (error) {
      console.error("Erro ao enviar dados para o backend:", error);
      alert("Erro ao processar imagens. Por favor, tente novamente.");
    } finally {
      setLoading(false);
    }
  }

  function handleClick() {
    setMostrarOrganizador(true);
  }

  return (
    <div className={inter.className}>
      <BackgroundImage>
        <Navbar />
        <Card>
          {loading ? (
            <Loading />
          ) : (
            <>
              <Usuario nome={name} />
              <MiniGaleria images={imagens} handleImages={setImagens} />

              <Button 
                color="#00C939" 
                onClick={handleClick}
                className="bg-[#00C939] hover:bg-[#00b033] text-white"
              >
                Organizar e Processar
              </Button>

              {mostrarOrganizador && (
                <OrganizadorImagens
                  images={imagens}
                  onSubmit={handleOrganizadorSubmit}
                  onClose={() => setMostrarOrganizador(false)}
                />
              )}
            </>
          )}
        </Card>
      </BackgroundImage>
    </div>
  );
}