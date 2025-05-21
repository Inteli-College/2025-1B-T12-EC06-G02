"use client";

import { Button } from "../components/ui/button";
import { useState, useEffect } from "react";
import { supabase } from "../lib/supabase";
import IconeDoc from "../../public/doc-icon.png";
import IconeServ from "../../public/serv-icon.png";
import IconeHist from "../../public/hist-icon.png";

export default function Homepage({}) {
  const [user, setUser] = useState(null);

  useEffect(() => {
    supabase.auth.getUser().then(({ data: { user } }) => {
      setUser(user);
    });
  }, []);

  const nome = user?.user_metadata?.name.split(" ")[0] || "Usuário";

  return (
    <div className="w-3/4 bg-white/70 backdrop-blur-sm p-4 md:p-6 flex justify-center flex-col rounded items-center shadow-lg gap-10">
      <Button className="!h-auto w-1/6 !p-2 text-white !text-xl rounded hover:bg-[#00b033] transition-colors mb-6">
        <img src={IconeDoc.src} className="h-6"></img>Upload Local
      </Button>

      <h1 className="text-[#434343] text-4xl mx-auto md:text-5xl font-medium leading-tight">
        Olá, {nome}!
      </h1>
      <div className="w-full flex justify-center flex-col items-center">
        <Button
          className="!h-auto w-1/3 !p-4 bg-[#00C939] text-white !text-2xl rounded hover:bg-[#00b033] transition-colors"
          color="#00C939"
        >
          <img src={IconeServ.src}></img>Upload via Servidor
        </Button>
        <p className="text-[#7E7E7E] text-lg italic mb-6">
          *O SOD pode cometer erros
        </p>
      </div>
      <Button className="!h-auto w-1/6 !p-2 text-white !text-xl rounded hover:bg-[#00b033] transition-colors">
        <img src={IconeHist.src} className="h-6"></img>Histórico
      </Button>
    </div>
  );
}
