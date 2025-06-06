"use client";
import "../globals.css";
import { Inter } from "next/font/google";
import React, { useState, useEffect } from "react";
import BackgroundImage from "../(components)/BackgroundImage";
import Navbar from "../(components)/Navbar";
import Card from "../(components)/Card";
import Download from "../../../public/download.png";
import { supabase } from "../../backend/lib/supabase";
import layout from "../(components)/Layout"

const inter = Inter({
  subsets: ["latin"],
  variable: "--font-inter",
  display: "swap",
});

export default function History() {
  const [reports, setReports] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [currentPage, setCurrentPage] = useState(1);
  const reportsPerPage = 10;

  const fetchReports = async () => {
    try {
      setLoading(true);
      const { data, error } = await supabase.storage
        .from("relatorios")
        .list("", {
          limit: 100,
          offset: 0,
          sortBy: { column: "created_at", order: "desc" },
        });

      if (error) throw error;

      const formattedReports = data
        .filter((file) => file.name && !file.name.endsWith("/"))
        .map((file) => ({
          id: file.id,
          name: file.name,
          created_at: file.created_at,
          updated_at: file.updated_at,
          size: file.metadata?.size || 0,
          formattedDate: formatDate(file.created_at || file.updated_at),
        }));

      setReports(formattedReports);
    } catch (err) {
      console.error("Erro ao buscar relatórios:", err);
      setError("Erro ao carregar os relatórios. Tente novamente.");
    } finally {
      setLoading(false);
    }
  };

  const formatDate = (dateString) => {
    if (!dateString) return "Data não disponível";

    const date = new Date(dateString);
    return date.toLocaleString("pt-BR", {
      day: "2-digit",
      month: "2-digit",
      year: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    });
  };

  const downloadReport = async (fileName) => {
    try {
      const { data, error } = await supabase.storage
        .from("relatorios")
        .download(fileName);

      if (error) throw error;

      const url = URL.createObjectURL(data);
      const link = document.createElement("a");
      link.href = url;
      link.download = fileName;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      URL.revokeObjectURL(url);
    } catch (err) {
      console.error("Erro ao fazer download:", err);
      alert("Erro ao fazer download do arquivo. Tente novamente.");
    }
  };

  useEffect(() => {
    fetchReports();
  }, []);

  // Lógica de paginação
  const indexOfLastReport = currentPage * reportsPerPage;
  const indexOfFirstReport = indexOfLastReport - reportsPerPage;
  const currentReports = reports.slice(indexOfFirstReport, indexOfLastReport);
  const totalPages = Math.ceil(reports.length / reportsPerPage);

  return (
    <div className={inter.className}>
      <BackgroundImage>
        <Navbar />
        <Card>
          <div className="w-full max-w-4xl mx-auto p-4">
            <div className="text-center mb-8">
              <h1 className="text-4xl text-gray-800 mb-6">Histórico</h1>
            </div>

            <div className="mt-8">
              {loading && (
                <div className="text-center py-8">
                  <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-[#2d608d]"></div>
                  <p className="mt-2 text-gray-600">Carregando relatórios...</p>
                </div>
              )}

              {error && (
                <div className="text-center py-8">
                  <p className="text-red-600 mb-4">{error}</p>
                  <button
                    onClick={fetchReports}
                    className="bg-[#2d608d] hover:bg-[#244d70] text-white px-4 py-2 rounded-lg"
                  >
                    Tentar Novamente
                  </button>
                </div>
              )}

              {!loading && !error && reports.length === 0 && (
                <div className="text-center py-8">
                  <p className="text-gray-600">Nenhum relatório encontrado.</p>
                </div>
              )}

              {!loading && !error && reports.length > 0 && (
                <>
                  <div className="space-y-3">
                    {currentReports.map((report) => (
                      <div
                        key={report.id || report.name}
                        className="flex items-center justify-between bg-white p-4 rounded-lg shadow-sm border border-gray-200 hover:shadow-md transition-shadow duration-200"
                      >
                        <div className="flex items-center space-x-4">
                          <button
                            onClick={() => downloadReport(report.name)}
                            className="w-10 h-10 bg-green-500 rounded flex items-center justify-center hover:bg-green-600 transition-colors duration-200 cursor-pointer"
                          >
                            <img src={Download.src} className="w-6 h-6" />
                          </button>

                          <div className="flex-1">
                            <h3 className="text-lg font-medium text-gray-800">
                              {report.name
                                .replace(/^relatorio-/, "Relatório ")
                                .replace(/\.[^/.]+$/, "")}
                            </h3>
                            <p className="text-sm text-gray-600">
                              {report.formattedDate}
                            </p>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>

                  <div className="flex justify-center items-center space-x-4 mt-6">
                    <button
                      onClick={() => setCurrentPage((prev) => Math.max(prev - 1, 1))}
                      disabled={currentPage === 1}
                      className={`px-4 py-2 rounded bg-[#2d608d] text-white ${
                        currentPage === 1
                          ? "opacity-50 cursor-not-allowed"
                          : "hover:bg-[#244d70]"
                      }`}
                    >
                      Anterior
                    </button>

                    <span className="text-gray-700">
                      Página {currentPage} de {totalPages}
                    </span>

                    <button
                      onClick={() =>
                        setCurrentPage((prev) =>
                          prev < totalPages ? prev + 1 : prev
                        )
                      }
                      disabled={currentPage >= totalPages}
                      className={`px-4 py-2 rounded bg-[#2d608d] text-white ${
                        currentPage >= totalPages
                          ? "opacity-50 cursor-not-allowed"
                          : "hover:bg-[#244d70]"
                      }`}
                    >
                      Próxima
                    </button>
                  </div>
                </>
              )}
            </div>
          </div>
        </Card>
      </BackgroundImage>
    </div>
  );
}
