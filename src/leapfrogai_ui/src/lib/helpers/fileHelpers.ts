import type { FileMetadata, FileRow } from '$lib/types/files';
import type { FileObject } from 'openai/resources/files';
import { FILE_CONTEXT_TOO_LARGE_ERROR_MSG } from '$constants/errors';

export const convertFileObjectToFileRows = (files: FileObject[]): FileRow[] =>
  files.map((file) => ({
    id: file.id,
    filename: file.filename,
    created_at: file.created_at * 1000,
    status: 'hide'
  }));

export const removeFilesUntilUnderLimit = (parsedFiles: FileMetadata[], max: number) => {
  const numFiles = parsedFiles.length;
  let numFilesReset = 0;
  let totalTextLength = parsedFiles.reduce((total, file) => total + JSON.stringify(file).length, 0);
  // Remove the largest files until the total size is within the allowed limit
  while (totalTextLength > max) {
    if (numFilesReset === numFiles) break;
    let largestIndex = 0;
    for (let i = 1; i < numFiles; i++) {
      const item = JSON.stringify(parsedFiles[i]);
      const largestItem = JSON.stringify(parsedFiles[largestIndex]);
      if (item.length > largestItem.length) {
        largestIndex = i;
      }
    }

    // remove the text and set to error status
    parsedFiles[largestIndex] = {
      ...parsedFiles[largestIndex],
      text: '',
      status: 'error',
      errorText: FILE_CONTEXT_TOO_LARGE_ERROR_MSG
    };
    numFilesReset += 1;
    totalTextLength = parsedFiles.reduce((total, file) => total + JSON.stringify(file).length, 0); //recalculate total size
  }
};
