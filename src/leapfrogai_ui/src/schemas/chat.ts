import { array, object, ObjectSchema, string } from 'yup';

export const messageSchema: ObjectSchema<AIMessage> = object({
	content: string().required(),
	role: string<'user' | 'system'>().required()
})
	.noUnknown(true)
	.strict();

export const messagesSchema = array().of(messageSchema).strict();


export const uuidSchema = string().uuid().required();