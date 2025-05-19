"use client";

import { Upload, History, Wifi } from "lucide-react";
import { Button } from "../../../components/ui/button";
import BackgroundImage from "../../../components/BackgroundImage";
import Navbar from "../../../components/Navbar";
import Image from "next/image";

export default function Dashboard({ userName = "Usuário" }) {
  return (
    <BackgroundImage>
      <Navbar />

      <div className="w-full max-w-3xl bg-white/80 backdrop-blur-sm p-8 md:p-10 rounded-lg shadow-xl space-y-6">
        {/* Conectar com drone
        <div className="flex justify-center">
          <Button variant="primary" className="text-white text-lg font-medium px-6 py-4">
            <Wifi className="mr-2 h-5 w-5" />
            Conectar com o drone
          </Button>
        </div> */}

        {/* Saudação */}
        <h1 className="text-center text-[#434343] text-4xl font-semibold">
          Olá, {userName}
        </h1>

        {/* Upload de imagens */}
        <div className="flex gap-3 items-center justify-center flex-wrap">
          {/* Imagens mockadas */}
          {["/1.jpg", "/2.jpg", "/3.jpg"].map((src, i) => (
            <div key={i} className="relative w-24 h-24 border rounded overflow-hidden bg-white shadow">
              <Image src={src} alt={`Imagem ${i + 1}`} fill className="object-cover" />
              <span className="absolute bottom-1 left-1 text-xs bg-white px-1 rounded text-gray-700">.jpg</span>
            </div>
          ))}

          {/* Botão de upload */}
          <div className="w-24 h-24 flex items-center justify-center border-2 border-dashed rounded text-3xl font-bold text-gray-400 cursor-pointer hover:bg-gray-100">
            +
          </div>
        </div>

        {/* Dropdown do modelo */}
        <div className="flex justify-center">
          <select className="px-4 py-2 border rounded text-gray-700">
            <option>Modelo de I.A. 01</option>
            <option>Modelo de I.A. 02</option>
          </select>
        </div>

        {/* Botão de Iniciar Processamento */}
        <div className="flex justify-end">
          <Button variant="success" className="px-6 py-4 text-white text-lg font-semibold">
            Iniciar Processamento
          </Button>
        </div>

        {/* Botão de Histórico */}
        <div className="flex justify-center">
          <Button variant="primary" className="px-6 py-4 text-white text-lg font-medium">
            <History className="mr-2 h-5 w-5" />
            Histórico
          </Button>
        </div>
      </div>
    </BackgroundImage>
  );
}