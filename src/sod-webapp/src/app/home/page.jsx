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
import { Button } from "../(components)/ui/button";
import { useState, useEffect, useRef } from "react";
import { supabase } from "../../backend/lib/supabase";
import IconeDoc from "../../../public/doc-icon.png";
import IconeServ from "../../../public/serv-icon.png";
import { useRouter } from "next/navigation";
import { useDadosStore } from "../(stores)/useDados";
import Usuario from "../(components)/Usuario";
import Historico from "../(components)/Historico";
import Loading from "../(components)/Loading";
import Card from "../(components)/Card";

export default function Home() {
  const router = useRouter();
  const [user, setUser] = useState(null);
  const fileInputRef = useRef(null);
  const [selectedImages, setSelectedImages] = useState([]);
  const [selection, setSelection] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    supabase.auth.getUser().then(({ data: { user } }) => {
      setUser(user);
      setIsLoading(false);
    });
  }, []);

  const redirecionar = () => {
    const dadosParaEnviar = { name, selection, images: selectedImages };
    console.log(dadosParaEnviar);
    useDadosStore.getState().setDados(dadosParaEnviar);
    router.push("/upload");
  };

  const handleFileChange = async (e) => {
    const files = Array.from(e.target.files);
    if (files.length > 0) {
      const newImages = files.map((file) => ({
        file,
        previewUrl: URL.createObjectURL(file),
        id: Math.random().toString(36).substring(2, 15),
      }));

      const allImages = [...selectedImages, ...newImages];
      setSelectedImages(allImages);

      // Atualize o store e redirecione usando allImages atualizado:
      const dadosParaEnviar = { name, selection, images: allImages };
      useDadosStore.getState().setDados(dadosParaEnviar);
      router.push("/upload");
    }
  };
  function handleUploadClick() {
    if (fileInputRef.current) {
      fileInputRef.current.click();
      setSelection("upload");
    }
  }

  const name = user?.user_metadata?.name.split(" ")[0] || "Usuário";

  return (
    <div className={inter.className}>
      <BackgroundImage>
        <Navbar />
        <>
          {isLoading ? (
            <Loading />
          ) : (
            <Card>
              <Button
                className="!h-auto w-1/6 !p-2 text-white !text-xl rounded hover:bg-[#00b033] transition-colors mb-6"
                onClick={handleUploadClick}
              >
                <input
                  type="file"
                  accept="image/*"
                  multiple
                  ref={fileInputRef}
                  style={{ display: "none" }}
                  onChange={handleFileChange}
                />
                <img src={IconeDoc.src} className="h-6"></img>Upload Local
              </Button>
              <Usuario nome={name} />
              <div className="w-full flex justify-center flex-col items-center">
                <Button
                  className="!h-auto w-1/3 !p-4 bg-[#00C939] text-white !text-2xl rounded hover:bg-[#00b033] transition-colors"
                  color="#00C939"
                >
                  <img src={IconeServ.src}></img>Upload via Servidor
                </Button>
                <p className="text-[#7E7E7E] text-lg italic mb-6">
                  *O SOD pode cometer erros
                </p>
              </div>
              <Historico />
            </Card>
          )}
        </>
      </BackgroundImage>
    </div>
  );
}
