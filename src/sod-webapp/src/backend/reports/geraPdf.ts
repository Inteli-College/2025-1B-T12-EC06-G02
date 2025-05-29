import { PDFDocument, StandardFonts, rgb } from 'pdf-lib';

export async function gerarPDF(termica: Buffer[], retracao: Buffer[]): Promise<{ base64: string }> {
  const pdfDoc = await PDFDocument.create();
  let page = pdfDoc.addPage([600, 800]); // altura aumentada
  const timesRomanFont = await pdfDoc.embedFont(StandardFonts.TimesRoman);
  const { width, height } = page.getSize();
  let y = height - 50;

  // Título
  page.drawText('Relatório de Classificação de Fissuras', {
    x: 50,
    y,
    size: 18,
    font: timesRomanFont,
    color: rgb(0, 0, 0),
  });

  y -= 40;

  // Seção: Térmicas
  page.drawText('Fissuras Térmicas:', {
    x: 50,
    y,
    size: 14,
    font: timesRomanFont,
    color: rgb(0.2, 0.2, 0.2),
  });

  y -= 20;

  for (const imgBuffer of termica) {
    let image;
    try {
      image = await pdfDoc.embedPng(imgBuffer);
    } catch {
      image = await pdfDoc.embedJpg(imgBuffer);
    }

    const dims = image.scale(0.5);
    if (y - dims.height < 50) {
      page = pdfDoc.addPage([600, 800]);
      y = height - 50;
    }

    page.drawImage(image, {
      x: 50,
      y: y - dims.height,
      width: dims.width,
      height: dims.height,
    });

    y -= dims.height + 20;
  }

  // Seção: Retração
  if (y < 100) {
    page = pdfDoc.addPage([600, 800]);
    y = height - 50;
  }

  page.drawText('Fissuras de Retração:', {
    x: 50,
    y,
    size: 14,
    font: timesRomanFont,
    color: rgb(0.2, 0.2, 0.2),
  });

  y -= 20;

  for (const imgBuffer of retracao) {
    let image;
    try {
      image = await pdfDoc.embedPng(imgBuffer);
    } catch {
      image = await pdfDoc.embedJpg(imgBuffer);
    }

    const dims = image.scale(0.5);
    if (y - dims.height < 50) {
      page = pdfDoc.addPage([600, 800]);
      y = height - 50;
    }

    page.drawImage(image, {
      x: 50,
      y: y - dims.height,
      width: dims.width,
      height: dims.height,
    });

    y -= dims.height + 20;
  }

  const pdfBytes = await pdfDoc.save();

  return {
    base64: Buffer.from(pdfBytes).toString('base64'),
  };
}
