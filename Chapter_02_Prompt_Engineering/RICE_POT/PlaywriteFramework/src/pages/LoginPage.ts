import { expect, type Locator, type Page } from '@playwright/test';

export class LoginPage {
  static readonly url =
    process.env.BASE_URL?.trim() || 'https://app.wingify.com/#/login';

  private readonly emailInput: Locator;
  private readonly passwordInput: Locator;
  private readonly signInButton: Locator;
  private readonly rememberMeLabel: Locator;
  private readonly rememberMeCheckbox: Locator;
  private readonly invalidLoginMessage: Locator;

  constructor(private readonly page: Page) {
    this.emailInput = page.locator(
      "xpath=(//input[@type='email' and @placeholder='Enter email ID'])[1]",
    );
    this.passwordInput = page.locator(
      "xpath=//input[@type='password' and @placeholder='Enter password']",
    );
    this.signInButton = page.locator(
      "xpath=(//button[@type='submit' and .//span[normalize-space(.)='Sign in']])[1]",
    );
    this.rememberMeLabel = page.locator(
      "xpath=//label[.//span[normalize-space(.)='Remember me']]",
    );
    this.rememberMeCheckbox = page.locator(
      "xpath=//input[@type='checkbox' and following-sibling::label[.//span[normalize-space(.)='Remember me']]]",
    );
    this.invalidLoginMessage = page.locator(
      "xpath=//div[contains(@class,'notification-box-description') and normalize-space(.)='Your email, password, IP address or location did not match']",
    );
  }

  async open(): Promise<void> {
    await this.page.goto(LoginPage.url, { waitUntil: 'domcontentloaded' });
    await expect(this.emailInput).toBeVisible();
  }

  async selectRememberMe(): Promise<void> {
    if (!(await this.rememberMeCheckbox.isChecked())) {
      await this.rememberMeLabel.click();
    }
  }

  async isRememberMeSelected(): Promise<boolean> {
    return this.rememberMeCheckbox.isChecked();
  }

  async submitEmptyLogin(): Promise<void> {
    await this.signInButton.click();
    await expect(this.invalidLoginMessage).toHaveText(
      'Your email, password, IP address or location did not match',
    );
  }

  async login(email: string, password: string): Promise<void> {
    this.requireValue(email, 'WINGFY_USERNAME');
    this.requireValue(password, 'WINGFY_PASSWORD');
    await this.emailInput.fill(email);
    await this.passwordInput.fill(password);
    await this.signInButton.click();
  }

  async waitForSuccessfulLogin(): Promise<void> {
    await expect(this.emailInput).toBeHidden();
  }

  async waitForInvalidLoginMessage(): Promise<void> {
    await expect(this.invalidLoginMessage).toHaveText(
      'Your email, password, IP address or location did not match',
    );
  }

  private requireValue(value: string, settingName: string): void {
    if (!value.trim()) {
      throw new Error(`${settingName} must be configured and non-blank.`);
    }
  }
}
