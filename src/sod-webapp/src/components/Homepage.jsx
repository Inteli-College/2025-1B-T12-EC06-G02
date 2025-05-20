"use client";

import { Button } from "../components/ui/button";
import { useState, useEffect } from "react";
import { supabase } from "../lib/supabase";

export default function Homepage({}) {
  const [user, setUser] = useState(null);

  useEffect(() => {
    supabase.auth.getUser().then(({ data: { user } }) => {
      setUser(user);
    });
  }, []);

  const nome = user?.user_metadata?.name.split(" ")[0] || "Usuário";

  return (
    <>
      <h1 className="text-[#434343] text-4xl mx-auto md:text-5xl font-medium mb-8 leading-tight">
        Olá, {nome}!
      </h1>
      <Button
        className="w-full p-6 bg-[#00C939] text-white text-xl font-semibold rounded-lg hover:bg-[#00b033] transition-colors flex items-center justify-center gap-3"
        style={{
          fontSize: "1.25rem",
          paddingTop: "2rem",
          paddingBottom: "2rem",
          paddingLeft: "2rem",
          paddingRight: "2rem",
        }}
      ></Button>
    </>
  );
}
