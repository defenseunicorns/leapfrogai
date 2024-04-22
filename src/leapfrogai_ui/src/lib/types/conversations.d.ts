type NewConversationInput = {
	label: string;
	inserted_at?: string;
};

type Conversation = NewConversationInput & {
	id: string;
	user_id: string;
	messages: Message[];
	label: string;
	inserted_at: string;
};

type NewMessageInput = {
	conversation_id: string;
	content: string;
	role: 'system' | 'user';
	inserted_at? : string;
};
type Message = NewMessageInput & {
	id: string;
	user_id: string;
	inserted_at: string;
};

type AIMessage = {
	role: 'user' | 'system';
	content: string;
};
