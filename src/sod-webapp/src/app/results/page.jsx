"use client";

import Image from "next/image";
import { useEffect, useState } from "react";
import { supabase } from "../../backend/lib/supabase";
import { Download, History } from "lucide-react";
import { useRouter } from "next/navigation";

export default function Dashboard() {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const router = useRouter();

  useEffect(() => {
    async function fetchLatestResult() {
      setLoading(true);
      setError(null);
      const { data, error } = await supabase
        .from("results")
        .select("*")
        .order("created_at", { ascending: false })
        .limit(1);
      if (error) {
        setError(error.message);
      } else if (data && data.length > 0) {
        setResult(data[0]);
      }
      setLoading(false);
    }
    fetchLatestResult();
  }, []);

  return (
    <div className="relative min-h-screen w-full overflow-hidden">
      {/* Background Image */}
      <div className="absolute inset-0 z-0">
        <Image
          src="/cityscape-background.png"
          alt="Cityscape background"
          fill
          className="object-cover"
          priority
        />
      </div>
      <div className="relative z-10 flex min-h-screen flex-col items-center justify-center px-4">
        <div className="w-full max-w-2xl rounded-lg bg-white/90 p-8 shadow-lg">
          <h1 className="mb-16 text-center text-4xl font-bold text-[#434343] md:text-5xl">
            Resultado da Análise de IA
          </h1>
          {loading ? (
            <div className="text-center text-lg text-gray-600">
              Carregando...
            </div>
          ) : error ? (
            <div className="text-center text-lg text-red-600">
              Erro: {error}
            </div>
          ) : result ? (
            <>
              <div className="mb-16 grid grid-cols-1 gap-8 md:grid-cols-3">
                <div className="flex flex-col items-center text-center">
                  <p className="text-7xl font-bold text-[#434343]">
                    {result.type === "Retracao" ? 1 : 0}
                  </p>
                  <p className="mt-2 text-xl text-[#434343]">
                    Fissuras de
                    <br />
                    retração
                  </p>
                </div>
                <div className="flex flex-col items-center text-center">
                  <p className="text-7xl font-bold text-[#434343]">
                    {result.type === "Termica" ? 1 : 0}
                  </p>
                  <p className="mt-2 text-xl text-[#434343]">
                    Fissuras
                    <br />
                    térmicas
                  </p>
                </div>
                <div className="flex flex-col items-center text-center">
                  <p className="text-7xl font-bold text-[#ff0000]">
                    {result.severity ?? "--"}
                  </p>
                  <p className="mt-2 text-xl text-[#ff0000]">Riscos</p>
                </div>
              </div>

              {/* Botões */}
              <div className="flex flex-col items-center gap-4">
                <button className="flex w-full max-w-lg items-center justify-center gap-2 rounded-md bg-[#00c939] px-6 py-4 text-xl font-medium text-white transition-colors hover:bg-[#00b033]">
                  <Download className="h-6 w-6" />
                  Baixar relatório na íntegra
                </button>

                <div className="mt-4 flex w-full max-w-lg flex-col gap-4 sm:flex-row">
                  <button
                    className="flex-1 rounded-md bg-[#2d608d] px-6 py-3 text-xl font-medium text-white transition-colors hover:bg-[#265279]"
                    onClick={() => router.push("/home")}
                  >
                    Nova Pesquisa
                  </button>
                  <button className="flex flex-1 items-center justify-center gap-2 rounded-md bg-[#2d608d] px-6 py-3 text-xl font-medium text-white transition-colors hover:bg-[#265279]">
                    <History className="h-5 w-5" />
                    Histórico
                  </button>
                </div>
              </div>
            </>
          ) : (
            <div className="text-center text-lg text-gray-600">
              Nenhum resultado encontrado.
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
