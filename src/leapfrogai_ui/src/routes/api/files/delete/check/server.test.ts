import { POST } from './+server';
import { mockOpenAI } from '../../../../../../vitest-setup';
import {
  getFakeAssistant,
  getFakeFiles,
  getFakeVectorStore,
  getFakeVectorStoreFile
} from '$testUtils/fakeData';
import type { RequestEvent } from '@sveltejs/kit';
import type { RouteParams } from './$types';
import { getLocalsMock } from '$lib/mocks/misc';

const validMessageBody = { fileIds: ['file1', 'file2'] };
describe('/api/files/delete/check', () => {
  it('returns a 401 when there is no session', async () => {
    const request = new Request('http://thisurlhasnoeffect', {
      method: 'POST',
      body: JSON.stringify(validMessageBody)
    });

    await expect(
      POST({
        request,
        locals: getLocalsMock({ nullSession: true })
      } as RequestEvent<RouteParams, '/api/files/delete/check'>)
    ).rejects.toMatchObject({
      status: 401
    });
  });

  it('returns a 400 when the body is invalid', async () => {
    // Empty body
    let request = new Request('http://thisurlhasnoeffect', {
      method: 'POST'
    });

    // Body missing
    await expect(
      POST({
        request,
        locals: getLocalsMock()
      } as RequestEvent<RouteParams, '/api/files/delete/check'>)
    ).rejects.toMatchObject({
      status: 400
    });

    // Invalid param
    request = new Request('http://thisurlhasnoeffect', {
      method: 'POST',
      body: JSON.stringify({ id: '123' })
    });

    await expect(
      POST({
        request,
        locals: getLocalsMock()
      } as RequestEvent<RouteParams, '/api/files/delete/check'>)
    ).rejects.toMatchObject({
      status: 400
    });

    // Extra param
    request = new Request('http://thisurlhasnoeffect', {
      method: 'POST',
      body: JSON.stringify({ ...validMessageBody, break: 'me' })
    });

    await expect(
      POST({
        request,
        locals: getLocalsMock()
      } as RequestEvent<RouteParams, '/api/files/delete/check'>)
    ).rejects.toMatchObject({
      status: 400
    });

    // Invalid type
    request = new Request('http://thisurlhasnoeffect', {
      method: 'POST',
      body: JSON.stringify({ fileIds: 'notAnArray' })
    });

    await expect(
      POST({
        request,
        locals: getLocalsMock()
      } as RequestEvent<RouteParams, '/api/files/delete/check'>)
    ).rejects.toMatchObject({
      status: 400
    });
  });

  it('returns a list of assistants affected by this file deletion', async () => {
    /* ---- DATA SETUP ---- */
    const [file1, file2] = getFakeFiles();
    const [file3, file4] = getFakeFiles();
    const vectorStore1 = getFakeVectorStore();
    const vectorStore2 = getFakeVectorStore();
    const vectorStoreFile1 = getFakeVectorStoreFile({
      id: file1.id,
      vector_store_id: vectorStore1.id
    });
    const vectorStoreFile2 = getFakeVectorStoreFile({
      id: file2.id,
      vector_store_id: vectorStore1.id
    });
    const vectorStoreFile3 = getFakeVectorStoreFile({
      id: file3.id,
      vector_store_id: vectorStore2.id
    });
    const vectorStoreFile4 = getFakeVectorStoreFile({
      id: file4.id,
      vector_store_id: vectorStore2.id
    });

    // Assistant 1 has file1 and file2
    // Assistant 2 has file3 and file4
    const assistant1 = getFakeAssistant({ vectorStoreId: vectorStore1.id });
    const assistant2 = getFakeAssistant({ vectorStoreId: vectorStore2.id });
    mockOpenAI.setAssistants([assistant1, assistant2]);
    mockOpenAI.setVectorStores([vectorStore1, vectorStore2]);
    mockOpenAI.setVectorStoreFiles([
      vectorStoreFile1,
      vectorStoreFile2,
      vectorStoreFile3,
      vectorStoreFile4
    ]);

    /* ---- END DATA SETUP ---- */

    // Test deleting file 1 and expect only assistant1 to be affected
    const request = new Request('http://thisurlhasnoeffect', {
      method: 'POST',
      body: JSON.stringify({ fileIds: [file1.id] })
    });

    const res = await POST({
      request,
      locals: getLocalsMock()
    } as RequestEvent<RouteParams, '/api/files/delete/check'>);

    const resData = await res.json();
    expect(res.status).toEqual(200);

    expect(resData[0]).toEqual(assistant1);

    // Test deleting file 1 and file 3 and expect both assistant1 and assistant2 to be affected
    const request2 = new Request('http://thisurlhasnoeffect', {
      method: 'POST',
      body: JSON.stringify({ fileIds: [file1.id, file3.id] })
    });

    const res2 = await POST({
      request: request2,
      locals: getLocalsMock()
    } as RequestEvent<RouteParams, '/api/files/delete/check'>);

    const resData2 = await res2.json();
    expect(res2.status).toEqual(200);

    expect(resData2[0]).toEqual(assistant1);
    expect(resData2[1]).toEqual(assistant2);
  });

  it('returns a 500 when there is a openai error', async () => {
    mockOpenAI.setError('listAssistants');
    const request = new Request('http://thisurlhasnoeffect', {
      method: 'POST',
      body: JSON.stringify(validMessageBody)
    });

    await expect(
      POST({
        request,
        locals: getLocalsMock()
      } as RequestEvent<RouteParams, '/api/files/delete/check'>)
    ).rejects.toMatchObject({
      status: 500
    });
  });
});
