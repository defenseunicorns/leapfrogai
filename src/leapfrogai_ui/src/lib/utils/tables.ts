import { formatDate } from '$helpers/dates';

export const filterTable = <T>(
  items: T[],
  filter_keys: Array<keyof T>,
  searchTerm: string
): T[] => {
  return items.filter((item) => {
    return filter_keys.some((filter) => {
      const value = item[filter];

      if (typeof value === 'string') {
        return value.toLowerCase().includes(searchTerm.toLowerCase());
      }
      if (typeof value === 'number') {
        // handles string date search term when date is stored as number
        const formattedDate = formatDate(new Date(value)).toLowerCase();

        return (
          value.toString().toLowerCase().includes(searchTerm) || formattedDate.includes(searchTerm)
        );
      }
      if (typeof value === 'object' && value !== null) {
        return JSON.stringify(value).includes(searchTerm);
      }
      return false;
    });
  });
};
