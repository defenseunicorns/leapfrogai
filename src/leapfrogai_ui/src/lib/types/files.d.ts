import type { SuperValidated } from 'sveltekit-superforms';

export type FileUploadStatus = 'uploading' | 'complete' | 'error' | 'hide';

export type FileRow = {
  id: string;
  filename: string;
  created_at: number | null;
  status: FileUploadStatus;
  vectorStatus?: 'in_progress' | 'completed' | 'cancelled' | 'failed';
};

// This type is taken from SuperValidated, leaving the any
export type FilesForm = SuperValidated<
  { files?: (File | null | undefined)[] | undefined },
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  any,
  { files?: (File | null | undefined)[] | undefined }
>;
