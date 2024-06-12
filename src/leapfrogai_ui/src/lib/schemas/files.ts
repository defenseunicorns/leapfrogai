import { array, mixed, object, ValidationError } from 'yup';
import { FILE_SIZE_ERROR_TEXT, MAX_FILE_SIZE } from '$constants';

export const filesSchema = object({
  files: array().of(
    mixed<File>()
      .nullable()
      .test('fileType', 'Please upload a file.', (value) => value == null || value instanceof File)
      .test('fileSize', FILE_SIZE_ERROR_TEXT, (value) => {
        if (value == null) {
          return true;
        }
        if (value.size > MAX_FILE_SIZE) {
          return new ValidationError(FILE_SIZE_ERROR_TEXT);
        }
        return true;
      })
      .test('type', 'Invalid file type, accepted types are: pdf and txt', (value) => {
        if (value == null) {
          return true;
        }
        if (value.type !== 'application/pdf' && value.type !== 'application/txt') {
          return new ValidationError('Invalid file type, accepted types are: pdf and txt');
        }
        return true;
      })
  )
});
