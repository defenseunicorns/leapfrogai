import { error } from '@sveltejs/kit';

/*
 * A generic error handler to log and structure error responses
 * Try/catch catch blocks can pass their error to this function
 * ex.
 * catch (e) {
    handleError(e, { id: file.id });
   }
 */
export const handleError = (e: unknown, additionalErrorInfo?: object) => {
  console.error('Caught Error:', e);

  let status = 500;
  let message = 'Internal Server Error';

  if (e instanceof Error) {
    message = e.message;
  } else if (typeof e === 'object' && e !== null && 'status' in e) {
    status = (e as { status: number }).status || 500;
    message =
      (e as unknown as { body: { message: string } }).body.message || 'Internal Server Error';
  }
  error(status, { message, ...additionalErrorInfo });
};

// In the test environment, formData.get('file') does not return a file of type File, so we mock it differently
// with this helper
export const requestWithFormData = (mockFile: unknown) => {
  return {
    formData: vi.fn().mockResolvedValue({
      get: vi.fn().mockReturnValue(mockFile)
    })
  } as unknown as Request;
};
