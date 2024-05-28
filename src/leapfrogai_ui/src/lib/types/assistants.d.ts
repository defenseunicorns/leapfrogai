import type { Assistant, AssistantCreateParams } from 'openai/resources/beta/assistants';

type AssistantInput = {
  name: string;
  description: string;
  instructions: string;
  temperature: number;
  data_sources?: string;
  avatar?: string;
  avatarFile?: File | null;
  pictogram?: string;
};

export type LFAssistantCreateParams = AssistantCreateParams & {
  user_id: string;
  data_sources?: string;
  pictogram?: string;
};

type EditAssistantInput = AssistantInput & { id: string };

export type LFAssistant = Assistant & {
  metadata: {
    user_id: string;
    data_sources?: string; // vector store ids, array as string
    avatar?: string;
    pictogram?: string;
    [key: string]: unknown;
  };
};
