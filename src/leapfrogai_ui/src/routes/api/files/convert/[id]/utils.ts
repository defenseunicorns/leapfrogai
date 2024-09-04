import libre from 'libreoffice-convert';
import { promisify } from 'util';

// Note - this throws a warning, but it seems erroneous as libre.convert does not return a promise and this is
// IAW with the documentation:
// (node:18447) [DEP0174] DeprecationWarning: Calling promisify on a function that returns a Promise is likely a mistake.
const convertAsync = promisify(libre.convert);

export const convertFileToPdf = async (fileArrayBuffer: ArrayBuffer, filename: string) => {
  const ext = '.pdf';
  const pdfBuf = await convertAsync(Buffer.from(fileArrayBuffer), ext, undefined);

  return new Response(pdfBuf, {
    headers: {
      'Content-Type': 'application/pdf',
      'Content-Disposition': `attachment; filename="${filename}${ext}"`
    }
  });
};
