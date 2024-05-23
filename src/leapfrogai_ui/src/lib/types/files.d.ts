

export type FileRow = {
    id: string;
    filename: string;
    created_at: number;
    status: 'uploading' | 'complete' | 'error' | 'hide';
};