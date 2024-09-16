import { MAX_NUM_FILES_UPLOAD } from '$constants/index';

type ToastData = {
  kind: ToastKind;
  title: string;
  subtitle?: string;
};

export const ERROR_SAVING_MSG_TOAST = (override: Partial<ToastData> = {}): ToastData => ({
  kind: 'error',
  title: 'Error',
  subtitle: 'Error saving message. Please try again.',
  ...override
});

export const ERROR_GETTING_AI_RESPONSE_TOAST = (override: Partial<ToastData> = {}): ToastData => ({
  kind: 'error',
  title: 'Error',
  subtitle: 'Error getting AI Response',
  ...override
});

export const ERROR_GETTING_ASSISTANT_MSG_TOAST = (
  override: Partial<ToastData> = {}
): ToastData => ({
  kind: 'error',
  title: 'Error',
  subtitle: 'Error getting Assistant Response',
  ...override
});

export const OPENAI_DOWNLOAD_DISABLED_MSG_TOAST = (
  override: Partial<ToastData> = {}
): ToastData => ({
  kind: 'warning',
  title: 'File download disabled when using OpenAI',
  subtitle: `OpenAI does not allow download of files with purpose 'assistants'`,
  ...override
});

export const FILE_DOWNLOAD_ERROR_MSG_TOAST = (override: Partial<ToastData> = {}): ToastData => ({
  kind: 'error',
  title: 'Error Downloading File',
  subtitle: `Please try again or contact support.`,
  ...override
});

export const CONVERT_FILE_ERROR_MSG_TOAST = (override: Partial<ToastData> = {}): ToastData => ({
  kind: 'warning',
  title: 'Unsupported File Type',
  subtitle: 'Viewing this file type is not currently supported',
  ...override
});

export const ERROR_PROCESSING_FILE_MSG_TOAST = (override: Partial<ToastData> = {}): ToastData => ({
  kind: 'error',
  title: 'Error Processing File',
  ...override
});

export const MAX_NUM_FILES_UPLOAD_MSG_TOAST = (override: Partial<ToastData> = {}): ToastData => ({
  kind: 'error',
  title: 'Too many files',
  subtitle: `Maximum number of files is ${MAX_NUM_FILES_UPLOAD}`,
  ...override
});

export const FILE_VECTOR_TIMEOUT_MSG_TOAST = (override: Partial<ToastData> = {}): ToastData => ({
  kind: 'error',
  title: 'Timeout',
  subtitle: 'There was an error processing assistant files',
  ...override
});

export const FILE_TRANSLATION_ERROR = (override: Partial<ToastData> = {}): ToastData => ({
  kind: 'error',
  title: 'Translation Error',
  subtitle: 'There was an error translating your audio file',
  ...override
});
