import type { FileMetadata, FileRow } from '$lib/types/files';
import type { FileObject } from 'openai/resources/files';
import { ADJUSTED_MAX_CHARACTERS } from '$constants';
import { FILE_CONTEXT_TOO_LARGE_ERROR_MSG } from '$constants/errors';

export const convertFileObjectToFileRows = (files: FileObject[]): FileRow[] =>
  files.map((file) => ({
    id: file.id,
    filename: file.filename,
    created_at: file.created_at * 1000,
    status: 'hide'
  }));

export const removeFilesUntilUnderLimit = (parsedFiles: FileMetadata[]) => {
  let totalTextLength = parsedFiles.reduce((total, file) => total + JSON.stringify(file).length, 0);

  // Sort the files in descending order based on their size
  parsedFiles.sort((a, b) => JSON.stringify(b).length - JSON.stringify(a).length);

  // Remove the largest files until the total size is within the allowed limit
  while (totalTextLength > ADJUSTED_MAX_CHARACTERS) {
    const largestFile = parsedFiles[0]; // The largest file after sorting
    // remove the text and set to error status
    parsedFiles[0] = {
      ...parsedFiles[0],
      text: '',
      status: 'error',
      errorText: FILE_CONTEXT_TOO_LARGE_ERROR_MSG
    };
    totalTextLength -= JSON.stringify(parsedFiles[0]).length; // recalculate the total size
  }
};
