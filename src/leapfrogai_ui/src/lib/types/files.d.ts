import type { SuperValidated } from 'sveltekit-superforms';

export type FileUploadStatus = 'uploading' | 'complete' | 'error' | 'hide';

export type FileRow = {
  id: string;
  filename: string;
  created_at: number | null;
  status: FileUploadStatus;
};


export type FilesForm = SuperValidated<
  { files?: (File | null | undefined)[] | undefined },
  any,
  { files?: (File | null | undefined)[] | undefined }
>;
