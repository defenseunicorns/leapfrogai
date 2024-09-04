import { array, mixed, object, string, ValidationError } from 'yup';
import {
  ACCEPTED_MIME_TYPES,
  FILE_SIZE_ERROR_TEXT,
  INVALID_FILE_TYPE_ERROR_TEXT,
  MAX_FILE_SIZE
} from '$constants';

export const filesSchema = object({
  files: array().of(
    mixed<File>()
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
      .test('type', INVALID_FILE_TYPE_ERROR_TEXT, (value) => {
        if (value == null) {
          return true;
        }
        if (!ACCEPTED_MIME_TYPES.includes(value.type)) {
          return new ValidationError(INVALID_FILE_TYPE_ERROR_TEXT);
        }
        return true;
      })
  )
})
  .noUnknown(true)
  .strict();

export const filesCheckSchema = object({
  fileIds: array().of(string())
})
  .noUnknown(true)
  .strict();

export const fileSchema = object({
  file: mixed<File>()
    .test('fileType', 'File is required.', (value) => value == null || value instanceof File)
    .test('fileSize', FILE_SIZE_ERROR_TEXT, (value) => {
      if (value == null) {
        return true;
      }
      if (value.size > MAX_FILE_SIZE) {
        return new ValidationError(FILE_SIZE_ERROR_TEXT);
      }
      return true;
    })
    .test('type', INVALID_FILE_TYPE_ERROR_TEXT, (value) => {
      if (value == null) {
        return true;
      }
      if (!ACCEPTED_MIME_TYPES.includes(value.type)) {
        return new ValidationError(INVALID_FILE_TYPE_ERROR_TEXT);
      }
      return true;
    })
})
  .noUnknown(true)
  .strict();
