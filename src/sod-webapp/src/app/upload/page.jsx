// src/app/images/upload/page.js
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
import { useDadosStore } from "../(stores)/useDados";
import Card from "../(components)/Card";
import Usuario from "../(components)/Usuario";
import MiniGaleria from "../(components)/miniGaleria"

export default function Upload() {
  const { name, selection, images } = useDadosStore((state) => state.dados);
  console.log(name, selection, images);

  return (
    <div className={inter.className}>
      <BackgroundImage>
        <Navbar />
        <Card>
          <Usuario nome={name} />
          <MiniGaleria images={images} />
        </Card>
      </BackgroundImage>
    </div>
  );
}
