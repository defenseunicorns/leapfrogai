import { openai } from '$lib/server/constants';
import { AssistantResponse } from 'ai';

export async function POST(req: Request) {
  // TODO - validate
  // Parse the request body
  const input: {
    threadId: string;
    message: string;
    assistantId: string;
  } = await req.json();
  // Add a message to the thread
  const createdMessage = await openai.beta.threads.messages.create(input.threadId, {
    role: 'user',
    content: input.message
  });

  return AssistantResponse(
    { threadId: input.threadId, messageId: createdMessage.id },
    async ({ forwardStream, sendDataMessage }) => {
      // Run the assistant on the thread
      const runStream = openai.beta.threads.runs.stream(input.threadId, {
        assistant_id: input.assistantId
      });

      // forward run status would stream message deltas
      let runResult = await forwardStream(runStream);

      // status can be: queued, in_progress, requires_action, cancelling, cancelled, failed, completed, or expired
      while (
        runResult?.status === 'requires_action' &&
        runResult.required_action?.type === 'submit_tool_outputs'
      ) {
        const tool_outputs = runResult.required_action.submit_tool_outputs.tool_calls.map(
          (toolCall: any) => {
            const parameters = JSON.parse(toolCall.function.arguments);

            switch (toolCall.function.name) {
              // configure your tool calls here

              default:
                throw new Error(`Unknown tool call function: ${toolCall.function.name}`);
            }
          }
        );

        runResult = await forwardStream(
          openai.beta.threads.runs.submitToolOutputsStream(input.threadId, runResult.id, {
            tool_outputs
          })
        );
      }
    }
  );
}
