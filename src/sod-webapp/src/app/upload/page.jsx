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
import { useDadosStore } from "../(stores)/useDados";
import Uploads from "../(components)/Uploads"


export default function Upload() {
    const {name, selection, images} = useDadosStore((state) => state.dados);
    console.log(name, selection, images)

    return (
        <div className={inter.className}>
            <BackgroundImage>
                <Navbar/>
                <Uploads name={name} images={images}/>
            </BackgroundImage>
        </div>
    );
}
