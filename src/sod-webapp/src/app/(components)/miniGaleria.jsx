"use client";
import Image from "next/image";
import React, { useRef, useState, useEffect } from "react";
import { createPortal } from "react-dom";

export default function miniGaleria({ images, handleImages }) {
  const [uploadError, setUploadError] = useState(null);
  const [uploadSuccess, setUploadSuccess] = useState(false);
  const [selectedImageForModal, setSelectedImageForModal] = useState(null);
  const [mounted, setMounted] = useState(false); // usado para aguardar montagem do DOM
  const fileInputRef = useRef(null);

  useEffect(() => {
    setMounted(true);
  }, []);

  const handleUploadClick = () => {
    if (fileInputRef.current) {
      fileInputRef.current.click();
    }
  };

  const handleFileChange = async (e) => {
    const files = Array.from(e.target.files);
    if (files.length > 0) {
      const newImages = files.map((file) => ({
        file,
        previewUrl: URL.createObjectURL(file),
        id: Math.random().toString(36).substring(2, 15),
      }));

      handleImages([...images, ...newImages]);
      setUploadError(null);
      setUploadSuccess(false);
    }
  };

  const handleDeleteImage = (imageId) => {
    handleImages((prevImages) => {
      const imageToDelete = prevImages.find((img) => img.id === imageId);
      if (imageToDelete) {
        URL.revokeObjectURL(imageToDelete.previewUrl);
      }
      return prevImages.filter((img) => img.id !== imageId);
    });
  };

  const handleImageClick = (image) => {
    setSelectedImageForModal(image);
  };

  const closeModal = () => {
    setSelectedImageForModal(null);
  };

  return (
    <>
      <div className="w-full max-w-4xl bg-gray-700/80 backdrop-blur-sm p-8 rounded-lg shadow-lg">
        <div className="grid grid-cols-3 md:grid-cols-8 gap-4 mb-6">
          {images.map((image, index) => (
            <div
              key={index}
              className="relative aspect-square border border-gray-300 rounded overflow-hidden bg-white group"
            >
              <img
                src={image.previewUrl}
                alt={`Preview ${index + 1}`}
                className="w-full h-full object-cover cursor-pointer hover:opacity-80 transition-opacity"
                onClick={() => handleImageClick(image)}
              />
              <button
                onClick={(e) => {
                  e.stopPropagation();
                  handleDeleteImage(image.id);
                }}
                className="absolute top-1 right-1 bg-gray-500 hover:bg-gray-600 text-white rounded-full w-6 h-6 flex items-center justify-center text-xs font-bold opacity-0 group-hover:opacity-100 transition-opacity"
                title="Deletar imagem"
              >
                ×
              </button>
            </div>
          ))}

          <div
            className="aspect-square border border-gray-300 rounded flex items-center justify-center bg-gray-600 cursor-pointer hover:bg-gray-500 transition-colors"
            onClick={handleUploadClick}
          >
            <input
              type="file"
              accept="image/*"
              multiple
              ref={fileInputRef}
              style={{ display: "none" }}
              onChange={handleFileChange}
            />
            <span className="text-white text-5xl">+</span>
          </div>
        </div>

        {uploadError && (
          <p className="text-red-400 mt-4 text-center">{uploadError}</p>
        )}
        {uploadSuccess && (
          <p className="text-green-400 mt-4 text-center">
            Imagens processadas com sucesso!
          </p>
        )}
      </div>

      {/* MODAL COM PORTAL */}
      {mounted && selectedImageForModal &&
        createPortal(
          <div
            className="fixed inset-0 bg-black/80 flex items-center justify-center z-50 p-4"
            onClick={closeModal}
          >
            <div
              className="relative w-full h-full max-w-6xl bg-black flex flex-col items-center justify-center"
              onClick={(e) => e.stopPropagation()}
            >
              <button
                onClick={closeModal}
                className="absolute top-4 right-4 bg-black/50 hover:bg-black/70 text-white rounded-full w-10 h-10 flex items-center justify-center text-xl font-bold z-10 transition-colors"
                title="Fechar"
              >
                ×
              </button>

              <img
                src={selectedImageForModal.previewUrl}
                alt="Imagem ampliada"
                className="w-full max-h-[80vh] object-contain"
              />

              <div className="p-4 bg-gray-100 w-full text-center">
                {selectedImageForModal?.file?.name ?
                  <p className="text-sm text-gray-600">
                    Nome: {selectedImageForModal?.file?.name}
                  </p> :
                  <a className="text-sm text-gray-600" href={selectedImageForModal?.previewUrl}>
                    Link: {selectedImageForModal?.previewUrl}
                  </a>
                }
                <p className="text-sm text-gray-600">
                  Tamanho: {(selectedImageForModal?.file?.size / 1024 / 1024).toFixed(2)} MB
                </p>
              </div>
            </div>
          </div>,
          document.getElementById("modal-root")
        )}
    </>
  );
}
