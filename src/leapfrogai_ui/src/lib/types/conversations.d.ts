

type NewConversationInput = {
  label: string;
  inserted_at?: string;
};

type Roles = 'system' | 'user' | 'assistant' | 'function' | 'data' | 'tool';
type NewMessageInput = {
  conversation_id: string;
  content: string;
  role: Roles;
  inserted_at?: string;
};
type Message = NewMessageInput & {
  id: string;
  user_id: string;
  inserted_at: string;
};
