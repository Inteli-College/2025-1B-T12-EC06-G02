"use client";
import "../globals.css";
import { Inter } from "next/font/google";

const inter = Inter({
  subsets: ["latin"],
  variable: "--font-inter",
  display: "swap",
});

import BackgroundImage from "../(components)/BackgroundImage";
import Navbar from "../(components)/Navbar";
import Card from "../(components)/Card";
import Layout from "../(components)/Layout";

export default function Preview({}) {
  return (
    <div className={inter.className}>
      <Layout>
        <Card>
          <embed
            src="/exemplo.pdf"
            type="application/pdf"
            width="100%"
            height="600px"
          />
        </Card>
      </Layout>
    </div>
  );
}
