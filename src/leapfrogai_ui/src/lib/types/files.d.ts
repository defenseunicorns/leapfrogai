import type { SuperValidated } from 'sveltekit-superforms';
import type { FileObject } from 'openai/resources/files';

export type FileUploadStatus = 'uploading' | 'complete' | 'error' | 'hide';

export type VectorStatus = 'in_progress' | 'completed' | 'cancelled' | 'failed';

export type LFFileObject = Omit<FileObject, 'status'> & {
  status: FileUploadStatus;
};

export type PendingOrErrorFile = Pick<LFFileObject, 'id' | 'filename' | 'status' | 'created_at'>;

// This type is taken from SuperValidated, leaving the any
export type FilesForm = SuperValidated<
  { files?: (File | null | undefined)[] | undefined },
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  any,
  { files?: (File | null | undefined)[] | undefined }
>;

export type FileMetadata = {
  id?: string;
  name: string;
  type: string;
  status: FileUploadStatus;
  text: string;
  errorText?: string;
};

export type LFFile = File & {
  id?: string;
};
