import { array, object, ObjectSchema, string } from 'yup';
import { MAX_LABEL_SIZE } from '$lib/constants';

export const messageSchema: ObjectSchema<Message> = object({
	id: string().uuid().required(),
	user_id: string().uuid().required(),
	conversation_id: string().uuid().required(),
	content: string().required(),
	role: string<'user' | 'system'>().required(),
	inserted_at: string().required()
})
	.noUnknown(true)
	.strict();

export const conversationSchema: ObjectSchema<Conversation> = object({
	id: string().uuid().required(),
	user_id: string().uuid().required(),
	messages: array().of(messageSchema).required(),
	label: string().required(),
	inserted_at: string().required()
})
	.noUnknown(true)
	.strict();

export const conversationsSchema = array().of(conversationSchema);

export const messageInputSchema: ObjectSchema<AIMessage> = object({
	content: string().required(),
	role: string<'user' | 'system'>().required()
})
	.noUnknown(true)
	.strict();

export const messagesInputSchema = object({ messages: array().of(messageInputSchema).strict() })
	.noUnknown(true)
	.strict();

export const supabaseMessagesInputSchema = messageInputSchema
	.shape({
		id: string().uuid().optional(),
		conversation_id: string().uuid().required(),
		inserted_at: string().optional()
	})
	.noUnknown(true)
	.strict();

export const uuidSchema = object({
	conversationId: string().uuid().required()
})
	.noUnknown(true)
	.strict();

const labelSchema = string().min(1).max(MAX_LABEL_SIZE).required();

export const newConversationInputSchema = object({
	label: labelSchema,
	inserted_at: string().optional()
})
	.noUnknown(true)
	.strict();

export const updateConversationSchema = object({
	id: string().uuid().required(),
	label: labelSchema
})
	.noUnknown(true)
	.strict();
