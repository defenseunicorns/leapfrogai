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
      const NUM_MONTHS_TO_DISPLAY = 6;
      const currentDate = new Date();
      const pastDate = new Date(
        currentDate.getFullYear(),
        currentDate.getMonth() - NUM_MONTHS_TO_DISPLAY - 1
      );
      const expectedCategory = 'Old';

      expect(
        dates.getDateCategory({ date: pastDate, numMonthsToDisplay: NUM_MONTHS_TO_DISPLAY })
      ).toBe(expectedCategory);
    });

    it('returns "Today" when the date is the same as the current date', () => {
      const currentDate = new Date();
      const expectedCategory = 'Today';

      expect(dates.getDateCategory({ date: currentDate })).toBe(expectedCategory);
    });

    it('returns "Yesterday" when the date is one day before the current date', () => {
      const currentDate = new Date();
      const yesterday = new Date(
        currentDate.getFullYear(),
        currentDate.getMonth(),
        currentDate.getDate() - 1
      );
      const expectedCategory = 'Yesterday';

      expect(dates.getDateCategory({ date: yesterday })).toBe(expectedCategory);
    });

    it('returns "This Month" when the date is in the same month as the current date', () => {
      const today = new Date();
      const sameMonthDate = new Date(today.getFullYear(), today.getMonth(), 20);
      const expectedCategory = 'This Month';

      expect(dates.getDateCategory({ date: sameMonthDate })).toBe(expectedCategory);
    });
  });

  describe('organizeConversationsByDate', () => {
    // Overriding to test with months that overlap years
    const todayOverride = new Date('2024-03-20T00:00');

    it('organizes conversations by date category', () => {
      const numMonthsToDisplay = 6;
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
            todayOverride.getFullYear() - 2,
            todayOverride.getMonth()
          ).toDateString()
        }),
        getFakeConversation({
          insertedAt: new Date(
            todayOverride.getFullYear(),
            todayOverride.getMonth() - numMonthsToDisplay - 1
          ).toDateString()
        })
      ];

      const expectedOrganizedConversations = [
        { label: 'Today', conversations: [conversations[0]] },
        { label: 'Yesterday', conversations: [conversations[1], conversations[2]] },
        { label: 'This Month', conversations: [conversations[3]] },
        { label: 'February', conversations: [conversations[4]] },
        { label: 'January', conversations: [] },
        { label: 'December', conversations: [conversations[5]] },
        { label: 'November', conversations: [] },
        { label: 'October', conversations: [] },
        { label: 'September', conversations: [] },
        { label: 'Old', conversations: [conversations[7], conversations[6]] } // tests ordering of old dates too
      ];
      const result = dates.organizeConversationsByDate(
        conversations,
        todayOverride,
        numMonthsToDisplay
      );
      expect(result).toEqual(expectedOrganizedConversations);
    });
  });
});
