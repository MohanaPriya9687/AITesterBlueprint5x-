import { test } from './fixtures';

test.describe('Wingify invalid login', () => {
  test('empty credentials display the observed invalid-login message', async ({ loginPage }) => {
    await loginPage.submitEmptyLogin();
    await loginPage.waitForInvalidLoginMessage();
  });
});
