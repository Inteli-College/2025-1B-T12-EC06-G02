// src/app/(components)/OrganizadorImagens.jsx
"use client";

import React, { useState, useRef } from "react";
import { Button } from "./ui/button";
import { X, Plus } from "lucide-react";

export default function OrganizadorImagens({ images, onSubmit, onClose }) {
  const [grupos, setGrupos] = useState([
    { id: 1, andar: "", direcao: "", imagens: [] }
  ]);
  const [imagensNaoAgrupadas, setImagensNaoAgrupadas] = useState(images);
  const [imagensSelecionadas, setImagensSelecionadas] = useState(new Set());
  const [draggedImages, setDraggedImages] = useState([]);
  const scrollContainerRef = useRef(null);

  const direcoes = ["Norte", "Sul", "Leste", "Oeste", "Nordeste", "Noroeste", "Sudeste", "Sudoeste"];

  // Adicionar novo grupo
  const adicionarGrupo = () => {
    const novoId = Math.max(...grupos.map(g => g.id)) + 1;
    setGrupos([...grupos, { id: novoId, andar: "", direcao: "", imagens: [] }]);
    
    // Scroll para o novo grupo
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
    const novoSet = new Set(imagensSelecionadas);
    
    if (event.ctrlKey || event.metaKey) {
      // Ctrl/Cmd + Click: toggle individual
      if (novoSet.has(imagemId)) {
        novoSet.delete(imagemId);
      } else {
        novoSet.add(imagemId);
      }
    } else if (event.shiftKey && imagensSelecionadas.size > 0) {
      // Shift + Click: selecionar range
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
      // Click normal: selecionar apenas esta
      novoSet.clear();
      novoSet.add(imagemId);
    }
    
    setImagensSelecionadas(novoSet);
  };

  // Drag start
  const handleDragStart = (e, imagens) => {
    const imagensParaArrastar = Array.isArray(imagens) ? imagens : [imagens];
    setDraggedImages(imagensParaArrastar);
    e.dataTransfer.effectAllowed = "move";
  };

  // Drag over
  const handleDragOver = (e) => {
    e.preventDefault();
    e.dataTransfer.dropEffect = "move";
  };

  // Drop em grupo
  const handleDropGrupo = (e, grupoId) => {
    e.preventDefault();
    
    const grupo = grupos.find(g => g.id === grupoId);
    if (!grupo.andar || !grupo.direcao) {
      alert("Por favor, preencha o andar e a direção antes de adicionar imagens.");
      return;
    }

    // Remover imagens da lista não agrupada
    setImagensNaoAgrupadas(imagensNaoAgrupadas.filter(
      img => !draggedImages.some(dragImg => dragImg.id === img.id)
    ));

    // Adicionar ao grupo
    setGrupos(grupos.map(g => 
      g.id === grupoId 
        ? { ...g, imagens: [...g.imagens, ...draggedImages] }
        : g
    ));

    // Limpar seleção
    setImagensSelecionadas(new Set());
    setDraggedImages([]);
  };

  // Drop na área não agrupada
  const handleDropNaoAgrupadas = (e) => {
    e.preventDefault();
    
    // Remover de qualquer grupo
    const novosGrupos = grupos.map(g => ({
      ...g,
      imagens: g.imagens.filter(img => !draggedImages.some(dragImg => dragImg.id === img.id))
    }));
    setGrupos(novosGrupos);

    // Adicionar às não agrupadas
    setImagensNaoAgrupadas([...imagensNaoAgrupadas, ...draggedImages]);
    setDraggedImages([]);
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

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-lg w-full max-w-7xl h-[90vh] flex flex-col">
        {/* Header */}
        <div className="flex justify-between items-center p-4 border-b">
          <h2 className="text-2xl font-bold">Organizar Imagens por Localização</h2>
          <Button
            variant="ghost"
            size="icon"
            onClick={onClose}
            className="hover:bg-gray-100"
          >
            <X className="h-5 w-5" />
          </Button>
        </div>

        {/* Instruções */}
        <div className="px-4 py-2 bg-blue-50 text-sm text-blue-700">
          <p>Para selecionar mais de uma imagem, pressione Ctrl + Click. Use Shift + Click para selecionar um intervalo.</p>
        </div>

        {/* Conteúdo */}
        <div className="flex-1 flex overflow-hidden">
          {/* Coluna de imagens não agrupadas */}
          <div className="w-64 border-r p-4 overflow-y-auto">
            <h3 className="font-semibold mb-3">Fotos submetidas ({imagensNaoAgrupadas.length})</h3>
            <div 
              className="grid grid-cols-2 gap-2 min-h-[200px] border-2 border-dashed border-gray-300 rounded p-2"
              onDragOver={handleDragOver}
              onDrop={handleDropNaoAgrupadas}
            >
              {imagensNaoAgrupadas.map((img) => (
                <div
                  key={img.id}
                  className={`relative cursor-pointer border-2 rounded overflow-hidden ${
                    imagensSelecionadas.has(img.id) ? 'border-blue-500' : 'border-gray-300'
                  }`}
                  onClick={(e) => toggleSelecaoImagem(img.id, e)}
                  draggable
                  onDragStart={(e) => {
                    if (imagensSelecionadas.has(img.id)) {
                      // Arrastar todas as selecionadas
                      const selecionadas = imagensNaoAgrupadas.filter(i => imagensSelecionadas.has(i.id));
                      handleDragStart(e, selecionadas);
                    } else {
                      // Arrastar apenas esta
                      handleDragStart(e, img);
                    }
                  }}
                >
                  <img
                    src={img.previewUrl}
                    alt={`Imagem ${img.id}`}
                    className="w-full h-20 object-cover"
                  />
                  {imagensSelecionadas.has(img.id) && (
                    <div className="absolute top-1 right-1 bg-blue-500 text-white rounded-full w-5 h-5 flex items-center justify-center text-xs">
                      ✓
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>

          {/* Grupos */}
          <div className="flex-1 overflow-x-auto" ref={scrollContainerRef}>
            <div className="flex h-full p-4 gap-4" style={{ minWidth: 'max-content' }}>
              {grupos.map((grupo) => (
                <div
                  key={grupo.id}
                  className="w-80 bg-gray-50 rounded-lg p-4 flex flex-col"
                  onDragOver={handleDragOver}
                  onDrop={(e) => handleDropGrupo(e, grupo.id)}
                >
                  <div className="flex justify-between items-start mb-4">
                    <h3 className="font-semibold">Grupo {grupo.id}</h3>
                    {grupos.length > 1 && (
                      <Button
                        variant="ghost"
                        size="icon"
                        onClick={() => removerGrupo(grupo.id)}
                        className="hover:bg-gray-200"
                      >
                        <X className="h-4 w-4" />
                      </Button>
                    )}
                  </div>

                  <div className="space-y-3 mb-4">
                    <div>
                      <label className="block text-sm font-medium mb-1">ANDAR</label>
                      <input
                        type="number"
                        value={grupo.andar}
                        onChange={(e) => atualizarGrupo(grupo.id, 'andar', e.target.value)}
                        className="w-full px-3 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
                        placeholder="Ex: 3"
                      />
                    </div>

                    <div>
                      <label className="block text-sm font-medium mb-1">DIREÇÃO</label>
                      <select
                        value={grupo.direcao}
                        onChange={(e) => atualizarGrupo(grupo.id, 'direcao', e.target.value)}
                        className="w-full px-3 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
                      >
                        <option value="">Selecione...</option>
                        {direcoes.map(dir => (
                          <option key={dir} value={dir}>{dir}</option>
                        ))}
                      </select>
                    </div>
                  </div>

                  <div className="flex-1 border-2 border-dashed border-gray-300 rounded p-2 overflow-y-auto">
                    <div className="grid grid-cols-3 gap-2">
                      {grupo.imagens.map((img) => (
                        <div
                          key={img.id}
                          className="relative cursor-move"
                          draggable
                          onDragStart={(e) => handleDragStart(e, img)}
                        >
                          <img
                            src={img.previewUrl}
                            alt={`Imagem ${img.id}`}
                            className="w-full h-20 object-cover rounded border border-gray-300"
                          />
                        </div>
                      ))}
                    </div>
                    {grupo.imagens.length === 0 && (
                      <p className="text-gray-400 text-center mt-8">
                        Arraste imagens para cá
                      </p>
                    )}
                  </div>

                  <p className="text-sm text-gray-600 mt-2">
                    {grupo.imagens.length} imagem(ns)
                  </p>
                </div>
              ))}

              {/* Botão adicionar grupo */}
              <div className="w-80 flex items-center justify-center">
                <Button
                  onClick={adicionarGrupo}
                  variant="outline"
                  className="h-full min-h-[400px] border-2 border-dashed hover:bg-gray-50"
                >
                  <Plus className="h-8 w-8" />
                </Button>
              </div>
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="flex justify-between items-center p-4 border-t">
          <p className="text-sm text-gray-600">
            {imagensNaoAgrupadas.length} imagem(ns) não organizadas
          </p>
          <div className="flex gap-2">
            <Button variant="outline" onClick={onClose}>
              Cancelar
            </Button>
            <Button 
              onClick={handleSubmit}
              disabled={imagensNaoAgrupadas.length > 0}
              className="bg-[#00C939] hover:bg-[#00b033]"
            >
              Iniciar processamento
            </Button>
          </div>
        </div>
      </div>
    </div>
  );
}