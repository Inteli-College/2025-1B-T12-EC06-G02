"use client";

import { Button } from "./ui/button";
import { useRouter } from "next/navigation";
import { supabase } from "../../backend/lib/supabase";
import { useCallback } from "react";
import Icone from "../../../public/buttonLogout.png";

export default function Navbar() {
  const router = useRouter();

  const handleLogout = useCallback(async () => {
    await supabase.auth.signOut();
    router.push("/login");
  }, [router]);

  return (
    <Button
      onClick={handleLogout}
      className="absolute top-4 right-6 text-base font-medium text-[#2d608d] cursor-pointer flex items-center gap-2"
    >
      <img src={Icone.src} alt="Logout" className="w-4 h-4" />
      Logout
    </Button>
  );
}
