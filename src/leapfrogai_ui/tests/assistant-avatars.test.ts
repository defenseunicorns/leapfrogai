import * as path from "node:path";
import { expect, test } from './fixtures';
import {getFakeNewAssistantInput} from "../testUtils/fakeData";
import {deleteAssistantByName} from "./helpers";

// TODO - unit test to ensure the pictogram name is right
test("it can choose a pictogram as an avatar", async ({page}) => {
    const assistantInput = getFakeNewAssistantInput();

    await page.goto('/chat/assistants-management/new');

    await page.getByLabel('name').fill(assistantInput.name);
    await page.getByLabel('description').fill(assistantInput.description);
    await page.getByPlaceholder("You'll act as...").fill(assistantInput.instructions);

    await page.locator('.mini-avatar-container').click();
    await page.locator('div:nth-child(2) > svg').click();
    await page.getByRole('dialog').getByRole('button', { name: 'Save' }).click();

    await page.getByRole('button', { name: 'Save' }).nth(1).click();

    // cleanup
    await deleteAssistantByName(assistantInput.name);
});

test("it can upload an image as an avatar", async ({page}) => {
    const assistantInput = getFakeNewAssistantInput();

    await page.goto('/chat/assistants-management/new');

    await page.getByLabel('name').fill(assistantInput.name);
    await page.getByLabel('description').fill(assistantInput.description);
    await page.getByPlaceholder("You'll act as...").fill(assistantInput.instructions);

    await page.locator('.mini-avatar-container').click();
    await page.getByText('Upload', { exact: true }).click();

    const fileChooserPromise = page.waitForEvent('filechooser');
    await page.locator('label').filter({ hasText: 'Upload from computer' }).click();
    const fileChooser = await fileChooserPromise;
    await fileChooser.setFiles('./tests/fixtures/Doug.png');

    await page.getByRole('dialog').getByRole('button', { name: 'Save' }).click();

    await page.getByRole('button', { name: 'Save' }).nth(1).click();


})