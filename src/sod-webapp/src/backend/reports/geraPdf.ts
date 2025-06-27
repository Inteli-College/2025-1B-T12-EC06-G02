import { PDFDocument, StandardFonts, rgb } from "pdf-lib";

type ArquivoProcessado = {
  name: string; // Ex: 'termica-Sul-1'
  filename: string; // Ex: 'relatorioTermica.pdf'
  buffer: Buffer;
};

type Agrupado = {
  [direcao: string]: {
    [andar: string]: ArquivoProcessado[];
  };
};

function agruparPorDirecaoEAndar(arquivos: ArquivoProcessado[]): Agrupado {
  const resultado: Agrupado = {};

  for (const arquivo of arquivos) {
    const [_, direcao, andar] = arquivo.name.split("-");

    if (!resultado[direcao]) resultado[direcao] = {};
    if (!resultado[direcao][andar]) resultado[direcao][andar] = [];

    resultado[direcao][andar].push(arquivo);
  }

  return resultado;
}

interface DadosRelatorio {
  numeroRelatorio?: string;
  cliente?: string;
  cnpj?: string;
  endereco?: string;
  naturezaTrabalho?: string;
  referencia?: string;
  material?: string;
  ensaiosRealizados?: string[];
  requisitos?: Array<{
    ensaio: string;
    resultado: string;
    classificacao: string;
  }>;
  equipe?: string[];
  responsavelTecnico?: string;
  crea?: string;
  gerenteTecnico?: string;
  crq?: string;
}

import fs from "fs";
import path from "path";

const loadImage = (imagePath: string): Buffer | null => {
  try {
    return fs.readFileSync(imagePath);
  } catch (error) {
    console.warn(`Could not load image from ${imagePath}`);
    return null;
  }
};

const headerBuffer = loadImage(
  path.join(process.cwd(), "public", "header.png")
);
const disclaimerBuffer = loadImage(
  path.join(process.cwd(), "public", "disclaimer.png")
);
const footerBuffer = loadImage(
  path.join(process.cwd(), "public", "footer.png")
);

export interface ImagensIPT {
  header?: Buffer;
  disclaimer?: Buffer;
  footer?: Buffer;
}

const imagensIPT = {
  header: headerBuffer,
  disclaimer: disclaimerBuffer,
  footer: footerBuffer,
};

