// Can't use import aliases here because playwright needs these and it doens't work with relative imports
import { faker } from '@faker-js/faker';
import { assistantDefaults, DEFAULT_ASSISTANT_TEMP } from '../../src/lib/constants';
import type { AssistantInput, LFAssistant } from '../../src/lib/types/assistants';
import type { LFMessage, NewMessageInput } from '../../src/lib/types/messages';
import type { LFThread } from '../../src/lib/types/threads';
import type {
  Message as OpenAIMessage,
  MessageContent
} from 'openai/resources/beta/threads/messages';
import { getUnixSeconds } from '../../src/lib/helpers/dates';
import type { FileObject } from 'openai/resources/files';
import type { Profile } from '$lib/types/profile';
import type { Session } from '@supabase/supabase-js';

const todayOverride = new Date('2024-03-20T00:00');

const userId = faker.string.uuid();

type FakeMessageOptions = {
  id?: string;
  role?: 'user' | 'assistant';
  thread_id?: string;
  user_id?: string;
  content?: string;
  assistant_id?: string;
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
    created_at = getUnixSeconds(new Date()),
    assistant_id = undefined
  } = options;

  return {
    id,
    assistant_id: assistant_id,
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
    pictogram: 'default',
    avatar: ''
  };
};

type GetFakeFilesOptions = {
  numFiles?: number;
  created_at?: Date;
};
export const getFakeFiles = (options: GetFakeFilesOptions = {}) => {
  const { numFiles = 2, created_at = new Date() } = options;

  const files: FileObject[] = [];
  for (let i = 0; i < numFiles; i++) {
    files.push({
      id: faker.string.uuid(),
      bytes: 32,
      created_at: getUnixSeconds(created_at),
      filename: `${faker.word.noun()}.pdf`,
      object: 'file',
      purpose: 'assistants',
      status: 'processed'
    });
  }
  return files;
};

type GetFakeProfileArgs = {
  id?: string;
  full_name?: string;
  thread_ids?: string[];
};
export const getFakeProfile = ({
  id = faker.string.uuid(),
  full_name = faker.person.fullName(),
  thread_ids = []
}: GetFakeProfileArgs): Profile => {
  return { id, full_name, thread_ids };
};

type GetFakeSessionArgs = {
  user_id?: string;
  email?: string;
  full_name?: string;
};

export const getFakeSession = ({
  user_id = faker.string.uuid(),
  email = faker.internet.email(),
  full_name = faker.person.fullName()
}: GetFakeSessionArgs = {}): Session => {
  return {
    provider_token: null,
    provider_refresh_token: null,
    access_token: '',
    refresh_token: '',
    expires_in: 3600,
    expires_at: undefined,
    token_type: 'bearer',
    user: {
      id: user_id,
      app_metadata: { provider: 'keycloak', providers: ['keycloak'] },
      user_metadata: {
        email,
        email_verified: true,
        full_name,
        iss: 'https://keycloak.admin.uds.dev/realms/uds',
        name: full_name,
        phone_verified: false,
        provider_id: faker.string.uuid(),
        sub: faker.string.uuid()
      },
      aud: 'authenticated',
      confirmation_sent_at: undefined,
      recovery_sent_at: undefined,
      email_change_sent_at: undefined,
      new_email: undefined,
      new_phone: undefined,
      created_at: new Date().toISOString()
    }
  };
};

export const getFakeOpenAIMessage = ({
  thread_id,
  content,
  role
}: NewMessageInput): OpenAIMessage => {
  return {
    id: `msg_${faker.string.uuid()}`,
    role,
    thread_id,
    content: [{ type: 'text', text: { value: content, annotations: [] } }],
    assistant_id: null,
    created_at: getUnixSeconds(new Date()),
    incomplete_at: null,
    incomplete_details: null,
    metadata: null,
    object: 'thread.message',
    status: 'completed',
    run_id: null,
    attachments: null,
    completed_at: getUnixSeconds(new Date())
  };
};

export const getFakeFileObject = (): FileObject => ({
  id: `file_${faker.string.uuid()}`,
  bytes: 64,
  created_at: getUnixSeconds(new Date()),
  filename: `${faker.word.noun()}.pdf`,
  object: 'file',
  purpose: 'assistants'
});
