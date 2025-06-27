"use client";
import "../globals.css";
import { Inter } from "next/font/google";
import React, { useState, useEffect } from "react";
import BackgroundImage from "../(components)/BackgroundImage";
import Navbar from "../(components)/Navbar";
import Card from "../(components)/Card";
import { supabase } from "../../backend/lib/supabase";

const inter = Inter({
  subsets: ["latin"],
  variable: "--font-inter",
  display: "swap",
});

// Função para formatar data
const formatDate = (dateString) => {
  if (!dateString) return "Data não disponível";
  
  try {
    const date = new Date(dateString);
    if (isNaN(date.getTime())) return "Data inválida";
    
    return date.toLocaleDateString("pt-BR", {
      day: "2-digit",
      month: "2-digit",
      year: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    });
  } catch (error) {
    console.error("Erro ao formatar data:", error);
    return "Data inválida";
  }
};

export default function Projects() {
  const [projects, setProjects] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showModal, setShowModal] = useState(false);
  const [showDetailsModal, setShowDetailsModal] = useState(false);
  const [selectedProject, setSelectedProject] = useState(null);
  const [newProjectName, setNewProjectName] = useState('');
  const [newProjectDescription, setNewProjectDescription] = useState('');
  const [newProjectNumber, setNewProjectNumber] = useState('');
  const [newProjectCNPJ, setNewProjectCNPJ] = useState('');
  const [newProjectAvenida, setNewProjectAvenida] = useState('');
  const [newProjectCEP, setNewProjectCEP] = useState('');
  const [creating, setCreating] = useState(false);
  const [currentPage, setCurrentPage] = useState(1);
  const projectsPerPage = 15;

  // Buscar projetos do Supabase
  const fetchProjects = async () => {
    try {
      setLoading(true);
      setError(null);
      
      const { data, error } = await supabase
        .from('projetos')
        .select('*')
        .order('created_at', { ascending: false });

      if (error) {
        console.error("Erro do Supabase:", error);
        throw error;
      }

      if (!data) {
        setProjects([]);
        return;
      }

      const formattedProjects = data.map((project) => ({
        id: project.id,
        name: project.name || 'Sem nome',
        description: project.Descricao || '',
        number: project.number || null,
        cnpj: project.CNPJ || '',
        avenida: project.Avenida || '',
        cep: project.CEP || null,
        created_at: project.created_at,
        updated_at: project.updated_at,
        formattedDate: formatDate(project.created_at),
      }));

      setProjects(formattedProjects);
    } catch (err) {
      console.error("Erro ao buscar projetos:", err);
      setError(`Erro ao carregar os projetos: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  // Criar novo projeto
  const handleCreateProject = async () => {
    if (!newProjectName.trim()) {
      alert("Nome do projeto é obrigatório!");
      return;
    }

    try {
      setCreating(true);
      setError(null);
      
      // Validar campos numéricos
      const numberValue = newProjectNumber.trim() ? parseInt(newProjectNumber.trim()) : null;
      const cepValue = newProjectCEP.trim() ? parseInt(newProjectCEP.trim()) : null;
      
      if (newProjectNumber.trim() && isNaN(numberValue)) {
        throw new Error("Número deve ser um valor numérico válido");
      }
      
      if (newProjectCEP.trim() && isNaN(cepValue)) {
        throw new Error("CEP deve ser um valor numérico válido");
      }

      const projectData = {
        name: newProjectName.trim(),
        Descricao: newProjectDescription.trim() || null,
        number: numberValue,
        CNPJ: newProjectCNPJ.trim() || null,
        Avenida: newProjectAvenida.trim() || null,
        CEP: cepValue
      };

      console.log("Dados a serem inseridos:", projectData);
      
      const { data, error } = await supabase
        .from('projetos')
        .insert([projectData])
        .select()
        .single();

      if (error) {
        console.error("Erro do Supabase ao criar:", error);
        if (error.code === '42501' || error.message.includes('row-level security')) {
          throw new Error('Erro de permissão: Não foi possível criar o projeto. Verifique as políticas RLS no Supabase.');
        }
        throw error;
      }

      if (!data) {
        throw new Error("Nenhum dado retornado após a criação");
      }

      // Atualizar lista local
      const newProject = {
        id: data.id,
        name: data.name || 'Sem nome',
        description: data.Descricao || '',
        number: data.number || null,
        cnpj: data.CNPJ || '',
        avenida: data.Avenida || '',
        cep: data.CEP || null,
        created_at: data.created_at,
        updated_at: data.updated_at,
        formattedDate: formatDate(data.created_at)
      };

      setProjects([newProject, ...projects]);
      
      // Limpar formulário
      setNewProjectName('');
      setNewProjectDescription('');
      setNewProjectNumber('');
      setNewProjectCNPJ('');
      setNewProjectAvenida('');
      setNewProjectCEP('');
      setShowModal(false);
      
    } catch (err) {
      console.error("Erro ao criar projeto:", err);
      setError(`Erro ao criar o projeto: ${err.message}`);
    } finally {
      setCreating(false);
    }
  };

  // Deletar projeto
  const handleDeleteProject = async (id) => {
    if (!window.confirm("Tem certeza que deseja excluir este projeto?")) return;

    try {
      const { error } = await supabase
        .from('projetos')
        .delete()
        .eq('id', id);

      if (error) {
        console.error("Erro do Supabase ao deletar:", error);
        throw error;
      }

      setProjects(projects.filter(project => project.id !== id));
      setShowDetailsModal(false);
    } catch (err) {
      console.error("Erro ao deletar projeto:", err);
      setError(`Erro ao excluir o projeto: ${err.message}`);
    }
  };

  // Abrir modal de detalhes
  const handleViewDetails = (project) => {
    setSelectedProject(project);
    setShowDetailsModal(true);
  };

  // Limpar formulário
  const clearForm = () => {
    setNewProjectName('');
    setNewProjectDescription('');
    setNewProjectNumber('');
    setNewProjectCNPJ('');
    setNewProjectAvenida('');
    setNewProjectCEP('');
  };

  useEffect(() => {
    fetchProjects();
  }, []);

  // Lógica de paginação
  const indexOfLastProject = currentPage * projectsPerPage;
  const indexOfFirstProject = indexOfLastProject - projectsPerPage;
  const currentProjects = projects.slice(indexOfFirstProject, indexOfLastProject);
  const totalPages = Math.ceil(projects.length / projectsPerPage);

  return (
    <div className={inter.className}>
      <BackgroundImage>
        <Navbar />
        <Card>
          <div className="w-full max-w-4xl mx-auto p-4">
            {/* Header */}
            <div className="text-center mb-8">
              <h1 className="text-4xl font-bold text-gray-800 mb-6 bg-gradient-to-r from-gray-800 to-gray-600 bg-clip-text text-transparent">
                Projetos
              </h1>
              
              <button
                onClick={() => setShowModal(true)}
                className="group relative px-6 py-3 bg-[#2d608d] hover:bg-[#244d70] text-white font-semibold rounded-lg shadow-lg hover:shadow-xl transform hover:scale-105 transition-all duration-300"
              >
                <div className="flex items-center space-x-2">
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                  </svg>
                  <span>Criar novo projeto</span>
                </div>
              </button>
            </div>

            {/* Error Display */}
            {error && (
              <div className="mb-6 bg-red-50 border border-red-200 rounded-lg p-4">
                <div className="flex items-center">
                  <svg className="w-5 h-5 text-red-400 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  <p className="text-red-600 text-sm">{error}</p>
                  <button
                    onClick={() => setError(null)}
                    className="ml-auto text-red-400 hover:text-red-600"
                  >
                    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                    </svg>
                  </button>
                </div>
              </div>
            )}

            {/* Content */}
            <div className="mt-8">
              {loading && (
                <div className="text-center py-12">
                  <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-[#2d608d]"></div>
                  <p className="mt-4 text-gray-600">Carregando projetos...</p>
                </div>
              )}

              {!loading && projects.length === 0 && (
                <div className="text-center py-12">
                  <div className="bg-gray-50 rounded-lg p-8 max-w-md mx-auto">
                    <svg className="w-16 h-16 text-gray-400 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1} d="M9 13h6m-3-3v6m5 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                    </svg>
                    <p className="text-gray-600 text-lg">Nenhum projeto encontrado.</p>
                    <p className="text-gray-500 mt-2">Clique em "Criar novo projeto" para começar.</p>
                  </div>
                </div>
              )}

              {!loading && projects.length > 0 && (
                <>
                  {/* Projects List */}
                  <div className="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden mb-8">
                    
                    <div className="divide-y divide-gray-200">
                      {currentProjects.map((project) => (
                        <div
                          key={project.id}
                          onClick={() => handleViewDetails(project)}
                          className="px-6 py-4 hover:bg-gray-50 cursor-pointer transition-colors duration-200 group"
                        >
                          <div className="flex items-center justify-between">
                            <div className="flex-1">
                              <h3 className="text-lg font-medium text-gray-900 group-hover:text-[#2d608d] transition-colors duration-200">
                                {project.name}
                              </h3>
                              <p className="text-sm text-gray-500 mt-1">
                                Criado em: {project.formattedDate}
                              </p>
                            </div>
                            <div className="flex items-center space-x-2">
                              <div className="w-2 h-2 bg-green-400 rounded-full"></div>
                              <svg className="w-5 h-5 text-gray-400 group-hover:text-[#2d608d] transition-colors duration-200" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                              </svg>
                            </div>
                          </div>
                        </div>
                      ))}
                    </div>
          </div>

                  {/* Pagination */}
                  {totalPages > 1 && (
                    <div className="flex justify-center items-center space-x-4 mt-8">
                      <button
                        onClick={() => setCurrentPage((prev) => Math.max(prev - 1, 1))}
                        disabled={currentPage === 1}
                        className={`px-4 py-2 rounded-lg bg-[#2d608d] text-white transition-all duration-200 ${
                          currentPage === 1
                            ? "opacity-50 cursor-not-allowed"
                            : "hover:bg-[#244d70] hover:shadow-md"
                        }`}
                      >
                        Anterior
                      </button>

                      <span className="text-gray-700 px-4">
                        Página {currentPage} de {totalPages}
                      </span>

                      <button
                        onClick={() =>
                          setCurrentPage((prev) =>
                            prev < totalPages ? prev + 1 : prev
                          )
                        }
                        disabled={currentPage >= totalPages}
                        className={`px-4 py-2 rounded-lg bg-[#2d608d] text-white transition-all duration-200 ${
                          currentPage >= totalPages
                            ? "opacity-50 cursor-not-allowed"
                            : "hover:bg-[#244d70] hover:shadow-md"
                        }`}
                      >
                        Próxima
                      </button>
                    </div>
                  )}
                </>
              )}
            </div>
          </div>
        </Card>
      </BackgroundImage>

      {/* Modal de Criação */}
      {showModal && (
        <div className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-xl shadow-2xl w-full max-w-md transform scale-95 animate-in duration-200">
            <div className="p-6 border-b border-gray-100">
              <div className="flex justify-between items-center">
                <h2 className="text-xl font-semibold text-gray-800">Criar Novo Projeto</h2>
                <button
                  onClick={() => {
                    setShowModal(false);
                    clearForm();
                  }}
                  className="p-2 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded-lg transition-all duration-200"
                >
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </div>
            </div>
            
            <div className="p-6 space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Nome do Projeto *
                </label>
                <input
                  type="text"
                  value={newProjectName}
                  onChange={(e) => setNewProjectName(e.target.value)}
                  placeholder="Digite o nome do projeto..."
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#2d608d] focus:border-transparent transition-all duration-200 placeholder-gray-400"
                  autoFocus
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Descrição
                </label>
                <textarea
                  value={newProjectDescription}
                  onChange={(e) => setNewProjectDescription(e.target.value)}
                  placeholder="Descreva o projeto..."
                  rows={3}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#2d608d] focus:border-transparent transition-all duration-200 placeholder-gray-400 resize-none"
                />
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Número
                  </label>
                  <input
                    type="number"
                    value={newProjectNumber}
                    onChange={(e) => setNewProjectNumber(e.target.value)}
                    placeholder="Ex: 123"
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#2d608d] focus:border-transparent transition-all duration-200 placeholder-gray-400"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    CEP
                  </label>
                  <input
                    type="number"
                    value={newProjectCEP}
                    onChange={(e) => setNewProjectCEP(e.target.value)}
                    placeholder="Ex: 12345678"
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#2d608d] focus:border-transparent transition-all duration-200 placeholder-gray-400"
                  />
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  CNPJ
                </label>
                <input
                  type="text"
                  value={newProjectCNPJ}
                  onChange={(e) => setNewProjectCNPJ(e.target.value)}
                  placeholder="Ex: 12.345.678/0001-90"
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#2d608d] focus:border-transparent transition-all duration-200 placeholder-gray-400"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Avenida/Endereço
                </label>
                <input
                  type="text"
                  value={newProjectAvenida}
                  onChange={(e) => setNewProjectAvenida(e.target.value)}
                  placeholder="Ex: Av. Paulista, 1000"
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#2d608d] focus:border-transparent transition-all duration-200 placeholder-gray-400"
                />
              </div>
            </div>
            
            <div className="p-6 pt-0 flex space-x-3">
              <button
                onClick={() => {
                  setShowModal(false);
                  clearForm();
                }}
                disabled={creating}
                className="flex-1 px-4 py-3 text-gray-600 border border-gray-300 rounded-lg hover:bg-gray-50 transition-all duration-200 disabled:opacity-50"
              >
                Cancelar
              </button>
              <button
                onClick={handleCreateProject}
                disabled={!newProjectName.trim() || creating}
                className="flex-1 px-4 py-3 bg-[#2d608d] hover:bg-[#244d70] text-white rounded-lg hover:shadow-lg transform hover:scale-105 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none flex items-center justify-center space-x-2"
              >
                {creating ? (
                  <>
                    <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                    <span>Criando...</span>
                  </>
                ) : (
                  <>
                    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                    </svg>
                    <span>Criar</span>
                  </>
                )}
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Modal de Detalhes */}
      {showDetailsModal && selectedProject && (
        <div className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-xl shadow-2xl w-full max-w-lg transform scale-95 animate-in duration-200">
            <div className="p-6 border-b border-gray-100">
              <div className="flex justify-between items-center">
                <h2 className="text-xl font-semibold text-gray-800">Detalhes do Projeto</h2>
                <button
                  onClick={() => setShowDetailsModal(false)}
                  className="p-2 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded-lg transition-all duration-200"
                >
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </div>
            </div>
            
            <div className="p-6 space-y-4">
              <div className="flex items-center space-x-3 mb-4">
                <div className="w-12 h-12 bg-gradient-to-br from-[#2d608d] to-[#1e3f5c] rounded-lg flex items-center justify-center">
                  <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                  </svg>
                </div>
                <div>
                  <h3 className="text-lg font-semibold text-gray-900">{selectedProject.name}</h3>
                  <p className="text-sm text-gray-500">ID: {selectedProject.id}</p>
                </div>
              </div>

              <div className="grid grid-cols-1 gap-4">
                {selectedProject.description && (
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Descrição</label>
                    <p className="text-gray-900 bg-gray-50 rounded-lg p-3">{selectedProject.description}</p>
                  </div>
                )}

                <div className="grid grid-cols-2 gap-4">
                  {selectedProject.number && (
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">Número</label>
                      <p className="text-gray-900 bg-gray-50 rounded-lg p-3">{selectedProject.number}</p>
                    </div>
                  )}

                  {selectedProject.cep && (
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">CEP</label>
                      <p className="text-gray-900 bg-gray-50 rounded-lg p-3">{selectedProject.cep}</p>
                    </div>
                  )}
                </div>

                {selectedProject.cnpj && (
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">CNPJ</label>
                    <p className="text-gray-900 bg-gray-50 rounded-lg p-3">{selectedProject.cnpj}</p>
                  </div>
                )}

              </div>
            </div>
            
            <div className="p-6 pt-0 flex space-x-3">
              <button
                onClick={() => setShowDetailsModal(false)}
                className="flex-1 px-4 py-3 text-gray-600 border border-gray-300 rounded-lg hover:bg-gray-50 transition-all duration-200"
              >
                Fechar
              </button>
              <button
                onClick={() => handleDeleteProject(selectedProject.id)}
                className="px-4 py-3 bg-red-600 hover:bg-red-700 text-white rounded-lg hover:shadow-lg transition-all duration-200 flex items-center space-x-2"
              >
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                </svg>
                <span>Excluir</span>
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}