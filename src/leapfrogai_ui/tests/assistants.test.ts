import { expect, test } from './fixtures';
import {loadChatPage} from "./helpers";

test('it navigates to the assistants page', async ({ page }) => {
	await loadChatPage(page);

    await page.getByLabel('Settings').click();
    await page.getByText("Assistants Management").click();

    await expect(page).toHaveTitle('LeapfrogAI - Assistants');

});
