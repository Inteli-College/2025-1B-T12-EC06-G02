"use client";
import "../globals.css";
import { Inter } from "next/font/google";

const inter = Inter({
  subsets: ["latin"],
  variable: "--font-inter",
  display: "swap",
});

import React from "react";
import BackgroundImage from "../(components)/BackgroundImage";
import Navbar from "../(components)/Navbar";
import Card from "../(components)/Card";

export default function Home() {

  const handleNewSearch = () => {
    // Lógica para nova pesquisa
    console.log("Nova pesquisa iniciada");
  };

  return (
    <div className={inter.className}>
      <BackgroundImage>
        <Navbar />
        <Card>
          <div className="w-full max-w-4xl mx-auto p-8">
            <div className="text-center mb-8">
              <h1 className="text-4xl text-gray-800 mb-6">
                Histórico
              </h1>
              <button
                onClick={handleNewSearch}
                className="bg-[#2d608d] hover:bg-[#244d70] text-white font-semibold py-3 px-8 rounded-lg transition-colors duration-200 shadow-md"
              >
                Nova Pesquisa
              </button>
            </div>
         </div>   
        </Card>
      </BackgroundImage>
    </div>
  );
}