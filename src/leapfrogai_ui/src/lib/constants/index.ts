import type { LFAssistant } from '$lib/types/assistants';
import { env } from '$env/dynamic/public';

export const MAX_LABEL_SIZE = 100;
export const DEFAULT_ASSISTANT_TEMP = 0.2;
export const MAX_AVATAR_SIZE = 5000000;
export const MAX_FILE_SIZE = 512000000;
export const MAX_AUDIO_FILE_SIZE = 25000000;
export const MAX_FILE_NAME_SIZE = 27;
export const MAX_NUM_FILES_UPLOAD = 10; // for chat completion

// PER OPENAI SPEC
export const ASSISTANTS_NAME_MAX_LENGTH = 256;
export const ASSISTANTS_DESCRIPTION_MAX_LENGTH = 512;
export const ASSISTANTS_INSTRUCTIONS_MAX_LENGTH = 256000;

// 1 token is approx 4 characters, whenever our max context window changes, this value will need to change
// leave a small buffer to prevent overflowing context (ex. 32k context window, set here to 31.750k)
export const APPROX_MAX_CHARACTERS = 31750;

// TODO - once using API to save, these defaults should be returned by the POST call and would not need to be supplied
// We only need to default the model and tools
export const assistantDefaults: Omit<LFAssistant, 'id' | 'created_at'> = {
  object: 'assistant',
  name: null,
  description: null,
  model: 'vllm',
  instructions: null,
  tools: [
    {
      type: 'file_search'
    }
  ],
  tool_resources: null,
  metadata: {
    user_id: ''
  },
  top_p: 1.0,
  temperature: 0.2,
  response_format: 'auto'
};

export const ACCEPTED_AUDIO_FILE_TYPES = [
  '.flac',
  '.mp3',
  '.mp4',
  '.mpeg',
  '.mpga',
  '.m4a',
  '.ogg',
  '.wav',
  '.webm'
];

export const ACCEPTED_FILE_TYPES = [
  '.pdf',
  '.txt',
  '.text',
  '.xls',
  '.xlsx',
  '.ppt',
  '.pptx',
  '.doc',
  '.docx',
  '.csv',
  ...ACCEPTED_AUDIO_FILE_TYPES
];

export const ACCEPTED_AUDIO_FILE_MIME_TYPES = [
  'audio/flac',
  'audio/mpeg',
  'audio/mp4',
  'audio/x-m4a',
  'audio/mpeg',
  'audio/ogg',
  'audio/wav',
  'audio/webm'
];

export const ACCEPTED_MIME_TYPES = [
  'application/pdf', // .pdf
  'text/plain', // .txt, .text
  'application/vnd.ms-excel', // .xls
  'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', // .xlsx
  'application/vnd.ms-powerpoint', // .ppt
  'application/vnd.openxmlformats-officedocument.presentationml.presentation', // .pptx
  'application/msword', // .doc
  'application/vnd.openxmlformats-officedocument.wordprocessingml.document', //.docx,
  'text/csv',
  ...ACCEPTED_AUDIO_FILE_MIME_TYPES
];

export const FILE_TYPE_MAP = {
  'application/pdf': 'PDF',
  'text/plain': 'TXT',
  'application/octet-stream': 'TEXT',
  'application/vnd.ms-excel': 'XLS',
  'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': 'XLSX',
  'application/vnd.ms-powerpoint': 'PPT',
  'application/vnd.openxmlformats-officedocument.presentationml.presentation': 'PPTX',
  'application/msword': 'DOC',
  'application/vnd.openxmlformats-officedocument.wordprocessingml.document': 'DOCX',
  'text/csv': 'CSV',
  ...ACCEPTED_AUDIO_FILE_MIME_TYPES.reduce((acc, type) => ({ ...acc, [type]: 'AUDIO' }), {})
};

export const NO_FILE_ERROR_TEXT = 'Please upload an image or select a pictogram';
export const AVATAR_FILE_SIZE_ERROR_TEXT = `File must be less than ${MAX_AVATAR_SIZE / 1000000} MB`;
export const FILE_SIZE_ERROR_TEXT = `File must be less than ${MAX_FILE_SIZE / 1000000} MB`;
export const AUDIO_FILE_SIZE_ERROR_TEXT = `Audio file must be less than ${MAX_AUDIO_FILE_SIZE / 1000000} MB`;
export const INVALID_FILE_TYPE_ERROR_TEXT = `Invalid file type, accepted types are: ${ACCEPTED_FILE_TYPES.join(', ')}`;
export const INVALID_AUDIO_FILE_TYPE_ERROR_TEXT = `Invalid file type, accepted types are: ${ACCEPTED_AUDIO_FILE_TYPES.join(', ')}`;
export const NO_SELECTED_ASSISTANT_ID = 'noSelectedAssistantId';

export const FILE_UPLOAD_PROMPT = "The following are the user's files: ";

export const ADJUSTED_MAX_CHARACTERS =
  APPROX_MAX_CHARACTERS - Number(env.PUBLIC_MESSAGE_LENGTH_LIMIT) - FILE_UPLOAD_PROMPT.length - 2;
