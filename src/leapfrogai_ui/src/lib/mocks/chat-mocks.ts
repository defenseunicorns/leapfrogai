import { http, HttpResponse, delay } from 'msw';
import { faker } from '@faker-js/faker';
import { server } from '../../../vitest-setup';

type MockChatCompletionOptions = {
	responseMsg?: string[];
	withDelay?: boolean;
	delayTime?: number;
};
export const mockChatCompletion = (
	options: MockChatCompletionOptions = {
		responseMsg: ['Fake', 'AI', 'Response'],
		withDelay: false,
		delayTime: 0
	}
) => {
	const encoder = new TextEncoder();

	server.use(
		http.post('/api/chat', async () => {
			if (options.withDelay) {
				await delay(options.delayTime);
			}
			const stream = new ReadableStream({
				start(controller) {
					options.responseMsg?.forEach((msg) => controller.enqueue(encoder.encode(msg)));
					controller.close();
				}
			});
			return new HttpResponse(stream, { headers: { 'Content-Type': 'text/plain' } });
		})
	);
};

export const mockChatCompletionError = () => {
	server.use(
		http.post('/api/chat', async () => {
			return new HttpResponse(null, { status: 500 });
		})
	);
};

// export const mockNewChatSubmission = (fakeConversation: Conversation, fakeMessage: Message) => {
// 	server.use(
// 		http.post('/', () => {
// 			return HttpResponse.json({
// 				type: 'success',
// 				status: 200,
// 				// Svelte form actions return data in a weird format that uses templating to build the object
// 				// not sure how to easily replicate this yet without hard coding the values like this
// 				data: `[{"newConversation":1},{"id":2,"user_id":3,"label":4,"inserted_at":5,"messages":6},"${fakeConversation.id}","${fakeConversation.user_id}","${fakeConversation.label}","${fakeConversation.inserted_at}",[7],{"id":8,"user_id":3,"conversation_id":2,"role":9,"content":4,"inserted_at":10},"${fakeMessage.id}","user","${fakeMessage.inserted_at}"]`
// 			});
// 		})
// 	);
// };

export const mockNewConversation = () => {
	server.use(
		http.post('/api/conversations/new', () => {
			return HttpResponse.json({
				id: faker.string.uuid(),
				user_id: faker.string.uuid(),
				label: faker.lorem.words(5),
				inserted_at: new Date().toLocaleString()
			});
		})
	);
};

export const mockNewMessage = (fakeMessage: Message) => {
	server.use(
		http.post('/api/messages/new', () => {
			return HttpResponse.json({ message: fakeMessage });
		})
	);
};

export const mockNewConversationError = () => {
	server.use(http.post('/api/conversations/new', () => new HttpResponse(null, { status: 500 })));
};
export const mockNewMessageError = () => {
	server.use(http.post('/api/messages/new', () => new HttpResponse(null, { status: 500 })));
};


export const mockDeleteConversation = () => {
	server.use(
		http.delete('/api/conversations/delete', () => new HttpResponse(null, { status: 204 }))
	);
};

export const mockDeleteConversationError = () => {
	server.use(
		http.delete('/api/conversations/delete', () => new HttpResponse(null, { status: 500 }))
	);
};

export const mockEditConversationLabel = () => {
	server.use(
		http.put('/api/conversations/update/label', () => new HttpResponse(null, { status: 204 }))
	);
};

export const mockEditConversationLabelError = () => {
	server.use(
		http.put('/api/conversations/update/label', () => new HttpResponse(null, { status: 500 }))
	);
};
