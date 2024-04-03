import { array, object, ObjectSchema, string } from 'yup';
import { MAX_LABEL_SIZE } from '$lib/constants';

export const messageSchema: ObjectSchema<AIMessage> = object({
	content: string().required(),
	role: string<'user' | 'system'>().required()
})
	.noUnknown(true)
	.strict();

export const messagesSchema = object({ messages: array().of(messageSchema).strict() })
	.noUnknown(true)
	.strict();

export const uuidSchema = object({
	conversationId: string().uuid().required()
})
	.noUnknown(true)
	.strict();

export const newConversationSchema = object({
	label: string().min(1).max(MAX_LABEL_SIZE).required()
})
	.noUnknown(true)
	.strict();
