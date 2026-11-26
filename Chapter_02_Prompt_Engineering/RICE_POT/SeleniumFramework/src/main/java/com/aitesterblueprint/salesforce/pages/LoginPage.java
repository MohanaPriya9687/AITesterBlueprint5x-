package com.aitesterblueprint.salesforce.pages;

import java.net.URI;
import java.time.Duration;
import java.util.Objects;
import java.util.function.Function;

import org.jspecify.annotations.NonNull;
import org.jspecify.annotations.Nullable;
import org.openqa.selenium.By;
import org.openqa.selenium.StaleElementReferenceException;
import org.openqa.selenium.TimeoutException;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebDriverException;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.FindBy;
import org.openqa.selenium.support.PageFactory;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;

public final class LoginPage {
    private static final String LOGIN_URL = "https://login.salesforce.com/?login=1&locale=in";
    private static final String LOGIN_HOST = "login.salesforce.com";
    private static final Duration WAIT_TIMEOUT = Duration.ofSeconds(20);

    private static final @NonNull By USERNAME_LOCATOR =
            By.xpath("//input[@autocomplete='username' and not(@type='hidden')]");
    private static final @NonNull By PASSWORD_LOCATOR = By.xpath("//input[@type='password']");
    private static final @NonNull By ERROR_LOCATOR =
            By.xpath("//div[@id='error' and @aria-live='polite']");
    private static final @NonNull By LOGIN_BUTTON_LOCATOR =
            By.xpath("//input[@type='submit' and @value='Log In']");
    private static final @NonNull By REMEMBER_ME_LOCATOR =
            By.xpath("//input[@type='checkbox' and @name='rememberUn']");
    private static final @NonNull By BODY_LOCATOR = By.xpath("//body");

    private final WebDriver driver;
    private final WebDriverWait wait;

    @FindBy(xpath = "//input[@autocomplete='username' and not(@type='hidden')]")
    private @Nullable WebElement usernameInput;

    @FindBy(xpath = "//input[@type='password']")
    private @Nullable WebElement passwordInput;

    @FindBy(xpath = "//input[@type='submit' and @value='Log In']")
    private @Nullable WebElement loginButton;

    public LoginPage(WebDriver driver) {
        this.driver = Objects.requireNonNull(driver, "WebDriver must not be null");
        this.wait = new WebDriverWait(driver, WAIT_TIMEOUT);
        PageFactory.initElements(driver, this);
    }

    public void open() {
        try {
            driver.get(LOGIN_URL);
            wait.until(ExpectedConditions.visibilityOfElementLocated(USERNAME_LOCATOR));
        } catch (WebDriverException exception) {
            throw new IllegalStateException(
                    "Salesforce username login page could not be opened or located. Page title: "
                            + safePageTitle() + "; host/path: " + safeLocation()
                            + "; visible text: " + safeVisibleText(),
                    exception);
        }
    }

    public boolean isRememberMeSelected() {
        try {
            return Boolean.TRUE.equals(wait.until(driver -> {
                try {
                    WebElement checkbox = driver.findElement(REMEMBER_ME_LOCATOR);
                    return checkbox.isDisplayed() && checkbox.isSelected();
                } catch (StaleElementReferenceException exception) {
                    return false;
                }
            }));
        } catch (WebDriverException exception) {
            throw new IllegalStateException("The Salesforce Remember me control is unavailable.", exception);
        }
    }

    public void selectRememberMe() {
        try {
            WebElement checkbox = Objects.requireNonNull(
                    wait.until(ExpectedConditions.elementToBeClickable(REMEMBER_ME_LOCATOR)),
                    "The Salesforce Remember me control was not found.");
            if (!checkbox.isSelected()) {
                checkbox.click();
            }
        } catch (WebDriverException exception) {
            throw new IllegalStateException("The Salesforce Remember me control could not be selected.", exception);
        }
    }

    public boolean continueWithUsername(@Nullable String username) {
        String validUsername = requireValue(username, "Username");
        try {
            WebElement usernameField = Objects.requireNonNull(
                    wait.until(ExpectedConditions.visibilityOfElementLocated(USERNAME_LOCATOR)),
                    "The Salesforce username field was not found.");
            usernameField.sendKeys(validUsername);
            WebElement button = Objects.requireNonNull(
                    wait.until(ExpectedConditions.elementToBeClickable(LOGIN_BUTTON_LOCATOR)),
                    "The Salesforce login button was not found.");
            button.click();
            return Boolean.TRUE.equals(wait.until(
                    driver -> isVisible(PASSWORD_LOCATOR) || hasNonEmptyErrorMessage()));
        } catch (WebDriverException exception) {
            throw new IllegalStateException(
                    "Salesforce did not present a password prompt or login error after username submission.",
                    exception);
        }
    }

