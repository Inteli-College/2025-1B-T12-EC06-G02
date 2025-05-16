import Image from "next/image";
import Link from "next/link";
import { Download, History } from "lucide-react";
import { useEffect, useState } from "react";
import { supabase } from "../../lib/supabase";

export default function Dashboard() {
  const [reports, setReports] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function fetchReports() {
      setLoading(true);
      setError(null);
      const { data, error } = await supabase
        .from("reports")
        .select(`*, reports_images (image_id)`)
        .order("generated_at", { ascending: false });
      if (error) setError(error.message);
      setReports(data || []);
      setLoading(false);
    }
    fetchReports();
  }, []);

  // Get the most recent report for insights
  const latestReport = reports && reports.length > 0 ? reports[0] : null;
  // Example: adjust these field names to match your DB schema
  const retractionCracks = latestReport?.retraction_cracks ?? '--';
  const thermalCracks = latestReport?.thermal_cracks ?? '--';
  const risks = latestReport?.risks ?? '--';

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <span className="text-xl">Carregando relatórios...</span>
      </div>
    );
  }
  if (error) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <span className="text-xl text-red-600">Erro ao carregar relatórios: {error}</span>
      </div>
    );
  }

  return (
    <div className="relative min-h-screen w-full overflow-hidden">
      {/* Background Image */}
      <div className="absolute inset-0 z-0">
        <Image src="/cityscape-background.png" alt="Cityscape background" fill className="object-cover" priority />
      </div>

      {/* Logout Button */}
      <div className="absolute right-8 top-12 z-10">
        <Link href="/logout" className="flex items-center text-[#2d608d] hover:underline">
          <span className="mr-2 text-lg">Logout</span>
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="24"
            height="24"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
            strokeLinecap="round"
            strokeLinejoin="round"
          >
            <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4" />
            <polyline points="16 17 21 12 16 7" />
            <line x1="21" y1="12" x2="9" y2="12" />
          </svg>
        </Link>
      </div>

      {/* Main Content */}
      <div className="relative z-10 flex min-h-screen flex-col items-center justify-center px-4">
        <div className="w-full max-w-5xl rounded-lg bg-white/90 p-8 shadow-lg">
          <h1 className="mb-16 text-center text-4xl font-bold text-[#434343] md:text-5xl">
            Principais Insights da sua imagem
          </h1>

          {/* Stats Section */}
          <div className="mb-16 grid grid-cols-1 gap-8 md:grid-cols-3">
            {/* Stat 1 */}
            <div className="flex flex-col items-center text-center">
              <p className="text-7xl font-bold text-[#434343]">{retractionCracks}</p>
              <p className="mt-2 text-xl text-[#434343]">
                Fissuras de<br />retração
              </p>
            </div>

            {/* Stat 2 */}
            <div className="flex flex-col items-center text-center">
              <p className="text-7xl font-bold text-[#434343]">{thermalCracks}</p>
              <p className="mt-2 text-xl text-[#434343]">
                Fissuras<br />térmicas
              </p>
            </div>

            {/* Stat 3 */}
            <div className="flex flex-col items-center text-center">
              <p className="text-7xl font-bold text-[#ff0000]">{risks}</p>
              <p className="mt-2 text-xl text-[#ff0000]">Riscos</p>
            </div>
          </div>

          {/* Buttons */}
          <div className="flex flex-col items-center gap-4">
            <button className="flex w-full max-w-lg items-center justify-center gap-2 rounded-md bg-[#00c939] px-6 py-4 text-xl font-medium text-white transition-colors hover:bg-[#00b033]">
              <Download className="h-6 w-6" />
              Baixar relatório na íntegra
            </button>

            <div className="mt-4 flex w-full max-w-lg flex-col gap-4 sm:flex-row">
              <button className="flex-1 rounded-md bg-[#2d608d] px-6 py-3 text-xl font-medium text-white transition-colors hover:bg-[#265279]">
                Nova Pesquisa
              </button>
              <button className="flex flex-1 items-center justify-center gap-2 rounded-md bg-[#2d608d] px-6 py-3 text-xl font-medium text-white transition-colors hover:bg-[#265279]">
                <History className="h-5 w-5" />
                Histórico
              </button>
            </div>
          </div>

          {/* Lista de Relatórios */}
          {reports.length === 0 ? (
            <div className="text-center text-lg text-gray-600">Nenhum relatório encontrado.</div>
          ) : (
            <div className="mb-12 space-y-8">
              {reports.map((report) => (
                <div key={report.id} className="border rounded-lg p-6 bg-white/80 shadow flex flex-col md:flex-row md:items-center md:justify-between gap-4">
                  <div>
                    <div className="font-semibold text-lg text-[#434343]">Relatório #{report.id}</div>
                    <div className="text-sm text-gray-600">Gerado em: {new Date(report.generated_at).toLocaleString()}</div>
                    <div className="text-sm text-gray-600">Projeto: {report.project_id}</div>
                    <div className="text-sm text-gray-600">Imagens: {report.reports_images?.length || 0}</div>
                  </div>
                  <div className="flex gap-2 mt-4 md:mt-0">
                    {report.file_path && (
                      <a href={"/api/download-report?path=" + encodeURIComponent(report.file_path)} target="_blank" rel="noopener noreferrer" className="flex items-center gap-2 px-4 py-2 bg-[#00c939] text-white rounded hover:bg-[#00b033]">
                        <Download className="h-5 w-5" /> Baixar PDF
                      </a>
                    )}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
