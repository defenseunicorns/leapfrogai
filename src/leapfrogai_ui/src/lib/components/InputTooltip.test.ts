import { render, screen } from '@testing-library/svelte';
import InputTooltip from '$components/InputTooltip.svelte';
import userEvent from '@testing-library/user-event';

describe('Input Tooltip', () => {
  it('has a label and tooltip', async () => {
    const labelText = 'Test Label Text';
    const tooltipText = 'Test label tooltip test';
    render(InputTooltip, {
      name: 'test',
      labelText,
      tooltipText
    });

    screen.getByText(labelText);
    const tooltip = screen.getByRole('button');
    expect(screen.queryByText(tooltipText)).not.toBeInTheDocument();

    await userEvent.click(tooltip);

    screen.getByText(tooltipText);
  });
});
