import { faker } from '@faker-js/faker';
import type { FileMetadata } from '$lib/types/files';
import { removeFilesUntilUnderLimit, updateFileMetadata } from '$helpers/fileHelpers';
import { FILE_CONTEXT_TOO_LARGE_ERROR_MSG } from '$constants/errors';
import { getMockFileMetadata } from '$testUtils/fakeData';

describe('removeFilesUntilUnderLimit', () => {
  test('removeFilesUntilUnderLimit should remove the largest file until total size is under the max limit', () => {
    // Metadata stringified without text is 95 characters, so the text added below will increase the size from that
    // baseline
    const text1 = faker.word.words(50);
    const text2 = faker.word.words(150);
    const text3 = faker.word.words(200);
    const files = [
      getMockFileMetadata({ text: text1 }),
      getMockFileMetadata({ text: text2 }),
      getMockFileMetadata({ text: text3 })
    ];

    // Files 2 and 3 will have different length once their text is removed and they are set to error status
    const file2WhenError = JSON.stringify({
      ...files[1],
      text: '',
      status: 'error',
      errorText: FILE_CONTEXT_TOO_LARGE_ERROR_MSG
    });
    const file3WhenError = JSON.stringify({
      ...files[2],
      text: '',
      status: 'error',
      errorText: FILE_CONTEXT_TOO_LARGE_ERROR_MSG
    });

    const totalSize = files.reduce((total, file) => total + JSON.stringify(file).length, 0);

    // Expected length when it removes the text of the last two files, but replaces them with error status
    const maxLimit =
      totalSize -
      JSON.stringify(files[1]).length -
      JSON.stringify(files[2]).length +
      file2WhenError.length +
      file3WhenError.length;

    removeFilesUntilUnderLimit(files, maxLimit);

    // file 1 remains
    expect(files[0].text).toBe(text1);

    // file 2 and 3 are removed and set to error status
    expect(files[1].text).toBe('');
    expect(files[1].status).toBe('error');
    expect(files[1].errorText).toBe(FILE_CONTEXT_TOO_LARGE_ERROR_MSG);
    expect(files[2].text).toBe('');
    expect(files[2].status).toBe('error');
    expect(files[2].errorText).toBe(FILE_CONTEXT_TOO_LARGE_ERROR_MSG);

    // Also check that the total size is under the limit
    const totalSizeRecalculated = files.reduce(
      (total, file) => total + JSON.stringify(file).length,
      0
    );

    expect(totalSizeRecalculated).toBeLessThanOrEqual(maxLimit);
  });

  it('should not modify files if total size is already under the max limit', () => {
    const text1 = faker.word.words(10);
    const text2 = faker.word.words(20);

    const files = [getMockFileMetadata({ text: text1 }), getMockFileMetadata({ text: text2 })];

    // Assume a limit of 50 characters
    const maxLimit = 10000000000000;

    // Call the function to test
    removeFilesUntilUnderLimit(files, maxLimit);

    // Expect no modifications to the files
    expect(files[0].text).toBe(text1);
    expect(files[1].text).toBe(text2);
  });

  it('can remove all files text and avoiding hanging (breaks out of while loop)', () => {
    const text1 = faker.word.words(10);
    const text2 = faker.word.words(20);

    const files = [getMockFileMetadata({ text: text1 }), getMockFileMetadata({ text: text2 })];

    // Assume a limit of 50 characters
    const maxLimit = 5;

    // Call the function to test
    removeFilesUntilUnderLimit(files, maxLimit);

    // Expect no modifications to the files
    expect(files[0].text).toBe('');
    expect(files[1].text).toBe('');
    expect(files[0].status).toBe('error');
    expect(files[1].status).toBe('error');
  });
});

describe('updateFileMetadata with order preservation', () => {
  it('should update existing files, add new files, and preserve the original order of old metadata', () => {
    const file1 = getMockFileMetadata({ status: 'complete' });
    const file2 = getMockFileMetadata({ status: 'uploading' });
    const file3 = getMockFileMetadata({ status: 'complete' });
    const file4 = getMockFileMetadata({ status: 'complete' });

    // 3 files
    const oldMetadata: FileMetadata[] = [file1, file2, file3];

    // updated file, and new file
    const newMetadata: FileMetadata[] = [file1, { ...file2, status: 'complete' }, file3, file4];

    const result = updateFileMetadata(oldMetadata, newMetadata);

    expect(result).toHaveLength(4);

    // Check if the order is preserved and one file was updated and new one added

    expect(result[0]).toEqual(file1);
    expect(result[1]).toEqual({
      ...file2,
      status: 'complete'
    });

    expect(result[2]).toEqual(file3);
    expect(result[3]).toEqual(file4);
  });

  it('should return new metadata if old metadata is empty', () => {
    const oldMetadata: FileMetadata[] = [];
    const newMetadata: FileMetadata[] = [getMockFileMetadata()];
    const result = updateFileMetadata(oldMetadata, newMetadata);
    expect(result).toHaveLength(1);
    expect(result).toEqual(newMetadata);
  });

  it('should keep old metadata if no new metadata is provided', () => {
    const oldMetadata: FileMetadata[] = [getMockFileMetadata()];
    const newMetadata: FileMetadata[] = [];
    const result = updateFileMetadata(oldMetadata, newMetadata);
    expect(result).toEqual(oldMetadata);
  });
});
