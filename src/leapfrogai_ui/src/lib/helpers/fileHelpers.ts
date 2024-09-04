import type { FileRow } from '$lib/types/files';
import type { FileObject } from 'openai/resources/files';

export const convertFileObjectToFileRows = (files: FileObject[]): FileRow[] =>
  files.map((file) => ({
    id: file.id,
    filename: file.filename,
    created_at: file.created_at * 1000,
    status: 'hide'
  }));
