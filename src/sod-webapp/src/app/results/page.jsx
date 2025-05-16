"use client";

import Image from "next/image";
import { useEffect, useState } from "react";
import { supabase } from "../../lib/supabase";

export default function Dashboard() {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function fetchResult() {
      setLoading(true);
      setError(null);
      // Busca o resultado mais recente
      const { data, error } = await supabase
        .from("results")
        .select("*")
        .order("created_at", { ascending: false })
        .limit(1);
      if (error) setError(error.message);
      setResult(data && data[0] ? data[0] : null);
      setLoading(false);
    }
    fetchResult();
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <span className="text-xl">Carregando resultado da IA...</span>
      </div>
    );
  }
  if (error) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <span className="text-xl text-red-600">Erro ao carregar resultado: {error}</span>
      </div>
    );
  }

  return (
    <div className="relative min-h-screen w-full overflow-hidden">
      {/* Background Image */}
      <div className="absolute inset-0 z-0">
        <Image src="/cityscape-background.png" alt="Cityscape background" fill className="object-cover" priority />
      </div>
      <div className="relative z-10 flex min-h-screen flex-col items-center justify-center px-4">
        <div className="w-full max-w-2xl rounded-lg bg-white/90 p-8 shadow-lg">
          <h1 className="mb-16 text-center text-4xl font-bold text-[#434343] md:text-5xl">
            Resultado da Análise de IA
          </h1>
          {result ? (
            <div className="mb-16 grid grid-cols-1 gap-8 md:grid-cols-3">
              <div className="flex flex-col items-center text-center">
                <p className="text-7xl font-bold text-[#434343]">{result.type === 'Retração' ? 1 : 0}</p>
                <p className="mt-2 text-xl text-[#434343]">Fissuras de<br />retração</p>
              </div>
              <div className="flex flex-col items-center text-center">
                <p className="text-7xl font-bold text-[#434343]">{result.type === 'Térmica' ? 1 : 0}</p>
                <p className="mt-2 text-xl text-[#434343]">Fissuras<br />térmicas</p>
              </div>
              <div className="flex flex-col items-center text-center">
                <p className="text-7xl font-bold text-[#ff0000]">{result.severity ?? '--'}</p>
                <p className="mt-2 text-xl text-[#ff0000]">Riscos</p>
              </div>
            </div>
          ) : (
            <div className="text-center text-lg text-gray-600">Nenhum resultado encontrado.</div>
          )}
        </div>
      </div>
    </div>
  );
}
