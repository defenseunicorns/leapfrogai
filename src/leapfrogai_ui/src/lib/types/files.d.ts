export type FileRow = {
  id: string;
  filename: string;
  created_at: number | null;
  status: 'uploading' | 'complete' | 'error' | 'hide';
};
