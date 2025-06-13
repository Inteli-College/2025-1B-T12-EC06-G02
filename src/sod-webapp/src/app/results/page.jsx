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
import Preview from "../(preview)/page";

const inter = Inter({
  subsets: ["latin"],
  variable: "--font-inter",
  display: "swap",
});

export default function Result() {
  const router = useRouter();
  const [pdfGerado, setPdfGerado] = useState(false);
  const [pdfUrl, setPdfUrl] = useState("");
  const [nTermicas, setNTermicas] = useState(0);
  const [nRetracao, setNRetracao] = useState(0);
  const [previewClick, setPreviewClick] = useState(false);

  async function urlToFile(previewUrl, filename) {
    const res = await fetch(previewUrl);
    const blob = await res.blob();
    return new File([blob], filename, { type: blob.type });
  }
  const { resultadoIA, pdf } = useDadosStore((state) => state.dados);

  useEffect(() => {
    async function gerarPdf() {
      try {
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

        if (!resultadoIA || !Array.isArray(resultadoIA)) {
          console.error("Dados de IA inválidos:", resultadoIA);
          throw new Error("Dados de classificação inválidos");
        }

        const termicaImg = resultadoIA
          .filter((item) => item.prev === "termica")
          .map((item) => ({
            id: item.id,
            previewUrl: item.previewUrl,
          }));

        setNTermicas(termicaImg.length);

        const retracaoImg = resultadoIA
          .filter((item) => item.prev === "retracao")
          .map((item) => ({
            id: item.id,
            previewUrl: item.previewUrl,
          }));

        setNRetracao(retracaoImg.length);
        
        // Adicionar metadados do relatório se disponível
        const metadata = {
          cliente: "Cliente de Exemplo",
          cnpj: "XX.XXX.XXX/0001-XX",
          endereco: "Endereço da Obra",
          naturezaTrabalho: "Análise de Fissuração em Concreto",
          referencia: "Projeto SOD-Control",
        };
        
        Object.entries(metadata).forEach(([key, value]) => {
          formData.append(key, value);
        });

        await appendImages("termica", termicaImg);
        await appendImages("retracao", retracaoImg);

        const res = await fetch("/api/gerar-pdf", {
          method: "POST",
          body: formData,
        });

        // Check if response is successful before parsing JSON
        if (!res.ok) {
          const errorText = await res.text();
          console.error("Error response from server:", errorText);
          throw new Error(`Server error: ${res.status} - ${errorText}`);
        }

        // Check if response has content
        const contentType = res.headers.get("content-type");
        if (!contentType || !contentType.includes("application/json")) {
          const responseText = await res.text();
          console.error("Non-JSON response:", responseText);
          throw new Error("Server did not return JSON");
        }

        const data = await res.json();

        // Validate that the response contains the expected data
        if (!data.buffer) {
          console.error("Invalid response structure:", data);
          throw new Error("Server response missing PDF buffer");
        }
 
        const nomeArquivo = `relatorio-${Date.now()}.pdf`;
        const file = data.buffer;


        function base64ToBlob(base64, mimeType = "application/pdf") {
          const binary = Uint8Array.from(atob(base64), (char) =>
            char.charCodeAt(0)
          );
          return new Blob([binary], { type: mimeType });
        }

         const pdfBlob = base64ToBlob(file);
         const url = URL.createObjectURL(pdfBlob);
         setPdfUrl(url);

         const { error } = await supabase.storage
           .from("relatorios")
           .upload(nomeArquivo, pdfBlob);

         if (error) {
           console.error("Erro ao fazer upload:", error);
           throw new Error(`Upload error: ${error.message}`);
         }

         // Salvar no estado global
         const dadosParaEnviar = { preview: nomeArquivo };
         useDadosStore.getState().setDados(dadosParaEnviar);

         // Marcar PDF como gerado
         setPdfGerado(true);
       } catch (error) {
         console.error("Error generating PDF:", error);
         alert(`Erro ao gerar o relatório: ${error.message}`);
         // You might want to show an error message to the user here
         // For example, set an error state and display it in the UI
       }
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
    setPreviewClick(true);
  }

  return (
    <AuthGuard>
      <div className={inter.className}>
        <Layout>
          {previewClick ?   (
            <Preview handlePreview={setPreviewClick}/>
          ) : (
            !pdfGerado ? (
              <Loading />
            ) : (
              <>
                <h1 className="text-[#434343] text-2xl md:text-4xl px-3 text-center mx-auto font-medium leading-tight">
                  Principais Insights do Relatório
                </h1>
                <div
                  id="resultados"
                  className="flex flex-row justify-between gap-3 w-3/4 md:w-1/2"
                >
                  <Resultado valor={nRetracao} label="Fissuras de Retração" />
                  <Resultado valor={nTermicas} label="Fissuras Térmicas" />
                </div>
                <Button
                  className="!h-auto !p-4 bg-[#00C939] text-white md:text-2xl rounded hover:bg-[#00b033] transition-colors"
                  onClick={handleClick}
                  color="#00C939"
                  disabled={!pdfGerado}
                >
                  <img src={IconeBaixar.src} className="md:h-6 h-4" />
                  Baixar Relatório na Íntegra
                </Button>
                <div className="flex flex-row gap-2 md:gap-4">
                  <Button
                    className="!h-auto !p-2 text-white text-md md:text-xl rounded transition-colors"
                    onClick={handleHome}
                    disabled={!pdfGerado}
                  >
                    Voltar para home
                  </Button>
                  <Button
                    className="!h-auto !p-2 text-white text-md md:text-xl rounded hover:bg-[#00b033] transition-colors"
                    onClick={handlePreview}
                    disabled={!pdfGerado}
                  >
                    Preview do relatório
                  </Button>
                </div>
              </>
            )
          )}
        </Layout>
      </div>
    </AuthGuard>
  );
}
