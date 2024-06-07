import type { LFAssistant } from '$lib/types/assistants';

export const MAX_LABEL_SIZE = 100;
export const DEFAULT_ASSISTANT_TEMP = 0.2;
export const MAX_AVATAR_SIZE = 5000000;
export const MAX_FILE_SIZE = 512000000;

// PER OPENAI SPEC
export const ASSISTANTS_NAME_MAX_LENGTH = 256;
export const ASSISTANTS_DESCRIPTION_MAX_LENGTH = 512;
export const ASSISTANTS_INSTRUCTIONS_MAX_LENGTH = 256000;

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

export const NO_FILE_ERROR_TEXT = 'Please upload an image or select a pictogram';
export const AVATAR_FILE_SIZE_ERROR_TEXT = `File must be less than ${MAX_AVATAR_SIZE / 1000000} MB`;
export const FILE_SIZE_ERROR_TEXT = `File must be less than ${MAX_FILE_SIZE / 1000000} MB`;
