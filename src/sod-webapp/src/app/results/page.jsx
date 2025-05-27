"use client";
import "../globals.css";
import { Inter } from "next/font/google";

const inter = Inter({
  subsets: ["latin"],
  variable: "--font-inter",
  display: "swap",
});

import { useState } from "react";
import Layout from "../(components)/Layout";
import { Button } from "../(components)/ui/button";
import Resultado from "../(components)/Resultado";
import IconeBaixar from "../../../public/icone-baixar.png";
import { useRouter } from "next/navigation";
import { supabase } from "../../backend/lib/supabase";
import { useDadosStore } from "../(stores)/useDados";


export default function Result() {
  const router = useRouter();
  const [pdfUrl, setPdfUrl] = useState("");

  async function handleClick() {
    const res = await fetch("/api/gerar-pdf", {
      method: "POST",
      body: JSON.stringify({ nome: "Gov da Silva" }),
      headers: { "Content-Type": "application/json" },
    });

    const data = await res.json();
    setPdfUrl(data.url);
    const file = data.buffer;
    console.log(file)

    function base64ToBlob(base64, mimeType = "application/pdf") {
      const byteCharacters = atob(base64);
      const byteNumbers = new Array(byteCharacters.length);
      for (let i = 0; i < byteCharacters.length; i++) {
        byteNumbers[i] = byteCharacters.charCodeAt(i);
      }
      const byteArray = new Uint8Array(byteNumbers);
      return new Blob([byteArray], { type: mimeType });
    }

    const pdfBlob = base64ToBlob(file);

    const { error } = await supabase.storage
      .from("relatorios")
      .upload(`relatorio-${Date.now()}.pdf`, pdfBlob);

    if (error) {
      console.error("Erro ao fazer upload:", error);
    }

    // Forçar download
    const link = document.createElement("a");
    link.href = data.url;
    link.download = `relatorio-${Date.now()}.pdf`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);

    // Mandar para o preview
    const dadosParaEnviar = {preview: pdfUrl};
    useDadosStore.getState().setDados(dadosParaEnviar);
  }

  function handleHome() {
    router.push("/home");
  }

  function handlePreview(){
    router.push("/preview");
  }

  return (
    <div className={inter.className}>
      <Layout>
        <h1 className="text-[#434343] text-4xl text-center mx-auto md:text-5xl font-medium leading-tight">
          Principais Insights do Relatório
        </h1>
        <div
          id="resultados"
          className="flex flex-row justify-between gap-3 w-1/2"
        >
          <Resultado valor="03" label="Fissuras de Retração" />
          <Resultado valor="02" label="Fissuras Térmicas" />
        </div>
        <Button
          className="!h-auto w-1/3 !p-4 bg-[#00C939] text-white !text-2xl rounded hover:bg-[#00b033] transition-colors"
          color="#00C939"
          onClick={handleClick}
        >
          <img src={IconeBaixar.src} className="h-6"></img>Baixar Relatório na
          Íntegra
        </Button>
        <div className="flex flex-row gap-4">
          <Button
            className="!h-auto !p-2 text-white !text-xl rounded hover:bg-[#00b033] transition-colors"
            onClick={handleHome}
          >
            Voltar para home
          </Button>
          <Button
            className="!h-auto !p-2 text-white !text-xl rounded hover:bg-[#00b033] transition-colors"
            onClick={handlePreview}
          >
            Preview do relatório
          </Button>
        </div>
      </Layout>
    </div>
  );
}
