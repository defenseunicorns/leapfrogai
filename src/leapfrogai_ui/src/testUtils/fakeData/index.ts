import { faker } from '@faker-js/faker';

const todayOverride = new Date('2024-03-20T00:00');

const userId = faker.string.uuid();

export const getFakeMessage = ({
	id = faker.string.uuid(),
	role = 'user',
	conversation_id = faker.string.uuid(),
	user_id = faker.string.uuid(),
	content = faker.lorem.lines(1),
	inserted_at = new Date().toISOString()
}: Partial<Message>): Message => ({
	id,
	role,
	user_id,
	conversation_id,
	content,
	inserted_at
});

type FakeConversationOptions = {
	label?: string;
	numMessages?: number;
	messages?: Message[];
	insertedAt?: string;
};

export const getFakeConversation = (options: FakeConversationOptions = {}): Conversation => {
	const {
		label = faker.lorem.sentence(4),
		messages = [],
		insertedAt = new Date().toISOString(),
		numMessages = 0
	} = options;

	const conversationId = faker.string.uuid();

	if (messages.length === 0 && numMessages > 0) {
		for (let i = 0; i < numMessages; i++) {
			messages.push(
				getFakeMessage({
					role: i % 2 === 0 ? 'user' : 'system',
					conversation_id: conversationId,
					user_id: userId
				})
			);
		}
	}

	return {
		id: conversationId,
		label,
		user_id: userId,
		inserted_at: insertedAt,
		messages: messages
	};
};

export const fakeConversations: Conversation[] = [
	// today
	getFakeConversation({ numMessages: 2, insertedAt: todayOverride.toDateString() }),
	// yesterday
	getFakeConversation({
		numMessages: 2,
		insertedAt: new Date(
			todayOverride.getFullYear(),
			todayOverride.getMonth(),
			todayOverride.getDate() - 1
		).toDateString()
	}),
	// This Month
	getFakeConversation({
		numMessages: 2,
		insertedAt: new Date(todayOverride.getFullYear(), todayOverride.getMonth(), 10).toDateString()
	})
];
