type NewAssistantInput = {
  name: string;
  description: string;
  instructions: string;
  temperature: number;
  data_sources?: string;
  avatar?: File | null;
  pictogram?: string;
};

type ToolResources = {
  code_interpreter: string[];
  file_search: string[];
};

type Tools = 'code_interpreter' | 'file_search' | 'function';

type Assistant = {
  id: string;
  object: string;
  name: string | null;
  description: string | null;
  model: string;
  instructions: string | null;
  tools: { type: Tools }[];
  tool_resources: ToolResources | null;
  metadata: {
    created_by: string | null; //user id
    data_sources?: string; // vector store ids, array as string
    avatar?: string;
    pictogram?: string;
    [key: string]: unknown;
  };
  temperature: number | null;
  top_p: number | null;
  response_format: string | { type: string };
  created_at: number;
};
