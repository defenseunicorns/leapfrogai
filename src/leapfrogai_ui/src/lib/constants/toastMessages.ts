type ToastData = {
  kind: ToastKind;
  title: string;
  subtitle?: string;
};

export const ERROR_SAVING_MSG_TOAST: ToastData = {
  kind: 'error',
  title: 'Error',
  subtitle: 'Error saving message. Please try again.'
};

export const ERROR_GETTING_AI_RESPONSE_TOAST: ToastData = {
  kind: 'error',
  title: 'Error',
  subtitle: 'Error getting AI Response'
};

export const ERROR_GETTING_ASSISTANT_MSG_TOAST: ToastData = {
  kind: 'error',
  title: 'Error',
  subtitle: 'Error getting Assistant Response'
};

export const OPENAI_DOWNLOAD_DISABLED_MSG_TOAST: ToastData = {
  kind: 'warning',
  title: 'File download disabled when using OpenAI',
  subtitle: `OpenAI does not allow download of files with purpose 'assistants'`
};

export const FILE_DOWNLOAD_ERROR_MSG_TOAST: ToastData = {
  kind: 'error',
  title: 'Error Downloading File',
  subtitle: `Please try again or contact support.`
};

export const CONVERT_FILE_ERROR_MSG_TOAST: ToastData = {
  kind: 'warning',
  title: 'Unsupported File Type',
  subtitle: 'Viewing this file type is not currently supported'
};
