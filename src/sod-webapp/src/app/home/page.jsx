// src/app/images/upload/page.js
"use client";
import "../globals.css"
import { Inter } from "next/font/google"

const inter = Inter({ 
  subsets: ["latin"],
  variable: '--font-inter',
  display: 'swap'
})

import React from 'react';
import BackgroundImage from "../(components)/BackgroundImage";
import Navbar from "../(components)/Navbar";
import Homepage from "../(components)/Homepage"

export default function Home() {
    return (
        <div className={inter.className}>
            <BackgroundImage>
                <Navbar/>
                <Homepage/>
            </BackgroundImage>
        </div>
    );
}
