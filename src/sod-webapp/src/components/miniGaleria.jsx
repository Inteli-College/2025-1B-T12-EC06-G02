import Image from "next/image";
import React, { useRef, useState } from "react";
import { supabase } from "../lib/supabase";

export default function miniGaleria() {
  const [selectedImages, setSelectedImages] = useState([]);
  const [uploadError, setUploadError] = useState(null);
  const [uploadSuccess, setUploadSuccess] = useState(false);
  const fileInputRef = useRef(null);

  const handleUploadClick = () => {
    if (fileInputRef.current) {
      fileInputRef.current.click();
    }
  };

  const handleFileChange = async (e) => {
    const files = Array.from(e.target.files);
    if (files.length > 0) {
      const newImages = files.map(file => ({
        file,
        previewUrl: URL.createObjectURL(file),
        id: Math.random().toString(36).substring(2, 15),
      }));
      
      setSelectedImages([...selectedImages, ...newImages]);
      setUploadError(null);
      setUploadSuccess(false);
    }
  };

  return (
    <main className="relative min-h-screen w-full">
      {/* Background Image */}
    <div className="absolute inset-0 -z-10">
        <div className="relative w-full h-full">
            <Image
                src="/cityscape-background.png"
                alt="Cityscape background"
                fill
                quality={100}
                priority
                className="object-cover brightness-90"
            />
        </div>
    </div>  


      {/* Content Container */}
      <div className="absolute min-h-screen w-full flex flex-col items-center justify-center p-4">

        {/* Main Card */}
        <div className="w-full max-w-4xl bg-gray-700/80 backdrop-blur-sm p-8 rounded-lg shadow-lg">
          {/* Image Preview Grid */}
          <div className="grid grid-cols-8 gap-4 mb-6">
            {selectedImages.map((image, index) => (
              <div key={image.id} className="relative aspect-square border border-gray-300 rounded overflow-hidden bg-white">
                <img
                  src={image.previewUrl}
                  alt={`Preview ${index + 1}`}
                  className="w-full h-full object-cover"
                />
              </div>
            ))}
            
            {/* Add Image Button */}
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

          {uploadError && <p className="text-red-400 mt-4 text-center">{uploadError}</p>}
          {uploadSuccess && <p className="text-green-400 mt-4 text-center">Imagens processadas com sucesso!</p>}
          
        </div>
      </div>
    </main>
  );
}