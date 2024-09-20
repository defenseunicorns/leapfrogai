import { vi } from 'vitest';
import { fireEvent, render, screen } from '@testing-library/svelte';
import LFCarousel from './LFCarousel.svelte';

describe('LFCarousel', () => {
  beforeEach(() => {
    // Mock the ResizeObserver since it's a browser API that isn't available in tests
    vi.stubGlobal(
      'ResizeObserver',
      class {
        observe() {}
        disconnect() {}
      }
    );
  });

  it('renders correctly with default props', () => {
    const { container } = render(LFCarousel);

    expect(container).toBeTruthy();
    // Next and Previous have sr-only tailwind class for this text
    expect(screen.getByText('Previous')).toBeInTheDocument();
    expect(screen.getByText('Next')).toBeInTheDocument();
  });

  it('hides buttons when the content is not overflowing with a scrollbar', async () => {
    render(LFCarousel);

    const scrollContainer = screen.getByTestId('scroll-container') as HTMLDivElement;

    // Set width so that there is no overflow
    Object.defineProperty(scrollContainer, 'scrollWidth', { value: 500, configurable: true });
    Object.defineProperty(scrollContainer, 'clientWidth', { value: 500, configurable: true });

    // Trigger checkOverflow and verify buttons are hidden
    await fireEvent.scroll(scrollContainer);

    const previousButton = screen.getByText('Previous').parentElement?.parentElement; // Navigate up to the button element
    const nextButton = screen.getByText('Next').parentElement?.parentElement; // Navigate up to the button element

    // Check that the buttons are visually hidden
    expect(previousButton?.classList.contains('hidden')).toBe(true);
    expect(nextButton?.classList.contains('hidden')).toBe(true);
  });

  it('shows buttons when overflow is detected', async () => {
    render(LFCarousel);

    const scrollContainer = screen.getByTestId('scroll-container') as HTMLDivElement;
    // force overflow
    Object.defineProperty(scrollContainer, 'scrollWidth', { value: 1000, configurable: true });
    Object.defineProperty(scrollContainer, 'clientWidth', { value: 500, configurable: true });

    // Trigger checkOverflow and verify buttons are shown
    await fireEvent.scroll(scrollContainer);

    const previousButton = screen.getByText('Previous').parentElement?.parentElement; // Navigate up to the button element
    const nextButton = screen.getByText('Next').parentElement?.parentElement; // Navigate up to the button element

    expect(previousButton?.classList).not.toContain('hidden');
    expect(nextButton?.classList).not.toContain('hidden');
  });

  it('calls scrollLeft when the Previous button is clicked', async () => {
    const scrollAmount = 100;
    const { getByText } = render(LFCarousel, { scrollAmount });

    const scrollContainer = screen.getByTestId('scroll-container') as HTMLDivElement;

    // Mock the scrollBy method since JSDOM does not implement it
    const scrollBySpy = vi.fn();
    scrollContainer.scrollBy = scrollBySpy;

    await fireEvent.click(getByText('Previous'));

    expect(scrollBySpy).toHaveBeenCalledWith({ left: scrollAmount * -1, behavior: 'smooth' });
  });

  it('calls scrollRight when the Next button is clicked', async () => {
    const scrollAmount = 100;
    const { getByText } = render(LFCarousel, { scrollAmount });

    const scrollContainer = screen.getByTestId('scroll-container') as HTMLDivElement;

    // Mock the scrollBy method since JSDOM does not implement it
    const scrollBySpy = vi.fn();
    scrollContainer.scrollBy = scrollBySpy;

    await fireEvent.click(getByText('Next'));

    expect(scrollBySpy).toHaveBeenCalledWith({ left: scrollAmount, behavior: 'smooth' });
  });

  it('removes event listeners on component destroy', async () => {
    const { unmount } = render(LFCarousel);
    const scrollContainer = screen.getByTestId('scroll-container') as HTMLDivElement;

    const removeEventListenerSpy = vi.spyOn(scrollContainer, 'removeEventListener');

    unmount(); // Simulate the component being destroyed

    expect(removeEventListenerSpy).toHaveBeenCalledWith('scroll', expect.any(Function));
  });
});
