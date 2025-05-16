import Image from "next/image";
import Link from "next/link";
import { Download, History } from "lucide-react";

export default function Dashboard() {
  return (
    <div className="relative min-h-screen w-full overflow-hidden">
      {/* Background Image */}
      <div className="absolute inset-0 z-0">
        <Image src="/cityscape-background.jpg" alt="Cityscape background" fill className="object-cover" priority />
      </div>

      {/* Logout Button */}
      <div className="absolute right-8 top-12 z-10">
        <Link href="/logout" className="flex items-center text-[#2d608d] hover:underline">
          <span className="mr-2 text-lg">Logout</span>
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="24"
            height="24"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
            strokeLinecap="round"
            strokeLinejoin="round"
          >
            <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4" />
            <polyline points="16 17 21 12 16 7" />
            <line x1="21" y1="12" x2="9" y2="12" />
          </svg>
        </Link>
      </div>

      {/* Main Content */}
      <div className="relative z-10 flex min-h-screen flex-col items-center justify-center px-4">
        <div className="w-full max-w-5xl rounded-lg bg-white/90 p-8 shadow-lg">
          <h1 className="mb-16 text-center text-4xl font-bold text-[#434343] md:text-5xl">
            Principais Insights da sua imagem
          </h1>

          {/* Stats Section */}
          <div className="mb-16 grid grid-cols-1 gap-8 md:grid-cols-3">
            {/* Stat 1 */}
            <div className="flex flex-col items-center text-center">
              <p className="text-7xl font-bold text-[#434343]">03</p>
              <p className="mt-2 text-xl text-[#434343]">
                Fissuras de
                <br />
                retração
              </p>
            </div>

            {/* Stat 2 */}
            <div className="flex flex-col items-center text-center">
              <p className="text-7xl font-bold text-[#434343]">13</p>
              <p className="mt-2 text-xl text-[#434343]">
                Fissuras
                <br />
                térmicas
              </p>
            </div>

            {/* Stat 3 */}
            <div className="flex flex-col items-center text-center">
              <p className="text-7xl font-bold text-[#ff0000]">12</p>
              <p className="mt-2 text-xl text-[#ff0000]">Riscos</p>
            </div>
          </div>

          {/* Buttons */}
          <div className="flex flex-col items-center gap-4">
            <button className="flex w-full max-w-lg items-center justify-center gap-2 rounded-md bg-[#00c939] px-6 py-4 text-xl font-medium text-white transition-colors hover:bg-[#00b033]">
              <Download className="h-6 w-6" />
              Baixar relatório na íntegra
            </button>

            <div className="mt-4 flex w-full max-w-lg flex-col gap-4 sm:flex-row">
              <button className="flex-1 rounded-md bg-[#2d608d] px-6 py-3 text-xl font-medium text-white transition-colors hover:bg-[#265279]">
                Nova Pesquisa
              </button>
              <button className="flex flex-1 items-center justify-center gap-2 rounded-md bg-[#2d608d] px-6 py-3 text-xl font-medium text-white transition-colors hover:bg-[#265279]">
                <History className="h-5 w-5" />
                Histórico
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
