"use client";
import "../globals.css";
import { Inter } from "next/font/google";
import { useEffect, useState } from "react";
import Layout from "../(components)/Layout";
import { Button } from "../(components)/ui/button";
import Resultado from "../(components)/Resultado";
import IconeBaixar from "../../../public/icone-baixar.png";
import { useRouter } from "next/navigation";
import { supabase } from "../../backend/lib/supabase";
import { useDadosStore } from "../(stores)/useDados";
import Loading from "../(components)/Loading";
import AuthGuard from "../(components)/AuthGuard";

const inter = Inter({
  subsets: ["latin"],
  variable: "--font-inter",
  display: "swap",
});

export default function Result() {
  const router = useRouter();
  const [pdfGerado, setPdfGerado] = useState(false);

  async function urlToFile(previewUrl, filename) {
    const res = await fetch(previewUrl);
    const blob = await res.blob();
    return new File([blob], filename, { type: blob.type });
  }

  useEffect(() => {
    async function gerarPdf() {
      const formData = new FormData();

      // Helper para processar cada grupo de imagens
      async function appendImages(key, images) {
        for (let i = 0; i < images.length; i++) {
          const img = images[i];
          const previewUrl = img.previewUrl;
          const filename = img.path || `img-${i}.jpg`;

          const file = await urlToFile(previewUrl, filename);
          formData.append(key, file);
        }
      }

      await appendImages("termica", termicaImgs);
      await appendImages("retracao", retracaoImgs);
      
      const res = await fetch("/api/gerar-pdf", {
        method: "POST",
        body: formData,
      });

      const data = await res.json();
      const nomeArquivo = `relatorio-${Date.now()}.pdf`;
      const file = data.buffer;

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
        .upload(nomeArquivo, pdfBlob);

      if (error) {
        console.error("Erro ao fazer upload:", error);
      }

      // Salvar no estado global
      const dadosParaEnviar = { preview: nomeArquivo };
      useDadosStore.getState().setDados(dadosParaEnviar);

      // Marcar PDF como gerado
      setPdfGerado(true);
    }

    gerarPdf();
  }, []);

  function handleClick() {
    const link = document.createElement("a");
    link.href = pdfUrl;
    link.download = `relatorio-${Date.now()}.pdf`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  }

  function handleHome() {
    router.push("/home");
  }

  function handlePreview() {
    router.push("/preview");
  }

  return (
    <AuthGuard>
      <div className={inter.className}>
        <Layout>
          {!pdfGerado ? (
            <Loading />
          ) : (
            <>
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
                disabled={!pdfGerado}
              >
                <img src={IconeBaixar.src} className="h-6" />
                Baixar Relatório na Íntegra
              </Button>
              <div className="flex flex-row gap-4">
                <Button
                  className="!h-auto !p-2 text-white !text-xl rounded hover:bg-[#00b033] transition-colors"
                  onClick={handleHome}
                  disabled={!pdfGerado}
                >
                  Voltar para home
                </Button>
                <Button
                  className="!h-auto !p-2 text-white !text-xl rounded hover:bg-[#00b033] transition-colors"
                  onClick={handlePreview}
                  disabled={!pdfGerado}
                >
                  Preview do relatório
                </Button>
              </div>
            </>
          )}
        </Layout>
      </div>
    </AuthGuard>
  );
}
