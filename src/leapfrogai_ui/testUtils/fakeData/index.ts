import { faker } from '@faker-js/faker';
import { assistantDefaults, DEFAULT_ASSISTANT_TEMP } from '../../src/lib/constants';

const todayOverride = new Date('2024-03-20T00:00');

const userId = faker.string.uuid();

type FakeMessageOptions = {
  id?: string;
  role?: Roles;
  conversation_id?: string;
  user_id?: string;
  content?: string;
  inserted_at?: string;
};
export const getFakeMessage = (options: FakeMessageOptions = {}): Message => {
  const {
    id = faker.string.uuid(),
    role = 'user',
    user_id = faker.string.uuid(),
    conversation_id = faker.string.uuid(),
    content = faker.lorem.lines(1),
    inserted_at = new Date().toISOString()
  } = options;
  return {
    id,
    role,
    user_id,
    conversation_id,
    content,
    inserted_at
  };
};

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
          role: i % 2 === 0 ? 'user' : 'assistant',
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

export const getFakeAssistant = (): Assistant => {
  return {
    id: faker.string.uuid(),
    ...assistantDefaults,
    name: faker.person.fullName(),
    description: faker.lorem.sentence(),
    instructions: faker.lorem.paragraph(),
    temperature: DEFAULT_ASSISTANT_TEMP,
    metadata: {
      created_by: faker.string.uuid(),
      data_sources: '',
      pictogram: 'default',
      avatar: undefined
    },
    created_at: Date.now()
  };
};

export const getFakeNewAssistantInput = (): NewAssistantInput => {
  return {
    name: faker.person.fullName(),
    description: faker.lorem.sentence(),
    instructions: faker.lorem.paragraph(),
    temperature: DEFAULT_ASSISTANT_TEMP,
    data_sources: '',
    pictogram: 'default',
    avatar: null
  };
};
