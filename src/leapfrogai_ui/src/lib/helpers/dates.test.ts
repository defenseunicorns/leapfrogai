import { dates } from '$helpers';
import { getFakeConversation } from '../../testUtils/fakeData';

describe('date helpers', () => {
	describe('isToday', () => {
		it('returns true when two dates are the same day', () => {
			const date1 = new Date('2022-01-01');
			const date2 = new Date('2022-01-01');
			expect(dates.isToday(date1, date2)).toBe(true);
		});

		it('returns false when two dates are different days', () => {
			const date1 = new Date('2022-01-01');
			const date2 = new Date('2022-01-02');
			expect(dates.isToday(date1, date2)).toBe(false);
		});

		it('returns false when two dates are different months', () => {
			const date1 = new Date('2022-01-01');
			const date2 = new Date('2022-02-01');
			expect(dates.isToday(date1, date2)).toBe(false);
		});

		it('returns false when two dates are different years', () => {
			const date1 = new Date('2022-01-01');
			const date2 = new Date('2023-01-01');
			expect(dates.isToday(date1, date2)).toBe(false);
		});
	});

	describe('getNumMonthsAgo', () => {
		it('returns the correct number of months ago', () => {
			const currentDate = new Date();
			const pastDate = new Date(currentDate.getFullYear() - 1, currentDate.getMonth() - 3);
			const expectedMonthsAgo = 15;

			expect(dates.getNumMonthsAgo(pastDate)).toBe(expectedMonthsAgo);
		});

		it('returns 0 when the past date is the same as the current date', () => {
			const currentDate = new Date();
			const pastDate = new Date(currentDate);
			const expectedMonthsAgo = 0;

			expect(dates.getNumMonthsAgo(pastDate)).toBe(expectedMonthsAgo);
		});

		it('returns a negative number when the past date is in the future', () => {
			const currentDate = new Date();
			const futureDate = new Date(currentDate.getFullYear() + 1, currentDate.getMonth() + 3);
			const expectedMonthsAgo = -15;

			expect(dates.getNumMonthsAgo(futureDate)).toBe(expectedMonthsAgo);
		});
	});

	describe('getDateCategory', () => {
		it('returns "Old" when the date is more than the default set for numMonthsAgo', () => {
			const currentDate = new Date();
			const pastDate = new Date(currentDate.getFullYear(), currentDate.getMonth() - 5);
			const expectedCategory = 'Old';

			expect(dates.getDateCategory(pastDate)).toBe(expectedCategory);
		});

		it('returns "Today" when the date is the same as the current date', () => {
			const currentDate = new Date();
			const expectedCategory = 'Today';

			expect(dates.getDateCategory(currentDate)).toBe(expectedCategory);
		});

		it('returns "Yesterday" when the date is one day before the current date', () => {
			const currentDate = new Date();
			const yesterday = new Date(
				currentDate.getFullYear(),
				currentDate.getMonth(),
				currentDate.getDate() - 1
			);
			const expectedCategory = 'Yesterday';

			expect(dates.getDateCategory(yesterday)).toBe(expectedCategory);
		});

		it('returns "This Month" when the date is in the same month as the current date', () => {
			const currentDate = new Date();
			const sameMonthDate = new Date(currentDate.getFullYear(), currentDate.getMonth(), 10);
			const expectedCategory = 'This Month';

			expect(dates.getDateCategory(sameMonthDate)).toBe(expectedCategory);
		});

		it('returns the formatted month and year when the date is in a different year', () => {
			// Date to compare against needs to be within numMonthsToDisplay months but still
			// within previous year in order to see the monthname - year
			// we are setting the numMonthsToDisplay to 1200 to make sure it does not put the month in 'Old' category

			// The system timezone here is behind UTC so you need to specify T00:00 to make sure it reflects the local
			// day properly and doesn't show October when it should be November 1
			const date = new Date('2023-11-01T00:00');
			const expectedCategory = 'November - 2023';

			expect(dates.getDateCategory(date, 1200)).toBe(expectedCategory);
		});

		it('returns the formatted month when the date is in the current year', () => {
			// We can't use actual today because if this test is run in January, the previous month
			// will get the year with its category (e.g December - 2023) and the test will fail
			const todayOverride = new Date('2024-03-01T00:00');
			const date = new Date('2024-02-01T00:00');
			const expectedCategory = 'February';

			expect(dates.getDateCategory(date, 4, todayOverride)).toBe(expectedCategory);
		});
	});

	describe('organizeConversationsByDate', () => {
		const todayOverride = new Date('2024-03-20T00:00');

		it('organizes conversations by date category', () => {
			const conversations = [
				// today
				getFakeConversation({ insertedAt: todayOverride.toDateString() }),
				// Yesterday
				getFakeConversation({
					insertedAt: new Date(
						todayOverride.getFullYear(),
						todayOverride.getMonth(),
						todayOverride.getDate() - 1
					).toDateString()
				}),
				getFakeConversation({
					insertedAt: new Date(
						todayOverride.getFullYear(),
						todayOverride.getMonth(),
						todayOverride.getDate() - 1
					).toDateString()
				}),
				// This Month
				getFakeConversation({
					insertedAt: new Date(
						todayOverride.getFullYear(),
						todayOverride.getMonth(),
						10
					).toDateString()
				}),
				// February
				getFakeConversation({
					insertedAt: new Date(new Date('2024-02-01T00:00')).toDateString()
				}),
				// December - 2023
				getFakeConversation({
					insertedAt: new Date(new Date('2023-12-01T00:00')).toDateString()
				}),
				// Old
				getFakeConversation({
					insertedAt: new Date(
						todayOverride.getFullYear(),
						todayOverride.getMonth() - 5
					).toDateString()
				})
			];
			console.log(conversations.map((c) => c.inserted_at));

			const expectedOrganizedConversations = {
				Today: [conversations[0]],
				Yesterday: [conversations[1], conversations[2]],
				'This Month': [conversations[3]],
				February: [conversations[4]],
				'December - 2023': [conversations[5]],
				Old: [conversations[6]]
			};

			const result = dates.organizeConversationsByDate(conversations, todayOverride);
			expect(result).toEqual(expectedOrganizedConversations);
		});
	});
});
