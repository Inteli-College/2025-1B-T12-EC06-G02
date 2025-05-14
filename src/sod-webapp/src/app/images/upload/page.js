// src/app/images/upload/page.js
"use client";
import "../../globals.css"
import { Inter } from "next/font/google"

const inter = Inter({ 
  subsets: ["latin"],
  variable: '--font-inter',
  display: 'swap'
})

import React from 'react';
import BackgroundImage from "@/components/BackgroundImage";
import Navbar from "@/components/Navbar";
import MainContent from "@/components/MainContent";

export default function ImageUploadPage() {
  return (
    <BackgroundImage>
      <Navbar />
      <MainContent userName="Usuário!" />
    </BackgroundImage>
  );
}
