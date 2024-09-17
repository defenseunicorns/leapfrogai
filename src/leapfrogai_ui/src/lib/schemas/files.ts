import { array, mixed, object, string, ValidationError } from 'yup';
import {
  ACCEPTED_AUDIO_FILE_MIME_TYPES,
  ACCEPTED_MIME_TYPES,
  AUDIO_FILE_SIZE_ERROR_TEXT,
  FILE_SIZE_ERROR_TEXT,
  INVALID_AUDIO_FILE_TYPE_ERROR_TEXT,
  INVALID_FILE_TYPE_ERROR_TEXT,
  MAX_AUDIO_FILE_SIZE,
  MAX_FILE_SIZE
} from '$constants';
import type { LFFile } from '$lib/types/files';

export const filesSchema = object({
  files: array().of(
    mixed<LFFile>()
      .test('fileType', 'Please upload a file.', (value) => value == null || value instanceof File)
      .test('fileSize', FILE_SIZE_ERROR_TEXT, (value) => {
        if (value == null) {
          return true;
        }
        // TODO - test that this error msg is used and not the one above
        if (ACCEPTED_AUDIO_FILE_MIME_TYPES.includes(value.type)) {
          if (value.size > MAX_AUDIO_FILE_SIZE) {
            return new ValidationError(AUDIO_FILE_SIZE_ERROR_TEXT);
          }
        } else if (value.size > MAX_FILE_SIZE) {
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
  file: mixed<LFFile>()
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

export const audioFileSchema = object({
  file: mixed<LFFile>()
    .test('fileType', 'File is required.', (value) => value == null || value instanceof File)
    .test('fileSize', AUDIO_FILE_SIZE_ERROR_TEXT, (value) => {
      if (value == null) {
        return true;
      }
      if (value.size > MAX_AUDIO_FILE_SIZE) {
        return new ValidationError(AUDIO_FILE_SIZE_ERROR_TEXT);
      }
      return true;
    })
    .test('type', INVALID_AUDIO_FILE_TYPE_ERROR_TEXT, (value) => {
      if (value == null) {
        return true;
      }
      if (!ACCEPTED_AUDIO_FILE_MIME_TYPES.includes(value.type)) {
        return new ValidationError(INVALID_AUDIO_FILE_TYPE_ERROR_TEXT);
      }
      return true;
    })
})
  .noUnknown(true)
  .strict();
