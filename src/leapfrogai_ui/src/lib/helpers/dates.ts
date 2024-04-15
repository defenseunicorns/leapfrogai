const formatOptions: Intl.DateTimeFormatOptions = {
	month: 'long'
};

/**
 * Calculates the number of months between a past date and the current date.
 * @param pastDate The past date to compare against the current date.
 * @returns The number of months between the past date and the current date.
 */
export const getNumMonthsAgo = (pastDate: Date) => {
	const currentDate = new Date();
	const currentYear = currentDate.getFullYear();
	const currentMonth = currentDate.getMonth();

	const pastYear = pastDate.getFullYear();
	const pastMonth = pastDate.getMonth();

	const yearDiff = currentYear - pastYear;
	const monthDiff = currentMonth - pastMonth;

	return yearDiff * 12 + monthDiff;
};

/**
 * Returns the category of a given date based on its proximity to the current date.
 * Categories include 'Today', 'Yesterday', 'This Month', the 'month name' and/or 'month name - year', and 'Old'
 * @param {Date} date - The date to categorize.
 * @param {number} [numMonthsToDisplay=4] numMonthsToDisplay - How many months to go back before putting in 'Old' category
 * @param {Date} [today=new Date()] today - The current date. Defaults to the current date.
 * @returns The category of the date.
 */

// function formatDate(someDateTimeStamp) {
// 	var dt = new Date(someDateTimeStamp),
// 		date = dt.getDate(),
// 		month = months[dt.getMonth()],
// 		timeDiff = someDateTimeStamp - Date.now(),
// 		diffDays = new Date().getDate() - date,
// 		diffMonths = new Date().getMonth() - dt.getMonth(),
// 		diffYears = new Date().getFullYear() - dt.getFullYear();
//
// 	if(diffYears === 0 && diffDays === 0 && diffMonths === 0){
// 		return "Today";
// 	}else if(diffYears === 0 && diffDays === 1) {
// 		return "Yesterday";
// 	}else if(diffYears === 0 && diffDays === -1) {
// 		return "Tomorrow";
// 	}else if(diffYears === 0 && (diffDays < -1 && diffDays > -7)) {
// 		return fulldays[dt.getDay()];
// 	}else if(diffYears >= 1){
// 		return month + " " + date + ", " + new Date(someDateTimeStamp).getFullYear();
// 	}else {
// 		return month + " " + date;
// 	}
// }

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

export const getDateCategory = (date: Date, numMonthsToDisplay = 4, today = new Date()) => {
	// How many months to go back before putting in 'Old' category
	const dateToCheck = new Date(date);

	const yearsDiff = Math.abs(dateToCheck.getFullYear() - today.getFullYear());
	const monthsDiff = getNumMonthsAgo(dateToCheck);

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

	if (yearsDiff > 0) {
		if (monthsDiff <= numMonthsToDisplay) {
			// Ex. November - 2023
			return `${dateToCheck.toLocaleString('en-US', formatOptions)} - ${dateToCheck.getFullYear()}`;
		}
	} else return dateToCheck.toLocaleString('en-US', formatOptions);
};

/**
 * Organizes an array of conversations by date category.
 *
 * @param {Conversation[]} conversations - The array of conversations to be organized.
 * @param {Date} [today=new Date()] today - The current date. Defaults to the current date.
 * @returns An object containing conversations grouped by date category.
 */
export const organizeConversationsByDate = (conversations: Conversation[], today = new Date()) => {
	const result: { [category: string]: Conversation[] } = {};
	for (const conversation of conversations) {
		const dateCategory = getDateCategory(
			new Date(conversation.inserted_at),
			undefined,
			today
		) as keyof typeof result;
		!result[dateCategory]
			? (result[dateCategory] = [conversation])
			: result[dateCategory].push(conversation);
	}
	return result;
};

/**
 * Sorts an array of months in reverse order.
 * Months can be in the format "MonthName" or "MonthName - Year". If the year is omitted, the current year is assumed.
 * e.g. "March - 2023" or "January".
 *
 * @param {string[]} months - The array of months to be sorted. Each month string should follow the
 * format "MonthName - Year" or "MonthName", where "MonthName" is the full name of the month.
 * @returns {string[]} The sorted array of months in reverse chronological order.
 */
export const sortMonthsReverse = (months: string[]) => {
	const monthOrder = [
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

	return months.sort((a, b) => {
		const [monthA, yearA = new Date().getFullYear().toString()] = a.split(' - ');
		const [monthB, yearB = new Date().getFullYear().toString()] = b.split(' - ');

		const monthIndexA = monthOrder.indexOf(monthA);
		const monthIndexB = monthOrder.indexOf(monthB);

		const yearComparison = parseInt(yearB) - parseInt(yearA);

		if (yearComparison === 0) {
			return monthIndexB - monthIndexA;
		}

		return yearComparison;
	});
};
