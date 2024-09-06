import { FILE_TYPE_MAP } from '$constants';

export const getFileType = (type: keyof typeof FILE_TYPE_MAP) => {
  return FILE_TYPE_MAP[type];
};
