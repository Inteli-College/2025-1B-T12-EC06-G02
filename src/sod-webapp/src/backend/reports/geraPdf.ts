// src/backend/reports/gerar-pdf.ts
import { PDFDocument, StandardFonts, rgb } from 'pdf-lib';

export async function gerarPDF(nome: string): Promise<{ base64: string }> {
  const pdfDoc = await PDFDocument.create();
  const page = pdfDoc.addPage([600, 400]);

  const timesRomanFont = await pdfDoc.embedFont(StandardFonts.TimesRoman);
  const { width, height } = page.getSize();

  page.drawText(`Olá, ${nome}! Este é o seu PDF gerado.`, {
    x: 50,
    y: height - 100,
    size: 20,
    font: timesRomanFont,
    color: rgb(0, 0.53, 0.71),
  });

  const pdfBytes = await pdfDoc.save();

return {
    base64: Buffer.from(pdfBytes).toString('base64'), // converte buffer para base64
  };
}
