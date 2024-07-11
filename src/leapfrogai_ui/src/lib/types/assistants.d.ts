import type { Assistant } from 'openai/resources/beta/assistants';

type AssistantInput = {
  name: string;
  description: string;
  instructions: string;
  temperature: number;
  data_sources?: Array<string | undefined>;
  vectorStoreId?: string;
  avatar?: string;
  avatarFile?: File | null;
  pictogram?: string;
};

type EditAssistantInput = AssistantInput & { id: string };

export type LFAssistant = Assistant & {
  metadata: {
    user_id: string;
    avatar?: string;
    pictogram?: string;
    [key: string]: unknown;
  };
};
