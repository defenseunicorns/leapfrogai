type Conversation = {
	id: string;
	label: string;
	user_id: string;
	messages: Message[];
	inserted_at: string;
};

type Message = {
	id: string;
	role: 'user' | 'system';
	user_id: string;
	conversation_id: string;
	content: string;
	inserted_at: string;
};

type AIMessage = {
	role: 'user' | 'system';
	content: string;
};
