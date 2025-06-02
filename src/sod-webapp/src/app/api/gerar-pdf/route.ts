import { NextResponse } from "next/server";
import { gerarPDF } from "../../../backend/reports/geraPdf";

export async function POST(req: Request) {
  try {
    const formData = await req.formData();

    const termicaFiles = formData.getAll("termica") as File[];
    const retracaoFiles = formData.getAll("retracao") as File[];

    const readFile = async (file: File) => {
      const arrayBuffer = await file.arrayBuffer();
      return Buffer.from(arrayBuffer);
    };

    const termicaBuffers = await Promise.all(termicaFiles.map(readFile));
    const retracaoBuffers = await Promise.all(retracaoFiles.map(readFile));

    // Gera o PDF
    const pdfBuffer = await gerarPDF(termicaBuffers, retracaoBuffers);

    const base64 = pdfBuffer.base64;

    return NextResponse.json({ buffer: base64 });
  } catch (error) {
    console.error(error);
    return NextResponse.json(
      { error: "Erro ao gerar o PDF" },
      { status: 500 }
    );
  }
}
