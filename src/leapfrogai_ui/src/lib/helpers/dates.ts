import type { LFThread } from '$lib/types/threads';

const NUM_MONTHS_TO_DISPLAY = 6;
export const monthNames = [
  'January',
  'February',
  'March',
  'April',
  'May',
  'June',
  'July',
  'August',
  'September',
  'October',
  'November',
  'December'
];

/**
 * Calculates the number of months between a past date and the current date.
 * @param pastDate The past date to compare against the current date.
 * @param today  The current date. Defaults to the current date. Can be overridden for testing purposes.
 * @returns The number of months between the past date and the current date.
 */
export const getNumMonthsAgo = (pastDate: Date, today = new Date()) => {
  const currentYear = today.getFullYear();
  const currentMonth = today.getMonth();

  const pastYear = pastDate.getFullYear();
  const pastMonth = pastDate.getMonth();

  const yearDiff = currentYear - pastYear;
  const monthDiff = currentMonth - pastMonth;

  return yearDiff * 12 + monthDiff;
};

/**
 * Checks if two dates are the same day.
 * @param d1 - The first date.
 * @param d2 - The second date.
 * @returns True if the dates are the same day, false otherwise.
 */
export const isToday = (d1: Date, d2: Date) => {
  return (
    d1.getDate() === d2.getDate() &&
    d1.getMonth() === d2.getMonth() &&
    d1.getFullYear() === d2.getFullYear()
  );
};

/**
 * Checks if the first date is exactly one day before the second date.
 *
 * @param {Date} firstDate - The first date to be compared.
 * @param {Date} secondDate - The second date to be compared.
 * @returns {boolean} - Returns true if the first date is exactly one day before the second date, false otherwise.
 */
function isOneDayBefore(firstDate: Date, secondDate: Date): boolean {
  // Set both dates to midnight to ensure we're only comparing the dates, not the times
  const first = new Date(firstDate.getFullYear(), firstDate.getMonth(), firstDate.getDate());
  const second = new Date(secondDate.getFullYear(), secondDate.getMonth(), secondDate.getDate());

  // Calculate the difference in milliseconds between the two dates
  const diff = second.getTime() - first.getTime();

  // Check if the difference is exactly 24 hours
  return diff === 24 * 60 * 60 * 1000;
}

/**
 * Generates an array of date categories based on the current date and a specified number of months to display.
 *
 * @param {Object} [params] - An optional parameters object.
 * @param {Date} [params.today=new Date()] - The current date. Defaults to the current date. Can override for testing purposes.
 * @param {number} [params.numMonthsToDisplay=NUM_MONTHS_TO_DISPLAY] - The number of months to display before putting in the 'Old' category.
 * @returns {string[]} - An array of date categories.
 *
 * This function generates an array of date categories, which includes 'Today', 'Yesterday', 'This Month',
 * the past NUM_MONTHS_TO_DISPLAY months by name, and 'Old'.
 */

type GetDateCategoriesParams = {
  today?: Date;
  numMonthsToDisplay?: number;
};
export const getDateCategories = ({
  today = new Date(),
  numMonthsToDisplay = NUM_MONTHS_TO_DISPLAY
}: GetDateCategoriesParams = {}): string[] => {
  const currentMonth = today.getMonth();

  const months = [];
  for (let i = 1; i <= numMonthsToDisplay; i++) {
    // Subtract one month at a time and wrap around using modulo operator
    const monthIndex = (currentMonth - i + 12) % 12;
    months.push(monthNames[monthIndex]);
  }

  return ['Today', 'Yesterday', 'This Month', ...months, 'Old'];
};

/**
 * Determines the date category for a given date.
 *
 * @param {Object} params - An object containing the parameters for the function.
 * @param {Date} params.date - The date to categorize.
 * @param {number} [params.numMonthsToDisplay=NUM_MONTHS_TO_DISPLAY] - The number of months to display before categorizing as 'Old'.
 * @param {Date} [params.today=new Date()] - The current date. Defaults to the current date. Can be overridden for testing purposes.
 * @returns {string} - The date category for the given date.
 *
 * This function checks the given date against a set of predefined categories:
 * 'Today', 'Yesterday', 'This Month', the past NUM_MONTHS_TO_DISPLAY months by name, and 'Old'.
 * It returns the category that the date falls into.
 * If the date is more than NUM_MONTHS_TO_DISPLAY months in the past, it returns 'Old'.
 */

type GetDateCategoryParams = {
  date: Date;
  numMonthsToDisplay?: number;
  today?: Date;
};
export const getDateCategory = ({
  date,
  numMonthsToDisplay = NUM_MONTHS_TO_DISPLAY,
  today = new Date()
}: GetDateCategoryParams): string => {
  const dateCategories = getDateCategories({ today, numMonthsToDisplay });
  const dateToCheck = new Date(date);
  const yearsDiff = Math.abs(dateToCheck.getFullYear() - today.getFullYear());
  const monthsDiff = getNumMonthsAgo(dateToCheck, today);

  if (monthsDiff > numMonthsToDisplay) return 'Old';

  if (isToday(dateToCheck, today)) {
    return 'Today';
  }

  if (isOneDayBefore(dateToCheck, today)) {
    return 'Yesterday';
  }

  if (yearsDiff === 0 && dateToCheck.getMonth() === today.getMonth()) {
    return 'This Month';
  }

  const month = monthNames[dateToCheck.getMonth()];
  if (monthsDiff <= numMonthsToDisplay && dateCategories.includes(month)) return month;
  else return 'Old';
};

/**
 * Organizes an array of threads by date category and sorts the 'Old' category by date.
 *
 * @param {LFThread[]} threads - The array of threads to be organized.
 * @param {Date} [today=new Date()] - The current date. Defaults to the current date. Can override for testing purposes.
 * @param {number} [numMonthsToDisplay=NUM_MONTHS_TO_DISPLAY] - The number of months to display before putting in the 'Old' category. * @returns An object with date categories as keys and arrays of threads as values.
 *
 * This function first gets the date categories and initializes the result object.
 * Then, for each thread, it finds its date category and adds it to the corresponding array in the result.
 * Finally, it sorts the threads in the 'Old' category by date.
 */
export const organizeThreadsByDate = (
  threads: LFThread[],
  today: Date = new Date(),
  numMonthsToDisplay: number = NUM_MONTHS_TO_DISPLAY
) => {
  const dateCategories = getDateCategories({ today, numMonthsToDisplay });

  const result: { label: string; threads: LFThread[] }[] = [];

  // Initialize result object with empty arrays for each date category and the proper labels
  for (const category of dateCategories) {
    result.push({ label: category, threads: [] });
  }

  // Add threads to the corresponding date category
  for (const thread of threads) {
    const dateCategory = getDateCategory({
      date: new Date(thread.created_at * 1000),
      numMonthsToDisplay,
      today
    });
    const index = dateCategories.indexOf(dateCategory);

    result[index].threads.push(thread);
  }

  // Sort each category by date
  for (const category of dateCategories) {
    const categoryIndex = dateCategories.indexOf(category);
    result[categoryIndex].threads = result[categoryIndex].threads.sort(
      (a, b) => new Date(b.created_at * 1000).getTime() - new Date(a.created_at * 1000).getTime()
    );
  }
  return result;
};

export const getUnixSeconds = (date: Date) => date.getTime() / 1000;
