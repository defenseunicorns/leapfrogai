import { server } from '../../../vitest-setup';
import { http, HttpResponse } from 'msw';
import { faker } from '@faker-js/faker';
import { assistantDefaults } from '$lib/constants';

export const mockAssistantCreation = (expectedRequestData: NewAssistantInput) => {
  server.use(
    http.post('/api/assistants/new', async ({ request }) => {
      const requestData = await request.json();

      // Test request data received in the request body matches the expected format
      if (JSON.stringify(requestData) !== JSON.stringify(expectedRequestData))
        return HttpResponse.json({ success: false }, { status: 500 });

      const fakeAssistant: Assistant = {
        ...assistantDefaults,
        ...expectedRequestData,
        metadata: {
          ...assistantDefaults.metadata,
          ...expectedRequestData.metadata,
          created_by: faker.string.uuid()
        },
        id: faker.string.uuid(),
        created_at: Date.now()
      };
      return HttpResponse.json({ assistant: fakeAssistant });
    })
  );
};

export const mockNewAssistantError = () => {
  server.use(http.post('/api/assistants/new', () => new HttpResponse(null, { status: 500 })));
};
