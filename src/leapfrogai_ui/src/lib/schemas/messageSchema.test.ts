import messageSchema from "$schemas/messageSchema";
import type {LFMessage} from "$lib/types/messages";
import {ValidationError} from "yup";

describe('Message Schema', () => {
    it('should validate a valid message', async () => {

        const validMessage: LFMessage = {
            id: 'msg_123',
            assistant_id: null,
            attachments: null,
            completed_at: null,
            content: [
                {
                    text: {
                        annotations: [
                            {
                                end_index: 10,
                                file_citation: {
                                    file_id: 'file_123',
                                    quote: 'example quote',
                                },
                                start_index: 0,
                                text: 'example text',
                                type: 'file_citation',
                            },
                        ],
                        value: 'This is an example message.',
                    },
                    type: 'text',
                },
            ],
            created_at: 1625077335,
            incomplete_at: null,
            incomplete_details: null,
            metadata: null,
            object: 'thread.message',
            role: 'user',
            run_id: null,
            status: 'completed',
            thread_id: 'thread_123',
        };

        await expect(messageSchema.validate(validMessage)).resolves.toBe(validMessage);
    });

    it('should invalidate a message with an invalid type in annotation', async () => {
        const invalidMessage = {
            id: 'msg_123',
            assistant_id: null,
            attachments: null,
            completed_at: null,
            content: [
                {
                    text: {
                        annotations: [
                            {
                                end_index: 10,
                                file_citation: {
                                    file_id: 'file_123',
                                    quote: 'example quote',
                                },
                                start_index: 0,
                                text: 'example text',
                                type: 'invalid_type', // Invalid type
                            },
                        ],
                        value: 'This is an example message.',
                    },
                    type: 'text',
                },
            ],
            created_at: 1625077335,
            incomplete_at: null,
            incomplete_details: null,
            metadata: null,
            object: 'thread.message',
            role: 'user',
            run_id: null,
            status: 'completed',
            thread_id: 'thread_123',
        };

        await expect(messageSchema.validate(invalidMessage)).rejects.toThrow(ValidationError);
    });

    it('should invalidate a message with missing required fields', async () => {
        const invalidMessage = {
            assistant_id: null,
            attachments: null,
            completed_at: null,
            content: [
                {
                    text: {
                        annotations: [
                            {
                                end_index: 10,
                                file_citation: {
                                    file_id: 'file_123',
                                    quote: 'example quote',
                                },
                                start_index: 0,
                                text: 'example text',
                                type: 'file_citation',
                            },
                        ],
                        value: 'This is an example message.',
                    },
                    type: 'text',
                },
            ],
            created_at: 1625077335,
            incomplete_at: null,
            incomplete_details: null,
            metadata: null,
            object: 'thread.message',
            role: 'user',
            run_id: null,
            status: 'completed',
            thread_id: 'thread_123',
        };

        // Missing 'id' field
        await expect(messageSchema.validate(invalidMessage)).rejects.toThrow(ValidationError);
    });
});