export async function gerarPDF(
  termica: ArquivoProcessado[],
  retracao: ArquivoProcessado[],
  dados: DadosRelatorio = {},
  imagensIPT: ImagensIPT = {}
): Promise<{ base64: string }> {
  const pdfDoc = await PDFDocument.create();
  let page = pdfDoc.addPage([595, 842]); // A4 size
  const font = await pdfDoc.embedFont(StandardFonts.Helvetica); // Arial
  const fontBold = await pdfDoc.embedFont(StandardFonts.HelveticaBold); // Arial Bold
  const { width, height } = page.getSize();
  let y = height - 80;

  // Embed das imagens do IPT
  let headerImage, disclaimerImage, footerImage;

  if (imagensIPT.header) {
    try {
      headerImage = await pdfDoc.embedPng(imagensIPT.header);
    } catch {
      headerImage = await pdfDoc.embedJpg(imagensIPT.header);
    }
  }

  if (imagensIPT.disclaimer) {
    try {
      disclaimerImage = await pdfDoc.embedPng(imagensIPT.disclaimer);
    } catch {
      disclaimerImage = await pdfDoc.embedJpg(imagensIPT.disclaimer);
    }
  }

  if (imagensIPT.footer) {
    try {
      footerImage = await pdfDoc.embedPng(imagensIPT.footer);
    } catch {
      footerImage = await pdfDoc.embedJpg(imagensIPT.footer);
    }
  }

  // Função auxiliar para adicionar nova página se necessário
  const checkNewPage = (requiredSpace: number) => {
    if (y - requiredSpace < 150) {
      page = pdfDoc.addPage([595, 842]);
      y = height - 80;
      addHeader();
      addFooter();
    }
  };

  // Função para adicionar cabeçalho
  const addHeader = () => {
    if (headerImage) {
      const headerDims = headerImage.scale(0.8);
      page.drawImage(headerImage, {
        x: 50,
        y: height - headerDims.height - 20,
        width: headerDims.width,
        height: headerDims.height,
      });
    } else {
      // Fallback para texto se não houver imagem
      page.drawText("IPT", {
        x: 50,
        y: height - 50,
        size: 24,
        font: fontBold,
        color: rgb(0, 0, 0.8),
      });

      page.drawText("INSTITUTO DE PESQUISAS TECNOLÓGICAS", {
        x: 100,
        y: height - 45,
        size: 12,
        font: fontBold,
        color: rgb(0, 0, 0),
      });

      page.drawText("HABITAÇÃO E EDIFICAÇÕES", {
        x: 50,
        y: height - 65,
        size: 10,
        font: font,
        color: rgb(0, 0, 0),
      });
    }
  };

  // Função para adicionar rodapé
  const addFooter = () => {
    if (footerImage) {
      const footerDims = footerImage.scale(0.8);
      page.drawImage(footerImage, {
        x: 50,
        y: 20,
        width: footerDims.width,
        height: footerDims.height,
      });
    } else {
      // Fallback para texto se não houver imagem
      const footerY = 80;

      page.drawText(
        "Os resultados apresentados neste documento se aplicam somente ao item ensaiado ou calibração.",
        {
          x: 50,
          y: footerY,
          size: 8,
          font: font,
          color: rgb(0, 0, 0),
        }
      );

      page.drawText(
        "Este documento não dá direito ao uso do nome ou da marca IPT, para quaisquer fins, sob pena de indenização.",
        {
          x: 50,
          y: footerY - 10,
          size: 8,
          font: font,
          color: rgb(0, 0, 0),
        }
      );

      page.drawText(
        "A reprodução deste documento só poderá ser feita integralmente, sem nenhuma alteração.",
        {
          x: 50,
          y: footerY - 20,
          size: 8,
          font: font,
          color: rgb(0, 0, 0),
        }
      );

      page.drawText("Av. Prof. Almeida Prado, 532 | Butantã", {
        x: 50,
        y: footerY - 40,
        size: 8,
        font: font,
        color: rgb(0, 0, 0),
      });

      page.drawText("São Paulo SP | 05508-901", {
        x: 50,
        y: footerY - 50,
        size: 8,
        font: font,
        color: rgb(0, 0, 0),
      });

      page.drawText("Tel +55 11 3767 4000 | ipt@ipt.br | www.ipt.br", {
        x: 50,
        y: footerY - 60,
        size: 8,
        font: font,
        color: rgb(0, 0, 0),
      });
    }
  };

  // Adicionar cabeçalho e rodapé inicial
  addHeader();
  addFooter();

  // Ajustar y para começar após o header
  y = height - 140;

  // Título do relatório
  const numeroRelatorio = dados.numeroRelatorio || "XXX XXX XX-203";
  page.drawText(`RELATÓRIO DE ENSAIO N° ${numeroRelatorio}`, {
    x: 50,
    y,
    size: 14,
    font: fontBold,
    color: rgb(0, 0, 0),
  });

  y -= 30;

  // Informações do cliente
  if (dados.cliente) {
    page.drawText(`CLIENTE: ${dados.cliente}`, {
      x: 50,
      y,
      size: 10,
      font: font,
      color: rgb(0, 0, 0),
    });
    y -= 15;
  }

  if (dados.cnpj) {
    page.drawText(`CNPJ: ${dados.cnpj}`, {
      x: 50,
      y,
      size: 10,
      font: font,
      color: rgb(0, 0, 0),
    });
    y -= 15;
  }

  if (dados.endereco) {
    page.drawText(`ENDEREÇO: ${dados.endereco}`, {
      x: 50,
      y,
      size: 10,
      font: font,
      color: rgb(0, 0, 0),
    });
    y -= 15;
  }

  y -= 10;

  // Natureza do trabalho
  const natureza =
    dados.naturezaTrabalho || "Ensaios de classificação de fissuras";
  page.drawText(`NATUREZA DO TRABALHO: ${natureza}`, {
    x: 50,
    y,
    size: 10,
    font: font,
    color: rgb(0, 0, 0),
  });

  y -= 15;

  if (dados.referencia) {
    page.drawText(`REFERÊNCIA: ${dados.referencia}`, {
      x: 50,
      y,
      size: 10,
      font: font,
      color: rgb(0, 0, 0),
    });
    y -= 15;
  }

  y -= 20;

  // Seção 1 - MATERIAL
  checkNewPage(40);
  page.drawText("1 MATERIAL", {
    x: 50,
    y,
    size: 12,
    font: fontBold,
    color: rgb(0, 0, 0),
  });

  y -= 20;

  const materialDesc =
    dados.material || "Material analisado conforme especificações técnicas.";
  page.drawText(materialDesc, {
    x: 50,
    y,
    size: 10,
    font: font,
    color: rgb(0, 0, 0),
  });

  y -= 30;

  // Seção 2 - ESCOPO DE ENSAIOS
  checkNewPage(60);
  page.drawText("2 ESCOPO DE ENSAIOS", {
    x: 50,
    y,
    size: 12,
    font: fontBold,
    color: rgb(0, 0, 0),
  });

  y -= 20;

  page.drawText("2.1 Ensaios realizados e métodos empregados", {
    x: 50,
    y,
    size: 10,
    font: fontBold,
    color: rgb(0, 0, 0),
  });

  y -= 15;

  if (dados.ensaiosRealizados && dados.ensaiosRealizados.length > 0) {
    for (const ensaio of dados.ensaiosRealizados) {
      checkNewPage(15);
      page.drawText(`• ${ensaio}`, {
        x: 60,
        y,
        size: 10,
        font: font,
        color: rgb(0, 0, 0),
      });
      y -= 15;
    }
  } else {
    page.drawText("• Análise visual de fissuras térmicas", {
      x: 60,
      y,
      size: 10,
      font: font,
      color: rgb(0, 0, 0),
    });
    y -= 15;
    page.drawText("• Análise visual de fissuras de retração", {
      x: 60,
      y,
      size: 10,
      font: font,
      color: rgb(0, 0, 0),
    });
    y -= 15;
  }

  y -= 20;

  // Seção 3 - RESULTADOS
  checkNewPage(40);
  page.drawText("3 RESULTADOS", {
    x: 50,
    y,
    size: 12,
    font: fontBold,
    color: rgb(0, 0, 0),
  });

  y -= 20;

    let figuraIndex = 1;

  // Fissuras Térmicas
  if (termica.length > 0) {
    page = pdfDoc.addPage([595, 842]);
    y = height - 80;
    addHeader();
    addFooter();
    checkNewPage(40);
    page.drawText("3.1 Fissuras Térmicas", {
      x: 50,
      y,
      size: 11,
      font: fontBold,
      color: rgb(0.2, 0.2, 0.2),
    });
    y -= 20;

    const termicaAgrupada = agruparPorDirecaoEAndar(termica);

    for (const direcao of Object.keys(termicaAgrupada).sort()) {
      checkNewPage(30);
      page.drawText(`Direção: ${direcao}`, {
        x: 60,
        y,
        size: 10,
        font: fontBold,
        color: rgb(0.1, 0.1, 0.1),
      });
      y -= 20;

      const andares = termicaAgrupada[direcao];
      for (const andar of Object.keys(andares).sort(
        (a, b) => Number(a) - Number(b)
      )) {
        checkNewPage(30);
        page.drawText(`Andar: ${andar}`, {
          x: 70,
          y,
          size: 9,
          font: fontBold,
          color: rgb(0.2, 0.2, 0.2),
        });
        y -= 15;

        for (const arquivo of andares[andar]) {
          let image;
          try {
            image = await pdfDoc.embedPng(arquivo.buffer);
          } catch {
            image = await pdfDoc.embedJpg(arquivo.buffer);
          }

          const dims = image.scale(0.4);
          checkNewPage(dims.height + 40);

          page.drawText(`Figura ${figuraIndex} - Fissura Térmica Detectada ${figuraIndex}`, {
            x: 80,
            y,
            size: 9,
            font,
            color: rgb(0, 0, 0),
          });
          figuraIndex++

          y -= 15;

          page.drawImage(image, {
            x: 80,
            y: y - dims.height,
            width: dims.width,
            height: dims.height,
          });

          y -= dims.height + 15;
        }
      }
    }
  }
  

  // Fissuras Retração
if (retracao.length > 0) {
  page = pdfDoc.addPage([595, 842]);
  y = height - 80;
  addHeader();
  addFooter();
  checkNewPage(40);
  page.drawText('3.2 Fissuras Retração', {
    x: 50,
    y,
    size: 11,
    font: fontBold,
    color: rgb(0.2, 0.2, 0.2),
  });
  y -= 20;

  const retracaoAgrupada = agruparPorDirecaoEAndar(retracao);

  for (const direcao of Object.keys(retracaoAgrupada).sort()) {
    checkNewPage(30);
    page.drawText(`Direção: ${direcao}`, {
      x: 60,
      y,
      size: 10,
      font: fontBold,
      color: rgb(0.1, 0.1, 0.1),
    });
    y -= 20;

    const andares = retracaoAgrupada[direcao];
    for (const andar of Object.keys(andares).sort((a, b) => Number(a) - Number(b))) {
      checkNewPage(30);
      page.drawText(`Andar: ${andar}`, {
        x: 70,
        y,
        size: 9,
        font: fontBold,
        color: rgb(0.2, 0.2, 0.2),
      });
      y -= 15;

      for (const arquivo of andares[andar]) {
        let image;
        try {
          image = await pdfDoc.embedPng(arquivo.buffer);
        } catch {
          image = await pdfDoc.embedJpg(arquivo.buffer);
        }

        const dims = image.scale(0.4);
        checkNewPage(dims.height + 40);

        page.drawText(`Figura ${figuraIndex} - Fissura de Retração Detectada ${figuraIndex}`, {
          x: 80,
          y,
          size: 9,
          font,
          color: rgb(0, 0, 0),
        });
        figuraIndex++

        y -= 15;

        page.drawImage(image, {
          x: 80,
          y: y - dims.height,
          width: dims.width,
          height: dims.height,
        });

        y -= dims.height + 15;
      }
    }
  }
}


  // Seção 4 - REQUISITOS
  checkNewPage(100);
  page.drawText("4 REQUISITOS", {
    x: 50,
    y,
    size: 12,
    font: fontBold,
    color: rgb(0, 0, 0),
  });

  y -= 20;

  // Tabela de classificação (se fornecida)
  if (dados.requisitos && dados.requisitos.length > 0) {
    page.drawText("Tabela 1 - Classificação dos ensaios realizados", {
      x: 50,
      y,
      size: 10,
      font: fontBold,
      color: rgb(0, 0, 0),
    });

    y -= 25;

    // Cabeçalho da tabela
    page.drawText("Ensaio", {
      x: 50,
      y,
      size: 9,
      font: fontBold,
      color: rgb(0, 0, 0),
    });

    page.drawText("Resultado", {
      x: 200,
      y,
      size: 9,
      font: fontBold,
      color: rgb(0, 0, 0),
    });

    page.drawText("Classificação", {
      x: 350,
      y,
      size: 9,
      font: fontBold,
      color: rgb(0, 0, 0),
    });

    y -= 15;

    // Dados da tabela
    for (const requisito of dados.requisitos) {
      checkNewPage(15);
      page.drawText(requisito.ensaio, {
        x: 50,
        y,
        size: 9,
        font: font,
        color: rgb(0, 0, 0),
      });

      page.drawText(requisito.resultado, {
        x: 200,
        y,
        size: 9,
        font: font,
        color: rgb(0, 0, 0),
      });

      page.drawText(requisito.classificacao, {
        x: 350,
        y,
        size: 9,
        font: font,
        color: rgb(0, 0, 0),
      });

      y -= 15;
    }
  }

  // Equipe técnica
  checkNewPage(120);
  y -= 20;
  page.drawText("EQUIPE TÉCNICA", {
    x: 50,
    y,
    size: 12,
    font: fontBold,
    color: rgb(0, 0, 0),
  });

  y -= 20;

  if (dados.equipe && dados.equipe.length > 0) {
    for (const membro of dados.equipe) {
      page.drawText(membro, {
        x: 50,
        y,
        size: 10,
        font: font,
        color: rgb(0, 0, 0),
      });
      y -= 15;
    }
  }

  y -= 20;

  // Data
  const hoje = new Date();
  const dataFormatada = hoje.toLocaleDateString("pt-BR", {
    year: "numeric",
    month: "long",
    day: "numeric",
  });

  page.drawText(`São Paulo, ${dataFormatada}.`, {
    x: 50,
    y,
    size: 10,
    font: font,
    color: rgb(0, 0, 0),
  });

  y -= 30;

  // Assinaturas
  if (dados.responsavelTecnico) {
    page.drawText(dados.responsavelTecnico, {
      x: 50,
      y,
      size: 10,
      font: font,
      color: rgb(0, 0, 0),
    });
    y -= 15;
    page.drawText("Pesquisador", {
      x: 50,
      y,
      size: 9,
      font: font,
      color: rgb(0, 0, 0),
    });
    y -= 15;
    if (dados.crea) {
      page.drawText(`CREA ${dados.crea}`, {
        x: 50,
        y,
        size: 9,
        font: font,
        color: rgb(0, 0, 0),
      });
    }
    y -= 30;
  }

  if (dados.gerenteTecnico) {
    page.drawText(dados.gerenteTecnico, {
      x: 50,
      y,
      size: 10,
      font: font,
      color: rgb(0, 0, 0),
    });
    y -= 15;
    page.drawText("Gerente Técnico", {
      x: 50,
      y,
      size: 9,
      font: font,
      color: rgb(0, 0, 0),
    });
    y -= 15;
    if (dados.crq) {
      page.drawText(`CRQ ${dados.crq}`, {
        x: 50,
        y,
        size: 9,
        font: font,
        color: rgb(0, 0, 0),
      });
    }
  }

  // Adicionar disclaimer na última página (se fornecido)
  if (disclaimerImage) {
    const disclaimerDims = disclaimerImage.scale(0.8);
    checkNewPage(disclaimerDims.height + 40);

    page.drawImage(disclaimerImage, {
      x: 50,
      y: y - disclaimerDims.height,
      width: disclaimerDims.width,
      height: disclaimerDims.height,
    });
  }

  const pdfBytes = await pdfDoc.save();

  return {
    base64: Buffer.from(pdfBytes).toString("base64"),
  };
}
