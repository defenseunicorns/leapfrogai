import { shortenFileName } from '$helpers/stringHelpers';

// Note - if MAX_FILE_NAME_SIZE changes, these fake names will have to be adjusted
describe('stringHelpers', () => {
  describe('shortenFileName', () => {
    it('should return the same name if it is MAX_FILE_NAME_SIZE characters or less', () => {
      const name = 'short-filename.txt';
      expect(shortenFileName(name)).toBe(name);
    });

    it('should shorten the filename and preserve the extension if longer than MAX_FILE_NAME_SIZE characters', () => {
      const name = 'this-is-a-very-long-filename.txt';
      const expected = 'this-is-a-very-long-....txt';
      expect(shortenFileName(name)).toBe(expected);
    });

    it('should handle filenames without extensions', () => {
      const name = 'this-is-a-very-long-filename-without-extension';
      const expected = 'this-is-a-very-long-file...';
      expect(shortenFileName(name)).toBe(expected);
    });

    it('should handle filenames with multiple dots', () => {
      const name = 'this.is.a.very.long.filename.with.dots.txt';
      const expected = 'this.is.a.very.long.....txt';
      expect(shortenFileName(name)).toBe(expected);
    });

    it('should handle filenames that are exactly MAX_FILE_NAME_SIZE characters', () => {
      const name = '12345678912345678912345.ext';
      expect(shortenFileName(name)).toBe(name);
    });

    it('should handle filenames with short extensions', () => {
      const name = 'this-is-a-very-long-filename.m';
      const expected = 'this-is-a-very-long-fi....m';
      expect(shortenFileName(name)).toBe(expected);
    });
  });
});
