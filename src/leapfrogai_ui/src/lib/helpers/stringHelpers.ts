import { MAX_FILE_NAME_SIZE } from '$constants';

export const shortenFileName = (name: string) => {
  if (name.length <= MAX_FILE_NAME_SIZE) return name;

  const parts = name.split('.');
  const extension = parts.length > 1 ? `.${parts.pop()}` : '';
  const baseName = parts.join('.');

  return `${baseName.substring(0, MAX_FILE_NAME_SIZE - 3 - extension.length)}...${extension}`;
};
