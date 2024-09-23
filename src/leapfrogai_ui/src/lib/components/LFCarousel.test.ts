import { vi } from 'vitest';
import { fireEvent, render, screen } from '@testing-library/svelte';
import LFCarousel from './LFCarousel.svelte';
import LFCarouselWithSlot from './LFCarouselWithSlot.test.svelte';

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

  it('does not render buttons but just renders slot when hidden to set to true', () => {
    render(LFCarouselWithSlot, {
      props: { hidden: true }
    });

    expect(screen.queryByText('Previous')).not.toBeInTheDocument();
    expect(screen.queryByText('Next')).not.toBeInTheDocument();
    expect(screen.getByText('test content')).toBeInTheDocument();
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
    scrollContainer.scrollLeft = 100; // Simulate a right scroll, scrollBy does not exist in JSDOM
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

  it('hides buttons when the window is resized', async () => {
    render(LFCarousel);

    const scrollContainer = screen.getByTestId('scroll-container') as HTMLDivElement;

    // create an overflow condition
    Object.defineProperty(scrollContainer, 'scrollWidth', { value: 1000, configurable: true });
    Object.defineProperty(scrollContainer, 'clientWidth', { value: 500, configurable: true });

    // Trigger the checkOverflow to ensure buttons are initially visible
    await fireEvent.scroll(scrollContainer);
    let nextButton = screen.getByText('Next').parentElement?.parentElement;
    expect(nextButton?.classList.contains('hidden')).toBe(false);

    // Previous button will not show until it has been scrolled right
    let previousButton = screen.getByText('Previous').parentElement?.parentElement;
    expect(previousButton?.classList.contains('hidden')).toBe(true);
    scrollContainer.scrollLeft = 100; // Simulate a right scroll, scrollBy does not exist in JSDOM
    await fireEvent.scroll(scrollContainer);
    expect(previousButton?.classList.contains('hidden')).toBe(false);

    // remove overflow condition
    Object.defineProperty(scrollContainer, 'scrollWidth', { value: 500, configurable: true });
    Object.defineProperty(scrollContainer, 'clientWidth', { value: 500, configurable: true });
    scrollContainer.scrollLeft = 0;
    // Simulate window resize event
    await fireEvent(window, new Event('resize'));

    previousButton = screen.getByText('Previous').parentElement?.parentElement;
    nextButton = screen.getByText('Next').parentElement?.parentElement;

    // buttons are hidden after resize
    expect(previousButton?.classList.contains('hidden')).toBe(true);
    expect(nextButton?.classList.contains('hidden')).toBe(true);
  });
});
