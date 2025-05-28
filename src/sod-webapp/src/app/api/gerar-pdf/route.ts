import type { NextApiRequest, NextApiResponse } from 'next';
import formidable from 'formidable';
import fs from 'fs';
import { gerarPDF } from '../../../backend/reports/geraPdf';

// Desativa o body parser padrão
export const config = {
  api: {
    bodyParser: false,
  },
};

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Método não permitido' });
  }

  const form = formidable({ multiples: true });

  form.parse(req, async (err, fields, files) => {
    if (err) {
      return res.status(500).json({ error: 'Erro ao processar formulário' });
    }

    // Extrai os arquivos de forma segura
    const extractBuffers = (fileField: any): Buffer[] => {
      if (!fileField) return [];

      const fileArray = Array.isArray(fileField) ? fileField : [fileField];
      return fileArray.map(f => fs.readFileSync(f.filepath));
    };

    const termicaBuffers = extractBuffers(files.termica);
    const retracaoBuffers = extractBuffers(files.retracao);

    try {
      const pdf = await gerarPDF(termicaBuffers, retracaoBuffers);
      return res.status(200).json(pdf);
    } catch (e) {
      console.error(e);
      return res.status(500).json({ error: 'Erro ao gerar o PDF' });
    }
  });
}