    public void submitPassword(@Nullable String password) {
        String validPassword = requireValue(password, "Password");
        try {
            WebElement passwordField = Objects.requireNonNull(
                    wait.until(ExpectedConditions.visibilityOfElementLocated(PASSWORD_LOCATOR)),
                    "The Salesforce password field was not found.");
            passwordField.sendKeys(validPassword);
            WebElement button = Objects.requireNonNull(
                    wait.until(ExpectedConditions.elementToBeClickable(LOGIN_BUTTON_LOCATOR)),
                    "The Salesforce login button was not found.");
            button.click();
        } catch (WebDriverException exception) {
            throw new IllegalStateException("Salesforce password submission could not be completed.", exception);
        }
    }

    public boolean hasNonEmptyErrorMessage() {
        try {
            for (WebElement element : driver.findElements(ERROR_LOCATOR)) {
                if (element.isDisplayed() && !element.getText().isBlank()) {
                    return true;
                }
            }
            return false;
        } catch (StaleElementReferenceException exception) {
            return false;
        } catch (WebDriverException exception) {
            throw new IllegalStateException("Salesforce login error state could not be inspected.", exception);
        }
    }

    public String waitForNonEmptyErrorMessage() {
        try {
            Function<WebDriver, @Nullable String> visibleErrorMessage = driver -> {
                for (WebElement element : driver.findElements(ERROR_LOCATOR)) {
                    if (element.isDisplayed()) {
                        String text = Objects.toString(element.getText(), "").trim();
                        if (!text.isEmpty()) {
                            return text;
                        }
                    }
                }
                return null;
            };
            return Objects.requireNonNull(
                    wait.until(visibleErrorMessage),
                    "Salesforce did not display a login error message.");
        } catch (TimeoutException exception) {
            throw new IllegalStateException("Salesforce did not display a login error message.", exception);
        }
    }

    public boolean isUsernameLoginVisible() {
        return isVisible(USERNAME_LOCATOR);
    }

    public boolean isPasswordPromptVisible() {
        return isVisible(PASSWORD_LOCATOR);
    }

    public boolean waitForRedirectFromLogin() {
        try {
            return Boolean.TRUE.equals(wait.until(driver -> {
                String currentUrl = Objects.toString(driver.getCurrentUrl(), "");
                if (currentUrl.isBlank()) {
                    return false;
                }
                try {
                    String host = Objects.toString(URI.create(currentUrl).getHost(), "");
                    return !host.isBlank() && !LOGIN_HOST.equalsIgnoreCase(host);
                } catch (IllegalArgumentException exception) {
                    return false;
                }
            }));
        } catch (TimeoutException exception) {
            return false;
        } catch (WebDriverException exception) {
            throw new IllegalStateException("Salesforce redirect state could not be inspected.", exception);
        }
    }

    public String currentUrl() {
        try {
            return Objects.requireNonNull(
                    driver.getCurrentUrl(),
                    "WebDriver did not provide the current URL.");
        } catch (WebDriverException exception) {
            throw new IllegalStateException("The Salesforce current URL could not be read.", exception);
        }
    }

    public void submitWithoutUsername() {
        try {
            WebElement pageFactoryButton = Objects.requireNonNull(
                    loginButton,
                    "The Salesforce login button was not initialized.");
            WebElement button = Objects.requireNonNull(
                    wait.until(ExpectedConditions.elementToBeClickable(pageFactoryButton)),
                    "The Salesforce login button was not available.");
            button.click();
            wait.until(driver -> hasNonEmptyErrorMessage());
        } catch (WebDriverException exception) {
            throw new IllegalStateException(
                    "Salesforce did not show the required-username validation message.", exception);
        }
    }

    private boolean isVisible(@NonNull By locator) {
        try {
            for (WebElement element : driver.findElements(locator)) {
                if (element.isDisplayed()) {
                    return true;
                }
            }
            return false;
        } catch (StaleElementReferenceException exception) {
            return false;
        } catch (WebDriverException exception) {
            throw new IllegalStateException("Salesforce login controls could not be inspected.", exception);
        }
    }

    private String safePageTitle() {
        try {
            return Objects.toString(driver.getTitle(), "unavailable");
        } catch (WebDriverException exception) {
            return "unavailable";
        }
    }

    private String safeLocation() {
        try {
            URI uri = URI.create(Objects.toString(driver.getCurrentUrl(), ""));
            String host = Objects.toString(uri.getHost(), "");
            if (host.isBlank()) {
                return "unavailable";
            }
            return host + Objects.toString(uri.getPath(), "");
        } catch (IllegalArgumentException | WebDriverException exception) {
            return "unavailable";
        }
    }

    private String safeVisibleText() {
        try {
            String text = driver.findElement(BODY_LOCATOR).getText().replaceAll("\\s+", " ");
            return text.substring(0, Math.min(300, text.length()));
        } catch (WebDriverException exception) {
            return "unavailable";
        }
    }

    private static String requireValue(@Nullable String value, String fieldName) {
        if (value == null || value.isBlank()) {
            throw new IllegalArgumentException(fieldName + " must be configured and non-blank.");
        }
        return value;
    }
}
