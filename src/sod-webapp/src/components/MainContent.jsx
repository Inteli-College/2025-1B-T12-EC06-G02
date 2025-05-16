"use client";
import { Button } from "../components/ui/button";
import { Upload, History, Wifi } from "lucide-react";
import Image from "next/image";
import React, { useRef, useState } from "react";
import { supabase } from "../lib/supabase";

export default function MainContent({ userName }) {
    const [selectedImage, setSelectedImage] = useState(null);
    const [previewUrl, setPreviewUrl] = useState(null);
    const [uploading, setUploading] = useState(false);
    const [uploadError, setUploadError] = useState(null);
    const [uploadSuccess, setUploadSuccess] = useState(false);
    const [filePath, setFilePath] = useState(null);
    const [axis, setAxis] = useState("");
    const [floor, setFloor] = useState("");
    const fileInputRef = useRef(null);

    const handleUploadClick = () => {
        if (fileInputRef.current) {
            fileInputRef.current.click();
        }
    };

    const handleFileChange = async (e) => {
        const file = e.target.files[0];
        if (file) {
            setSelectedImage(file);
            setPreviewUrl(URL.createObjectURL(file));
            setUploadError(null);
            setUploadSuccess(false);
            setUploading(true);
            try {
                const fileName = `${Date.now()}_${file.name}`;
                const path = `uploads/${fileName}`;
                const { error: storageError } = await supabase.storage
                    .from('crack_images')
                    .upload(path, file);
                if (storageError) throw storageError;
                setFilePath(path);
            } catch (err) {
                setUploadError('Erro ao enviar imagem: ' + err.message);
                setFilePath(null);
            } finally {
                setUploading(false);
            }
        }
    };

    async function handleAnalyzeImage() {
        if (!selectedImage || !filePath || !axis || !floor) return;
        setUploading(true);
        setUploadError(null);
        setUploadSuccess(false);
        try {
            const { error: insertError } = await supabase
                .from('images')
                .insert([
                    {
                        user_id: null, // ou o id do usuário logado
                        project_id: null, // pode ser mockado
                        file_path: filePath,
                        file_name: selectedImage.name,
                        type: selectedImage.type,
                        size_kb: Math.round(selectedImage.size / 1024),
                        uploaded_at: new Date().toISOString(),
                        metadata: {},
                        axis,
                        floor
                    }
                ]);
            if (insertError) throw insertError;
            setUploadSuccess(true);
        } catch (err) {
            setUploadError('Erro ao salvar no banco: ' + err.message);
        } finally {
            setUploading(false);
        }
    }

    return (
        <main className="relative min-h-screen w-full">
            {/* Background Image with Filter */}
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
            <div className="absolute min-h-screen w-full flex items-center justify-center p-4">
                {/* Semi-transparent Card */}
                <div className="w-full max-w-md bg-white/80 backdrop-blur-sm p-8 md:p-12 rounded shadow-lg space-y-6">
                    {/* Greeting */}
                    <h1 className="text-[#434343] text-4xl md:text-5xl font-medium mb-8 leading-tight">
                        Olá, {userName}!
                    </h1>

                    {/* Upload Images Button */}
                    <input
                        type="file"
                        accept="image/*"
                        ref={fileInputRef}
                        style={{ display: "none" }}
                        onChange={handleFileChange}
                    />
                    <Button
                        className="w-full p-6 bg-[#00C939] text-white text-xl font-semibold rounded-lg hover:bg-[#00b033] transition-colors flex items-center justify-center gap-3"
                        style={{ fontSize: "1.25rem", paddingTop: "2rem", paddingBottom: "2rem", paddingLeft: "2rem", paddingRight: "2rem" }}
                        onClick={handleUploadClick}
                    >
                        <Upload size={28} />
                        Upload de Imagens
                    </Button>

                    {/* Preview da Imagem */}
                    {previewUrl && (
                        <div className="flex flex-col items-center space-y-4 w-full">
                            <img
                                src={previewUrl}
                                alt="Preview"
                                className="w-full max-h-64 object-contain rounded border border-gray-300 shadow"
                            />
                            <div className="w-full flex flex-col md:flex-row gap-4">
                                <div className="w-full">
                                    <label className="block text-gray-700 text-sm mb-1">Piso</label>
                                    <input
                                        type="text"
                                        className="w-full p-2 border border-gray-300 rounded focus:outline-none focus:ring-1 focus:ring-[#2d608d]"
                                        placeholder="Ex: 1, Térreo, 2, Cobertura..."
                                        value={floor}
                                        onChange={e => setFloor(e.target.value)}
                                    />
                                </div>
                                <div className="w-full">
                                    <label className="block text-gray-700 text-sm mb-1">Direção</label>
                                    <select
                                        className="w-full p-2 border border-gray-300 rounded focus:outline-none focus:ring-1 focus:ring-[#2d608d]"
                                        value={axis}
                                        onChange={e => setAxis(e.target.value)}
                                    >
                                        <option value="">Selecione</option>
                                        <option value="Norte">Norte</option>
                                        <option value="Sul">Sul</option>
                                        <option value="Leste">Leste</option>
                                        <option value="Oeste">Oeste</option>
                                    </select>
                                </div>
                            </div>
                            <Button className="w-full p-4 bg-[#2d608d] text-white text-lg font-medium rounded hover:bg-[#245179] transition-colors" onClick={handleAnalyzeImage} disabled={uploading || !axis || !floor}>
                                {uploading ? "Enviando..." : "Analisar imagem com IA"}
                            </Button>
                            {uploadError && <p className="text-red-600 text-sm">{uploadError}</p>}
                            {uploadSuccess && <p className="text-green-600 text-sm">Imagem enviada com sucesso!</p>}
                        </div>
                    )}

                    {/* Warning */}
                    <p className="text-sm italic text-gray-600 text-center">
                        * O SOD pode cometer erros
                    </p>

                    {/* History Button */}
                    <Button className="w-full p-4 bg-[#2d608d] text-white text-lg font-medium rounded hover:bg-[#245179] transition-colors flex items-center justify-center gap-2">
                        <History size={20} />
                        Histórico
                    </Button>
                </div>
            </div>
        </main>
    );
}
