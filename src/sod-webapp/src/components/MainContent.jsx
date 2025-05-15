"use client";
import { Button } from "../components/ui/button";
import { Upload, History, Wifi } from "lucide-react";
import Image from "next/image";

export default function MainContent({ userName }) {
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
                    {/* Connect Button
                    <Button className="w-full p-4 bg-[#2d608d] text-white text-lg font-medium rounded hover:bg-[#245179] transition-colors flex items-center justify-center gap-2">
                        <Wifi size={20} />
                        Conectar com o drone
                    </Button> */}

                    {/* Greeting */}
                    <h1 className="text-[#434343] text-4xl md:text-5xl font-medium mb-8 leading-tight">
                        Olá, {userName}
                    </h1>

                    {/* Upload Images Button */}
                    <Button className="w-full p-4 bg-[#00c939] text-white text-lg font-medium rounded hover:bg-[#00b033] transition-colors flex items-center justify-center gap-2">
                        <Upload size={20} />
                        Upload de Imagens
                    </Button>

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
