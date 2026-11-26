import { expect, test } from './fixtures';

test.describe('Wingify login', () => {
  test('Remember me can be selected', async ({ loginPage }) => {
    await loginPage.selectRememberMe();
    await expect
      .poll(() => loginPage.isRememberMeSelected())
      .toBe(true);
  });

  test('valid credentials sign in successfully', async ({ loginPage }) => {
    const email = process.env.WINGFY_USERNAME;
    const password = process.env.WINGFY_PASSWORD;
    if (!email?.trim() || !password?.trim()) {
      test.skip(true, 'Set WINGFY_USERNAME and WINGFY_PASSWORD in .env to run this test.');
      return;
    }

    await loginPage.login(email, password);
    await loginPage.waitForSuccessfulLogin();
  });
});
