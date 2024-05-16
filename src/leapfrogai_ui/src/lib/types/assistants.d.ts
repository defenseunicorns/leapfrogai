import type {Assistant} from "openai/resources/beta";

type AssistantInput = {
  name: string;
  description: string;
  instructions: string;
  temperature: number;
  data_sources?: string;
  avatar?: File | null;
  pictogram?: string;
};

type EditAssistantInput = AssistantInput & { id: string };


type LFAssistant = Assistant & {
  metadata: {
    created_by: string | null; //user id
    data_sources?: string; // vector store ids, array as string
    avatar?: string;
    pictogram?: string;
    [key: string]: unknown;
  };
};

