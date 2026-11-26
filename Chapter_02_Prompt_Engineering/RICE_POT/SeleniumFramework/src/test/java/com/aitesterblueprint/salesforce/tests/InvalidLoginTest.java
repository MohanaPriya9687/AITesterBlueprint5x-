package com.aitesterblueprint.salesforce.tests;

import static org.testng.Assert.assertEquals;
import static org.testng.Assert.assertTrue;

import java.time.Duration;

import com.aitesterblueprint.salesforce.pages.LoginPage;
import io.qameta.allure.Description;
import io.qameta.allure.Feature;
import io.qameta.allure.Story;
import io.qameta.allure.testng.AllureTestNg;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebDriverException;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.chrome.ChromeOptions;
import org.testng.SkipException;
import org.testng.annotations.AfterMethod;
import org.testng.annotations.BeforeMethod;
import org.testng.annotations.BeforeTest;
import org.testng.annotations.Listeners;
import org.testng.annotations.Test;

@Listeners(AllureTestNg.class)
@Feature("Salesforce login")
public final class InvalidLoginTest {
    private static final Duration WAIT_TIMEOUT = Duration.ofSeconds(30);
    private static final String REQUIRED_USERNAME_ERROR = "Error: Please enter your username.";

    private WebDriver driver;
    private LoginPage loginPage;

    @BeforeTest
    public void configureTestSuite() {
        System.setProperty("allure.results.directory", "target/allure-results");
    }

    @BeforeMethod
    public void startHeadedBrowser() {
        ChromeOptions options = new ChromeOptions();
        options.addArguments("--start-maximized", "--disable-notifications", "--lang=en-US");
        try {
            driver = new ChromeDriver(options);
            driver.manage().timeouts().implicitlyWait(Duration.ZERO);
            driver.manage().timeouts().pageLoadTimeout(WAIT_TIMEOUT);
            loginPage = new LoginPage(driver);
        } catch (WebDriverException exception) {
            closeDriver();
            throw new IllegalStateException(
                    "The headed Chrome browser could not be started. Confirm Chrome is installed and reachable.",
                    exception);
        }
    }

    @AfterMethod(alwaysRun = true)
    public void stopBrowser() {
        closeDriver();
    }

    @Test
    @Story("Required username validation")
    @Description("Submits the username login form empty and verifies the observed validation message.")
    public void emptyUsernameDisplaysRequiredFieldError() {
        loginPage.open();
        loginPage.submitWithoutUsername();
        assertEquals(loginPage.waitForNonEmptyErrorMessage(), REQUIRED_USERNAME_ERROR);
    }

    @Test
    @Story("Invalid credentials")
    @Description("Submits an approved invalid password for the configured Salesforce test username.")
    public void invalidPasswordDisplaysLoginError() {
        String username = configuredValue("SF_USERNAME");
        String invalidPassword = configuredValue("SF_INVALID_PASSWORD");
        if (username == null || invalidPassword == null) {
            throw new SkipException(
                    "Set SF_USERNAME and SF_INVALID_PASSWORD locally to run the invalid-password test.");
        }

        loginPage.open();
        assertTrue(loginPage.continueWithUsername(username),
                "Salesforce should present the password prompt for the configured test username.");
        loginPage.submitPassword(invalidPassword);
        assertTrue(loginPage.hasNonEmptyErrorMessage(),
                "Salesforce should display an error for the invalid password.");
        assertTrue(loginPage.currentUrl().contains("login.salesforce.com"),
                "An invalid password should not redirect away from the Salesforce login host.");
    }

    private static String configuredValue(String name) {
        String value = System.getenv(name);
        return value == null || value.isBlank() ? null : value;
    }

    private void closeDriver() {
        if (driver != null) {
            try {
                driver.quit();
            } catch (WebDriverException exception) {
                throw new IllegalStateException("The headed Chrome browser could not be closed cleanly.", exception);
            } finally {
                driver = null;
                loginPage = null;
            }
        }
    }
}
