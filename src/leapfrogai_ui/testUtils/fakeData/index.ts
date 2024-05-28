// Can't use import aliases here because playwright needs these and it doens't work with relative imports
import { faker } from '@faker-js/faker';
import { assistantDefaults, DEFAULT_ASSISTANT_TEMP } from '../../src/lib/constants';
import type { AssistantInput, LFAssistant } from '../../src/lib/types/assistants';
import type { LFMessage } from '../../src/lib/types/messages';
import type { LFThread, Roles } from '../../src/lib/types/threads';
import type { MessageContent } from 'openai/resources/beta/threads/messages';
import { getUnixSeconds } from '../../src/lib/helpers/dates';

const todayOverride = new Date('2024-03-20T00:00');

const userId = faker.string.uuid();

type FakeMessageOptions = {
  id?: string;
  role?: Roles;
  thread_id?: string;
  user_id?: string;
  content?: string;
  created_at?: number;
};
export const getFakeMessage = (options: FakeMessageOptions = {}): LFMessage => {
  const messageContent: MessageContent[] = [
    { type: 'text', text: { value: options.content || faker.lorem.lines(1), annotations: [] } }
  ];

  const {
    id = `message_${faker.string.uuid()}`,
    role = 'user',
    user_id = faker.string.uuid(),
    thread_id = faker.string.uuid(),
    created_at = getUnixSeconds(new Date())
  } = options;

  return {
    id,
    assistant_id: null,
    attachments: null,
    completed_at: created_at,
    content: messageContent,
    created_at,
    incomplete_at: null,
    incomplete_details: null,
    metadata: { user_id },
    object: 'thread.message',
    role,
    run_id: null,
    status: 'completed',
    thread_id
  };
};

type FakeThreadOptions = {
  id?: string;
  label?: string;
  numMessages?: number;
  messages?: LFMessage[];
  created_at?: number;
};

export const getFakeThread = (options: FakeThreadOptions = {}): LFThread => {
  const thread_id = options.id || faker.string.uuid();

  const {
    label = faker.lorem.sentence(4),
    messages = [],
    created_at = getUnixSeconds(new Date()),
    numMessages = 0
  } = options;

  if (messages.length === 0 && numMessages > 0) {
    for (let i = 0; i < numMessages; i++) {
      messages.push(
        getFakeMessage({
          role: i % 2 === 0 ? 'user' : 'assistant',
          thread_id,
          user_id: userId
        })
      );
    }
  }

  return {
    id: thread_id,
    created_at,
    metadata: {
      label,
      user_id: userId
    },
    object: 'thread',
    tool_resources: null,
    messages
  };
};

export const fakeThreads: LFThread[] = [
  // today
  getFakeThread({ numMessages: 2, created_at: getUnixSeconds(todayOverride) }),
  // yesterday
  getFakeThread({
    numMessages: 2,
    created_at: getUnixSeconds(
      new Date(todayOverride.getFullYear(), todayOverride.getMonth(), todayOverride.getDate() - 1)
    )
  }),
  // This Month
  getFakeThread({
    numMessages: 2,
    created_at: getUnixSeconds(new Date(todayOverride.getFullYear(), todayOverride.getMonth(), 10))
  })
];

export const getFakeAssistant = (): LFAssistant => {
  return {
    id: faker.string.uuid(),
    ...assistantDefaults,
    name: faker.person.fullName(),
    description: faker.lorem.sentence(),
    instructions: faker.lorem.paragraph(),
    temperature: DEFAULT_ASSISTANT_TEMP,
    metadata: {
      user_id: faker.string.uuid(),
      data_sources: '',
      pictogram: 'default',
      avatar: undefined
    },
    created_at: Date.now()
  };
};

export const getFakeAssistantInput = (): AssistantInput => {
  return {
    name: faker.person.fullName(),
    description: faker.lorem.sentence(),
    instructions: faker.lorem.paragraph(),
    temperature: DEFAULT_ASSISTANT_TEMP,
    data_sources: '',
    pictogram: 'default',
    avatar: ''
  };
};
