import { writable } from 'svelte/store';
import { MAX_LABEL_SIZE } from '$lib/constants';
import { goto } from '$app/navigation';

type ConversationsStore = {
	conversations: Conversation[];
};

const defaultValues: ConversationsStore = {
	conversations: []
};

const createConversationsStore = () => {
	const { subscribe, set, update } = writable<ConversationsStore>({ ...defaultValues });
	return {
		subscribe,
		set,
		update,
		setConversations: (conversations: Conversation[]) => {
			update((old) => ({ ...old, conversations }));
		},
		changeConversation: async (newId: string | null) => {
			await goto(`/chat/${newId}`);
		},
		newConversation: async (label: string) => {
			const res = await fetch('/api/conversations/new', {
				method: 'POST',
				body: JSON.stringify({ label: label.substring(0, MAX_LABEL_SIZE) }),
				headers: {
					'Content-Type': 'application/json'
				}
			});
			if (res.ok) {
				const newConversation = { ...(await res.json()), messages: [] };
				update((old) => {
					return {
						...old,
						conversations: [...old.conversations, newConversation]
					};
				});
				await goto(`/chat/${newConversation.id}`);
			}
		},

		newMessage: async (conversation_id: string, content: string, role: 'system' | 'user') => {
			const res = await fetch('/api/messages/new', {
				method: 'POST',
				body: JSON.stringify({
					role,
					content,
					conversation_id
				}),
				headers: {
					'Content-Type': 'application/json'
				}
			});
			if (res.ok) {
				const responseMessage = await res.json();

				update((old) => {
					const updatedConversations = [...old.conversations];
					const conversationIndex = old.conversations.findIndex((c) => c.id === conversation_id);
					const oldConversation = old.conversations[conversationIndex];

					updatedConversations[conversationIndex] = {
						...oldConversation,
						messages: [...oldConversation.messages, responseMessage]
					};
					return {
						...old,
						conversations: updatedConversations
					};
				});
			}
		},
		deleteConversation: async (id: string) => {
			update((old) => ({
				...old,
				conversations: old.conversations.filter((c) => c.id !== id)
			}));
			await goto('/chat');
		},
		updateConversationLabel: (id: string, newLabel: string) =>
			update((old) => {
				const updatedConversationIndex = old.conversations.findIndex((c) => c.id === id);
				const updatedConversation = { ...old.conversations[updatedConversationIndex] };
				updatedConversation.label = newLabel;

				const updatedConversations = [...old.conversations];
				updatedConversations[updatedConversationIndex] = updatedConversation;

				return {
					...old,
					conversations: updatedConversations
				};
			})
	};
};

export default createConversationsStore();
