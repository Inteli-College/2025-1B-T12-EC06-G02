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
    // Caminho absoluto correto para main.py (ajustado para o local real do arquivo)
    const mainPyPath = 'C:/Users/Inteli/Documents/GitHub/inteli-projetos/2025-1B-T12-EC06-G02/src/IA_classificacao/main.py';
    const pythonPath = 'C:/Users/Inteli/AppData/Local/Programs/Python/Python310/python.exe';
    console.log('=== mainPyPath ===');
    console.log(mainPyPath);
    const runAI = () =>
      new Promise((resolve, reject) => {
        exec(`"${pythonPath}" "${mainPyPath}" --image_path "${tempFile}"`, (error, stdout, stderr) => {
          // Loga stdout e stderr para debug
          console.log('=== PYTHON STDOUT ===');
          console.log(stdout);
          console.log('=== PYTHON STDERR ===');
          console.log(stderr);
          if (error) return reject(stderr || error.message || stdout);
          resolve(stdout);
        });
      });
    let aiResultRaw;
    let aiResult;
    try {
      aiResultRaw = await runAI();
      // Loga o resultado bruto da IA
      console.log('=== AI RAW RESULT ===');
      console.log(aiResultRaw);
      // Extrai a última linha JSON válida do stdout
      let jsonLine = null;
      const lines = aiResultRaw.split(/\r?\n/).reverse();
      for (const line of lines) {
        try {
          const parsed = JSON.parse(line);
          jsonLine = parsed;
          break;
        } catch (e) {}
      }
      if (jsonLine) {
        aiResult = jsonLine;
      } else {
        aiResult = { raw: aiResultRaw };
      }
    } catch (err) {
      await fs.unlink(tempFile).catch(() => {});
      // Loga o erro detalhado
      console.error('=== AI analysis failed ===');
      console.error(err);
      return NextResponse.json({ error: "AI analysis failed", details: String(err) }, { status: 500 });
    }

    // Limpar arquivo temporário
    await fs.unlink(tempFile).catch(() => {});

    // Salvar resultado no banco de dados (tabela reports)
    // Exemplo: campos mínimos para criar um report
    const { data: reportData, error: reportError } = await supabase
      .from('reports')
      .insert([
        {
          user_id: null, // ou o id do usuário logado, se disponível
          project_id: null, // ou o id do projeto, se disponível
          file_path: file_path,
          generated_at: new Date().toISOString(),
          // Adicione outros campos se necessário
        }
      ])
      .select();
    if (reportError) {
      return NextResponse.json({ error: 'Erro ao salvar report', details: reportError.message }, { status: 500 });
    }
    const reportId = reportData && reportData[0] && reportData[0].id;

    // Vincular imagem ao report na tabela reports_images
    if (reportId && image_id) {
      await supabase.from('reports_images').insert([
        { report_id: reportId, image_id }
      ]);
    }

    // Salvar resultado detalhado na tabela results
    let resultId = null;
    console.log('AI RESULT OBJ:', aiResult);
    if (reportId && aiResult && typeof aiResult === 'object') {
      // Corrige para garantir que as chaves estejam corretas e não undefined
      const resultPayload = {
        user_id: null, // ou id do usuário
        trustability: aiResult.trustability ?? null,
        severity: aiResult.severity ?? null,
        type: aiResult.type ?? aiResult.classificacao ?? null,
        created_at: new Date().toISOString(),
      };
      console.log('RESULT PAYLOAD TO INSERT:', resultPayload);
      const { data: resultData, error: resultError } = await supabase.from('results').insert([
        resultPayload
      ]).select();
      if (!resultError && resultData && resultData[0]) {
        resultId = resultData[0].id;
      }
    }
    // Atualiza o report para vincular o result_id
    if (reportId && resultId) {
      await supabase.from('reports').update({ result_id: resultId }).eq('id', reportId);
    }

    return NextResponse.json({ success: true, aiResult, reportId });
  } catch (err) {
    return NextResponse.json({ error: err.message }, { status: 500 });
  }
}
