import { NextResponse } from "next/server";
import { gerarPDF } from "../../../backend/reports/geraPdf";

export async function POST(req: Request) {
  try {
    const formData = await req.formData();

    const files: { name: string; file: File }[] = [];
    const metadados: Record<string, string> = {};

    for (const [name, value] of formData.entries()) {
      if (value instanceof File) {
        files.push({ name, file: value });
      } else if (typeof value === "string") {
        metadados[name] = value;
      }
    }

    const readFileWithName = async ({ name, file }: { name: string; file: File }) => {
      const arrayBuffer = await file.arrayBuffer();
      return {
        name,
        filename: file.name,
        buffer: Buffer.from(arrayBuffer),
      };
    };

    const processedFiles = await Promise.all(files.map(readFileWithName));

    const termica = processedFiles.filter(f => f.name.startsWith("termica"));
    const retracao = processedFiles.filter(f => f.name.startsWith("retracao"));

    const pdfBuffer = await gerarPDF(termica, retracao, metadados);

    const base64 = pdfBuffer.base64;

    return NextResponse.json({ buffer: base64 });
  } catch (error) {
    console.error("Erro ao gerar o relatório:", error);
    return NextResponse.json(
      { error: "Erro ao gerar o PDF" },
      { status: 500 }
    );
  }
}
