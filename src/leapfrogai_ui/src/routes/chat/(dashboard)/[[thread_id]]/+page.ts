export const load = async ({ params, fetch }) => {
  const promises = [
    fetch(`/api/threads/${params.thread_id}`),
    fetch('/api/assistants'),
    fetch('/api/files')
  ];
  const [threadRes, assistantsRes, filesRes] = await Promise.all(promises);

  const thread = await threadRes.json();
  const assistants = await assistantsRes.json();
  const files = await filesRes.json();

  return { thread, assistants, files };
};
