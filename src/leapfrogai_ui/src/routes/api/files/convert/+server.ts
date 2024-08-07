import type { RequestHandler } from './$types';
import { error, fail } from '@sveltejs/kit';
import { superValidate } from 'sveltekit-superforms';
import { yup } from 'sveltekit-superforms/adapters';
import { fileSchema } from '$schemas/files';

const path = require('path');
const fs = require('fs').promises;

const libre = require('libreoffice-convert');
libre.convertAsync = require('util').promisify(libre.convert);

export const POST: RequestHandler = async ({ request, locals: { session } }) => {
  if (!session) {
    error(401, 'Unauthorized');
  }

  const form = await superValidate(request, yup(fileSchema));
  if (!form.valid) {
    return fail(400, { form });
  }

  const file = form.data.file;
  console.log('file', file)

  if (file) {
    const ext = '.pdf';
    // const inputPath = path.join(__dirname, '/resources/example.docx');
    const outputPath = path.join(__dirname, `/conversions/${file.name}${ext}`);

    // Read file
    // const docxBuf = await fs.readFile(inputPath);

    // Convert it to pdf format with undefined filter (see Libreoffice docs about filter)
    let pdfBuf = await libre.convertAsync(file.arrayBuffer(), ext, undefined);

    // Here in done you have pdf file which you can save or transfer in another stream
    await fs.writeFile(outputPath, pdfBuf);
    return new Response(pdfBuf, {
      headers: {
        'Content-Type': 'application/pdf',
        'Content-Disposition': 'attachment; filename="output.pdf"',
      },
    });
    //Should not reach this line, this case should be caught by form validation above
  } else return fail(400, { form });
};
