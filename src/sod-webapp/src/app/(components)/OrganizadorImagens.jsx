// src/app/(components)/OrganizadorImagens.jsx
"use client";

import React, { useState, useRef, useEffect } from "react";
import { Button } from "./ui/button";
import { X, Plus } from "lucide-react";
import { createPortal } from "react-dom";

export default function OrganizadorImagens({ images = [], onSubmit, onClose }) {
  const [grupos, setGrupos] = useState([
    { id: 1, andar: "", direcao: "", imagens: [] }
  ]);
  const [imagensNaoAgrupadas, setImagensNaoAgrupadas] = useState(images);
  const [imagensSelecionadas, setImagensSelecionadas] = useState(new Set());
  const [draggedImages, setDraggedImages] = useState([]);
  const [draggedFromGrupo, setDraggedFromGrupo] = useState(null);
  const [imagemAmpliada, setImagemAmpliada] = useState(null);
  const [imagemParaDeletar, setImagemParaDeletar] = useState(null);
  const [mounted, setMounted] = useState(false);
  const scrollContainerRef = useRef(null);

  const direcoes = ["Norte", "Sul", "Leste", "Oeste", "Nordeste", "Noroeste", "Sudeste", "Sudoeste"];

  useEffect(() => {
    setMounted(true);
  }, []);

  // Adicionar novo grupo
  const adicionarGrupo = () => {
    const novoId = Math.max(...grupos.map(g => g.id)) + 1;
    setGrupos([...grupos, { id: novoId, andar: "", direcao: "", imagens: [] }]);
    
    setTimeout(() => {
      if (scrollContainerRef.current) {
        scrollContainerRef.current.scrollLeft = scrollContainerRef.current.scrollWidth;
      }
    }, 100);
  };

  // Remover grupo
  const removerGrupo = (grupoId) => {
    const grupo = grupos.find(g => g.id === grupoId);
    if (grupo.imagens.length > 0) {
      setImagensNaoAgrupadas([...imagensNaoAgrupadas, ...grupo.imagens]);
    }
    setGrupos(grupos.filter(g => g.id !== grupoId));
  };

  // Atualizar informações do grupo
  const atualizarGrupo = (grupoId, campo, valor) => {
    setGrupos(grupos.map(g => 
      g.id === grupoId ? { ...g, [campo]: valor } : g
    ));
  };

  // Selecionar/deselecionar imagem
  const toggleSelecaoImagem = (imagemId, event) => {
    event.stopPropagation();
    const novoSet = new Set(imagensSelecionadas);
    
    if (event.ctrlKey || event.metaKey) {
      if (novoSet.has(imagemId)) {
        novoSet.delete(imagemId);
      } else {
        novoSet.add(imagemId);
      }
    } else if (event.shiftKey && imagensSelecionadas.size > 0) {
      const todasImagens = imagensNaoAgrupadas.map(img => img.id);
      const ultimaSelecionada = Array.from(imagensSelecionadas)[imagensSelecionadas.size - 1];
      const indexUltima = todasImagens.indexOf(ultimaSelecionada);
      const indexAtual = todasImagens.indexOf(imagemId);
      
      const inicio = Math.min(indexUltima, indexAtual);
      const fim = Math.max(indexUltima, indexAtual);
      
      for (let i = inicio; i <= fim; i++) {
        novoSet.add(todasImagens[i]);
      }
    } else {
      novoSet.clear();
      novoSet.add(imagemId);
    }
    
    setImagensSelecionadas(novoSet);
  };

  // Double click para ampliar imagem
  const handleDoubleClick = (imagem) => {
    setImagemAmpliada(imagem);
  };

  // Deletar imagem
  const handleDeleteImage = (imagem, grupoId = null) => {
    setImagemParaDeletar({ imagem, grupoId });
  };

  const confirmarDelecao = () => {
    if (!imagemParaDeletar) return;

    const { imagem, grupoId } = imagemParaDeletar;

    if (grupoId) {
      // Remover do grupo
      setGrupos(grupos.map(g => 
        g.id === grupoId 
          ? { ...g, imagens: g.imagens.filter(img => img.id !== imagem.id) }
          : g
      ));
    } else {
      // Remover das não agrupadas
      setImagensNaoAgrupadas(imagensNaoAgrupadas.filter(img => img.id !== imagem.id));
      // Remover da seleção se estiver selecionada
      const novoSet = new Set(imagensSelecionadas);
      novoSet.delete(imagem.id);
      setImagensSelecionadas(novoSet);
    }

    setImagemParaDeletar(null);
  };

  // Drag start
  const handleDragStart = (e, imagens, grupoOrigemId = null) => {
    const imagensParaArrastar = Array.isArray(imagens) ? imagens : [imagens];
    setDraggedImages(imagensParaArrastar);
    setDraggedFromGrupo(grupoOrigemId);
    e.dataTransfer.effectAllowed = "move";
  };

  // Drag over
  const handleDragOver = (e) => {
    e.preventDefault();
    e.dataTransfer.dropEffect = "move";
  };

  // Drop em grupo
  const handleDropGrupo = (e, grupoDestinoId) => {
    e.preventDefault();
    
    const grupo = grupos.find(g => g.id === grupoDestinoId);
    if (!grupo.andar || !grupo.direcao) {
      alert("Por favor, preencha o andar e a direção antes de adicionar imagens.");
      return;
    }

    // Se está arrastando do mesmo grupo, não fazer nada
    if (draggedFromGrupo === grupoDestinoId) {
      setDraggedImages([]);
      setDraggedFromGrupo(null);
      return;
    }

    if (draggedFromGrupo !== null) {
      // Movendo de um grupo para outro
      setGrupos(grupos.map(g => {
        if (g.id === draggedFromGrupo) {
          // Remover do grupo origem
          return {
            ...g,
            imagens: g.imagens.filter(img => !draggedImages.some(dragImg => dragImg.id === img.id))
          };
        } else if (g.id === grupoDestinoId) {
          // Adicionar ao grupo destino
          return {
            ...g,
            imagens: [...g.imagens, ...draggedImages]
          };
        }
        return g;
      }));
    } else {
      // Movendo das não agrupadas para um grupo
      setImagensNaoAgrupadas(imagensNaoAgrupadas.filter(
        img => !draggedImages.some(dragImg => dragImg.id === img.id)
      ));

      setGrupos(grupos.map(g => 
        g.id === grupoDestinoId 
          ? { ...g, imagens: [...g.imagens, ...draggedImages] }
          : g
      ));
    }

    // Limpar seleção e drag
    setImagensSelecionadas(new Set());
    setDraggedImages([]);
    setDraggedFromGrupo(null);
  };

  // Drop na área não agrupada
  const handleDropNaoAgrupadas = (e) => {
    e.preventDefault();
    
    // Evitar duplicação
    const imagensExistentes = new Set(imagensNaoAgrupadas.map(img => img.id));
    const imagensParaAdicionar = draggedImages.filter(img => !imagensExistentes.has(img.id));

    if (draggedFromGrupo !== null) {
      // Remover do grupo origem
      setGrupos(grupos.map(g => 
        g.id === draggedFromGrupo
          ? { ...g, imagens: g.imagens.filter(img => !draggedImages.some(dragImg => dragImg.id === img.id)) }
          : g
      ));

      // Adicionar às não agrupadas apenas as que não existem
      setImagensNaoAgrupadas([...imagensNaoAgrupadas, ...imagensParaAdicionar]);
    }

    setDraggedImages([]);
    setDraggedFromGrupo(null);
  };

  // Validar e submeter
  const handleSubmit = () => {
    const gruposComImagens = grupos.filter(g => g.imagens.length > 0);
    
    if (gruposComImagens.length === 0) {
      alert("Por favor, organize as imagens em pelo menos um grupo.");
      return;
    }

    if (imagensNaoAgrupadas.length > 0) {
      alert("Ainda existem imagens não organizadas. Por favor, organize todas as imagens.");
      return;
    }

    onSubmit(gruposComImagens);
  };

  // Obter nome do arquivo
  const getNomeArquivo = (imagem) => {
    if (imagem.file?.name) return imagem.file.name;
    if (imagem.path) return imagem.path.split('/').pop();
    return `Imagem ${imagem.id}`;
  };

  return (
    <div className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50 p-4">
      <div className="bg-white/90 backdrop-blur-sm rounded-lg w-full max-w-[95vw] h-[92vh] flex flex-col shadow-2xl">
        {/* Header */}
        <div className="flex justify-between items-center px-8 py-6 border-b border-gray-200">
          <h2 className="text-3xl font-bold text-[#434343]">Organizar Imagens por Localização</h2>
          <button
            onClick={onClose}
            className="text-gray-500 hover:text-gray-700 transition-colors"
          >
            <X className="h-6 w-6" />
          </button>
        </div>

        {/* Instruções */}
        <div className="px-8 py-4 bg-blue-50/50 text-sm text-blue-700 italic">
          <p>Para selecionar mais de uma imagem, pressione Ctrl + Click. Use Shift + Click para selecionar um intervalo.</p>
        </div>

        {/* Conteúdo */}
        <div className="flex-1 flex overflow-hidden">
          {/* Coluna de imagens não agrupadas */}
          <div className="w-[350px] border-r border-gray-200 p-8 overflow-y-auto bg-gray-50/50">
            <h3 className="font-semibold text-xl mb-6 text-[#434343]">Fotos submetidas ({imagensNaoAgrupadas.length})</h3>
            <div 
              className="grid grid-cols-2 gap-4 min-h-[400px] border-2 border-dashed border-gray-300 rounded-lg p-6 bg-white/50"
              onDragOver={handleDragOver}
              onDrop={handleDropNaoAgrupadas}
            >
              {imagensNaoAgrupadas && imagensNaoAgrupadas.map((img) => (
                <div
                  key={img.id}
                  className="group relative"
                >
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      handleDeleteImage(img);
                    }}
                    className="absolute -top-2 -right-2 z-10 bg-red-500 hover:bg-red-600 text-white rounded-full w-6 h-6 flex items-center justify-center text-xs font-bold opacity-0 group-hover:opacity-100 transition-opacity shadow-lg"
                    title="Deletar imagem"
                  >
                    ×
                  </button>
                  <div
                    className={`relative cursor-pointer border-2 rounded-lg overflow-hidden transition-all hover:shadow-lg ${
                      imagensSelecionadas.has(img.id) ? 'border-[#00C939] shadow-md' : 'border-gray-300'
                    }`}
                    onClick={(e) => toggleSelecaoImagem(img.id, e)}
                    onDoubleClick={() => handleDoubleClick(img)}
                    draggable
                    onDragStart={(e) => {
                      if (imagensSelecionadas.has(img.id)) {
                        const selecionadas = imagensNaoAgrupadas.filter(i => imagensSelecionadas.has(i.id));
                        handleDragStart(e, selecionadas, null);
                      } else {
                        handleDragStart(e, img, null);
                      }
                    }}
                  >
                    <img
                      src={img.previewUrl}
                      alt={`Imagem ${img.id}`}
                      className="w-full h-28 object-cover"
                    />
                    {imagensSelecionadas.has(img.id) && (
                      <div className="absolute top-2 right-2 bg-[#00C939] text-white rounded-full w-6 h-6 flex items-center justify-center text-xs font-bold">
                        ✓
                      </div>
                    )}
                  </div>
                  <p className="text-xs text-gray-600 mt-1 truncate text-center">
                    {getNomeArquivo(img)}
                  </p>
                </div>
              ))}
            </div>
          </div>

          {/* Grupos */}
          <div className="flex-1 overflow-x-auto bg-gray-100/30" ref={scrollContainerRef}>
            <div className="flex h-full p-8 gap-8" style={{ minWidth: 'max-content' }}>
              {grupos.map((grupo) => (
                <div
                  key={grupo.id}
                  className="w-[450px] bg-white/80 backdrop-blur-sm rounded-lg p-8 flex flex-col shadow-lg border border-gray-200"
                  onDragOver={handleDragOver}
                  onDrop={(e) => handleDropGrupo(e, grupo.id)}
                >
                  <div className="flex justify-between items-start mb-6">
                    <h3 className="font-semibold text-xl text-[#434343]">Grupo {grupo.id}</h3>
                    {grupos.length > 1 && (
                      <button
                        onClick={() => removerGrupo(grupo.id)}
                        className="text-gray-400 hover:text-red-600 transition-colors"
                      >
                        <X className="h-5 w-5" />
                      </button>
                    )}
                  </div>

                  <div className="space-y-5 mb-8">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">ANDAR</label>
                      <input
                        type="number"
                        value={grupo.andar}
                        onChange={(e) => atualizarGrupo(grupo.id, 'andar', e.target.value)}
                        className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-[#00C939] focus:border-transparent"
                        placeholder="Ex: 3"
                      />
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">DIREÇÃO</label>
                      <select
                        value={grupo.direcao}
                        onChange={(e) => atualizarGrupo(grupo.id, 'direcao', e.target.value)}
                        className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-[#00C939] focus:border-transparent"
                      >
                        <option value="">Selecione...</option>
                        {direcoes.map(dir => (
                          <option key={dir} value={dir}>{dir}</option>
                        ))}
                      </select>
                    </div>
                  </div>

                  <div className="flex-1 border-2 border-dashed border-gray-300 rounded-lg p-6 overflow-y-auto bg-gray-50/50 min-h-[350px]">
                    <div className="grid grid-cols-3 gap-4">
                      {grupo.imagens.map((img) => (
                        <div
                          key={img.id}
                          className="group relative"
                        >
                          <button
                            onClick={(e) => {
                              e.stopPropagation();
                              handleDeleteImage(img, grupo.id);
                            }}
                            className="absolute -top-2 -right-2 z-10 bg-red-500 hover:bg-red-600 text-white rounded-full w-5 h-5 flex items-center justify-center text-xs font-bold opacity-0 group-hover:opacity-100 transition-opacity shadow-lg"
                            title="Deletar imagem"
                          >
                            ×
                          </button>
                          <div
                            className="relative cursor-move border border-gray-300 rounded-lg overflow-hidden hover:shadow-md transition-all"
                            draggable
                            onDragStart={(e) => handleDragStart(e, img, grupo.id)}
                            onDoubleClick={() => handleDoubleClick(img)}
                          >
                            <img
                              src={img.previewUrl}
                              alt={`Imagem ${img.id}`}
                              className="w-full h-24 object-cover"
                            />
                          </div>
                          <p className="text-xs text-gray-600 mt-1 truncate text-center">
                            {getNomeArquivo(img)}
                          </p>
                        </div>
                      ))}
                    </div>
                    {grupo.imagens.length === 0 && (
                      <div className="flex items-center justify-center h-full">
                        <p className="text-gray-400 text-center text-lg">
                          Arraste imagens para cá
                        </p>
                      </div>
                    )}
                  </div>

                  <p className="text-sm text-gray-600 mt-4 text-center">
                    {grupo.imagens.length} imagem(ns)
                  </p>
                </div>
              ))}

              {/* Botão adicionar grupo */}
              <div className="w-[450px] flex items-center justify-center">
                <button
                  onClick={adicionarGrupo}
                  className="h-full min-h-[600px] w-full border-2 border-dashed border-gray-400 rounded-lg hover:bg-gray-50 transition-colors flex items-center justify-center group"
                >
                  <Plus className="h-12 w-12 text-gray-400 group-hover:text-gray-600" />
                </button>
              </div>
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="flex justify-between items-center px-8 py-6 border-t border-gray-200 bg-gray-50/50">
          <p className="text-gray-600">
            {imagensNaoAgrupadas.length} imagem(ns) não organizadas
          </p>
          <div className="flex gap-4">
            <Button 
              variant="outline" 
              onClick={onClose}
              className="px-6 py-2 border border-gray-300 text-gray-700 hover:bg-gray-50"
            >
              Cancelar
            </Button>
            <Button 
              onClick={handleSubmit}
              disabled={imagensNaoAgrupadas.length > 0}
              className="px-6 py-2 bg-[#00C939] hover:bg-[#00b033] text-white disabled:bg-gray-300 disabled:cursor-not-allowed"
            >
              Iniciar processamento
            </Button>
          </div>
        </div>
      </div>

      {/* Modal de imagem ampliada */}
      {mounted && imagemAmpliada &&
        createPortal(
          <div
            className="fixed inset-0 bg-black/80 flex items-center justify-center z-[60] p-4"
            onClick={() => setImagemAmpliada(null)}
          >
            <div
              className="relative w-full h-full max-w-6xl bg-black flex flex-col items-center justify-center"
              onClick={(e) => e.stopPropagation()}
            >
              <button
                onClick={() => setImagemAmpliada(null)}
                className="absolute top-4 right-4 bg-black/50 hover:bg-black/70 text-white rounded-full w-10 h-10 flex items-center justify-center text-xl font-bold z-10 transition-colors"
                title="Fechar"
              >
                ×
              </button>

              <img
                src={imagemAmpliada.previewUrl}
                alt="Imagem ampliada"
                className="w-full max-h-[80vh] object-contain"
              />

              <div className="p-4 bg-gray-900 w-full text-center">
                <p className="text-sm text-gray-300">
                  {getNomeArquivo(imagemAmpliada)}
                </p>
                {imagemAmpliada.file?.size && (
                  <p className="text-sm text-gray-400">
                    Tamanho: {(imagemAmpliada.file.size / 1024 / 1024).toFixed(2)} MB
                  </p>
                )}
              </div>
            </div>
          </div>,
          document.getElementById("modal-root") || document.body
        )}

      {/* Modal de confirmação de deleção */}
      {mounted && imagemParaDeletar &&
        createPortal(
          <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-[70] p-4">
            <div className="bg-white rounded-lg p-6 max-w-md w-full shadow-xl">
              <h3 className="text-lg font-semibold mb-4">Confirmar Exclusão</h3>
              <p className="text-gray-600 mb-6">
                Tem certeza que deseja apagar esta análise do relatório?
              </p>
              <div className="flex justify-end gap-3">
                <Button
                  variant="outline"
                  onClick={() => setImagemParaDeletar(null)}
                  className="px-4 py-2"
                >
                  Não
                </Button>
                <Button
                  onClick={confirmarDelecao}
                  className="px-4 py-2 bg-red-500 hover:bg-red-600 text-white"
                >
                  Sim
                </Button>
              </div>
            </div>
          </div>,
          document.getElementById("modal-root") || document.body
        )}
    </div>
  );
}