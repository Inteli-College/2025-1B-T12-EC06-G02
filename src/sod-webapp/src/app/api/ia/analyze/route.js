// API route for triggering AI analysis on an uploaded image
// POST /api/ia/analyze
import { NextResponse } from "next/server";
import { exec } from "child_process";
import { createClient } from "@supabase/supabase-js";
import fs from "fs/promises";
import path from "path";
import os from "os";

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL;
const supabaseKey = process.env.SUPABASE_SERVICE_ROLE_KEY || process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY;
const supabase = createClient(supabaseUrl, supabaseKey);

export async function POST(req) {
  try {
    const { file_path, image_id, floor, axis } = await req.json();
    if (!file_path) {
      return NextResponse.json({ error: "Missing file_path" }, { status: 400 });
    }

    // 1. Baixar a imagem do Supabase Storage
    const { data, error } = await supabase.storage.from("crack_images").download(file_path);
    if (error || !data) {
      return NextResponse.json({ error: "Erro ao baixar imagem do Supabase", details: error?.message }, { status: 500 });
    }
    // Salvar em arquivo temporário
    const tempDir = os.tmpdir();
    const tempFile = path.join(tempDir, `img_${Date.now()}.jpg`);
    const arrayBuffer = await data.arrayBuffer();
    await fs.writeFile(tempFile, Buffer.from(arrayBuffer));

    // 2. Rodar a IA com o caminho local
    const runAI = () =>
      new Promise((resolve, reject) => {
        exec(`python ../../../../IA_classificacao/main.py --image_path "${tempFile}"`, (error, stdout, stderr) => {
          if (error) return reject(stderr || error.message);
          resolve(stdout);
        });
      });
    let aiResultRaw;
    let aiResult;
    try {
      aiResultRaw = await runAI();
      // Tentar parsear JSON da saída da IA
      try {
        aiResult = JSON.parse(aiResultRaw);
      } catch (e) {
        aiResult = { raw: aiResultRaw };
      }
    } catch (err) {
      await fs.unlink(tempFile).catch(() => {});
      return NextResponse.json({ error: "AI analysis failed", details: err }, { status: 500 });
    }

    // Limpar arquivo temporário
    await fs.unlink(tempFile).catch(() => {});

    // Opcional: salvar resultado no banco
    // ...

    return NextResponse.json({ success: true, aiResult });
  } catch (err) {
    return NextResponse.json({ error: err.message }, { status: 500 });
  }
}
