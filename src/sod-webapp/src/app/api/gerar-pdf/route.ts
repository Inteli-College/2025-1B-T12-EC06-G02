import { NextResponse } from "next/server";
import { gerarPDF } from '../../../backend/reports/geraPdf';

export async function POST(req: Request) {
   try {
    const { nome } = await req.json();
    const result = await gerarPDF(nome);
    return NextResponse.json({ buffer: result.base64 });
  } catch (err) {
    console.error('Erro ao gerar PDF:', err);
    return NextResponse.json({ error: 'Erro ao gerar PDF' }, { status: 500 });
  }
}
