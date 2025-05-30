// src/app/images/upload/page.js
"use client";
import "../globals.css";
import { Inter } from "next/font/google";

const inter = Inter({
  subsets: ["latin"],
  variable: "--font-inter",
  display: "swap",
});

import React from "react";
import BackgroundImage from "../(components)/BackgroundImage";
import Navbar from "../(components)/Navbar";
import { useDadosStore } from "../(stores)/useDados";
import Card from "../(components)/Card";
import Usuario from "../(components)/Usuario";
import MiniGaleria from "../(components)/miniGaleria"
import { Button } from "../(components)/ui/button";
import { useRouter } from "next/navigation";

export default function Upload() {
  const { name, selection, images } = useDadosStore((state) => state.dados);
  const router = useRouter()
  
  console.log(name, selection, images);

  function handleClick(){
    const resultadoIA = [{id:images[0].id,previewUrl:images[0].previewUrl, prev:"termica"}, {id:images[1].id,previewUrl:images[1].previewUrl, prev:"retracao"}]
    const dadosParaEnviar = { name, resultadoIA };
    useDadosStore.getState().setDados(dadosParaEnviar);
    router.push("/results");
  }

  return (
    <div className={inter.className}>
      <BackgroundImage>
        <Navbar />
        <Card>
          <Usuario nome={name} />
          <MiniGaleria images={images} />

          <Button color="#00C939" onClick={handleClick}>
            Iniciar processamento
          
          </Button>

        </Card>
      </BackgroundImage>
    </div>
  );
}
