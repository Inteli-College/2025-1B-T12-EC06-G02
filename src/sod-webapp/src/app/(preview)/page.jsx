"use client";

import { useEffect, useState } from "react";
import "../globals.css";
import { Inter } from "next/font/google";
import { Button } from "../(components)/ui/button";
import Card from "../(components)/Card";
import { useDadosStore } from "../(stores)/useDados";
import Layout from "../(components)/Layout";
import AuthGuard from "../(components)/AuthGuard";
import { supabase } from "../../backend/lib/supabase";

const inter = Inter({
  subsets: ["latin"],
  variable: "--font-inter",
  display: "swap",
});

export default function Preview({ handlePreview }) {
  const dados = useDadosStore((state) => state.dados);
  const [signedUrl, setSignedUrl] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchSignedUrl() {
      if (!dados?.preview) return;

      const { data, error } = await supabase.storage
        .from("relatorios")
        .createSignedUrl(dados.preview, 3600); // 1h de validade

      if (error) {
        console.error("Erro ao gerar URL assinada:", error.message);
        setSignedUrl(null);
      } else {
        setSignedUrl(data?.signedUrl || null);
      }
      setLoading(false);
    }

    fetchSignedUrl();
  }, [dados]);

  return (
    <>
      {loading ? (
        <p>Carregando relatório...</p>
      ) : signedUrl ? (
        <embed
          src={signedUrl}
          type="application/pdf"
          width="100%"
          height="600px"
        />
      ) : (
        <p>Não foi possível carregar o PDF.</p>
      )}
      <Button onClick={() => handlePreview(false)}>Voltar</Button>
    </>
  );
}
