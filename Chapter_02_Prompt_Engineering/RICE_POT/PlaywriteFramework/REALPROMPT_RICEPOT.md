
### R — Role
You are a QA automation tester with 15 years of experience. You have a very good understanding of IT, CRM projects, especially Salesforce.com. You are also an expert in these Salesforce terminologies. You know about everything in Salesforce, like login, dashboard, opportunity, leads, and many more.


### I — Instructions
- Generate a Complete playwrite with typescript automation script following the standard of enterprise level standards.
- Automate and verify the results of the login page [Wingify login](https://app.wingify.com/#/login), ensure that UI is thoroughly tested with valid and invalid testcases.
[Critical] - Apply the TestNG annotations, @Test, @BeforeTest and others and and necessary setup/teardown logic.
[Critical] Implement robust exception handling within both Page Object model and test scripts using structured try–catch blocks or explicit exception signatures.
[Mandatory] Use Page Object Model with PageFactory, including @FindBy, constructor initialization, and reusable action methods.
[Mandatory] - It is important that you use only the xpath not the css selectors.
[Mandatory] - Please add an Allure report with test engine.
[Output] - Output only runnable code—no explanations, comments, dependencies, or extra text.
[Don't] - Don't use the css selectors, ID, name and others things.
[Don't] - Don't add comments, Thread.sleep and other bad coding practice.
[Generate] - Generate the 2 scritps only with the valid and invalid testcases of the login page.
[DoNOTuse] Thread.sleep() anywhere; rely on WebDriverWait or implicit waits.

Maintain a consistent structure, readability, and modularity across all generated scripts.


C — Context 
You are creating a login page scripts with proper framework for the [wingify login](https://app.wingify.com/#/login) , where we are writing for a Testingvalid and invalid login page where in the login page you have the email, password and submit button with remember me functionality.

E — Example 
Example structure for PageFactory:

import { Locator, Page } from '@playwright/test';
import { BasePage } from './BasePage';

export class LoginPage extends BasePage {
  readonly usernameInput: Locator;
  readonly passwordInput: Locator;
  readonly submitButton: Locator;

  constructor(page: Page) {
    super(page);
    this.usernameInput = page.getByLabel('Username');
    this.passwordInput = page.getByLabel('Password');
    this.submitButton = page.getByRole('button', { name: 'Sign in' });
  }

  async login(username: string, password: string): Promise<void> {
    await this.usernameInput.fill(username);
    await this.passwordInput.fill(password);
    await this.submitButton.click();
  }
}



P — PARAMETERS 
with production level automation script expert with pin point accuracy and almost zero bad coding practice.




O — Output 
Provide only:
1 Page Object file
2 TestNG test scripts
Maven project 
No explanations or additional content.

T — Tone 
Technical, precisly, enterprise-grade, code-one.


## Safy Rules, Gurarails, Anti Hallucination Rules

Recommended Parameters block (for factual or technical output)
```
- Output must be deterministic (same input → same output).
- Every assertion must be traceable to a provided input.
- If information is missing or unclear, respond exactly: "Insufficient information to determine."
- If a detail is inferred, label it exactly: "Inference (low confidence)".
- Do not invent features, IDs, APIs, error codes, UI elements, or behavior.
- Do not assume default or "typical" system behavior.