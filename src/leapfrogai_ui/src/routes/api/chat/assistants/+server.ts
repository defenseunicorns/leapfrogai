import { openai } from '$lib/server/constants';
import { AssistantResponse } from 'ai';

export async function POST({ request }) {
  // TODO - validate
  // Parse the request body
  const input: {
    message: string;
    data: {
      assistantId: string;
      threadId: string | null;
    };
  } = await request.json();

  const threadId = input.data.threadId ?? (await openai.beta.threads.create({ metadata: {} })).id;

  // Add a message to the thread
  const createdMessage = await openai.beta.threads.messages.create(threadId, {
    role: 'user',
    content: input.message
  });

  return AssistantResponse(
    {
      threadId: threadId,
      messageId: createdMessage.id
    },
    async ({ forwardStream }) => {
      // Run the assistant on the thread
      const runStream = openai.beta.threads.runs.stream(threadId, {
        assistant_id:
          input.data.assistantId ??
          (() => {
            throw new Error('assistant_id is not set');
          })()
      });

      // forward run status would stream message deltas
      let runResult = await forwardStream(runStream);

      // status can be: queued, in_progress, requires_action, cancelling, cancelled, failed, completed, or expired
      while (
        runResult?.status === 'requires_action' &&
        runResult.required_action?.type === 'submit_tool_outputs'
      ) {
        const tool_outputs = runResult.required_action.submit_tool_outputs.tool_calls.map(
          // This code comes from the docs, not going to modify the typing to fix the 'any' type here
          // eslint-disable-next-line @typescript-eslint/no-explicit-any
          (toolCall: any) => {
            // const parameters = JSON.parse(toolCall.function.arguments);

            switch (toolCall.function.name) {
              // configure your tool calls here

              default:
                throw new Error(`Unknown tool call function: ${toolCall.function.name}`);
            }
          }
        );

        runResult = await forwardStream(
          openai.beta.threads.runs.submitToolOutputsStream(threadId, runResult.id, {
            tool_outputs
          })
        );
      }
    }
  );
}
