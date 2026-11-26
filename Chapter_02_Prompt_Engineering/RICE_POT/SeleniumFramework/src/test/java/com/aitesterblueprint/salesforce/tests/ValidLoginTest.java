package com.aitesterblueprint.salesforce.tests;

import static org.testng.Assert.assertFalse;
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
public final class ValidLoginTest {
    private static final Duration WAIT_TIMEOUT = Duration.ofSeconds(30);

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
    @Story("Remember me")
    @Description("Checks that the Remember me option can be selected on the Salesforce username login form.")
    public void rememberMeCanBeSelected() {
        loginPage.open();
        loginPage.selectRememberMe();
        assertTrue(loginPage.isRememberMeSelected(), "Remember me should be selected after activation.");
    }

    @Test
    @Story("Valid credentials")
    @Description("Signs in with an approved Salesforce test account using credentials from environment variables.")
    public void validCredentialsRedirectToSalesforce() {
        String username = configuredValue("SF_USERNAME");
        String password = configuredValue("SF_PASSWORD");
        if (username == null || password == null) {
            throw new SkipException(
                    "Set SF_USERNAME and SF_PASSWORD locally to run the valid-credentials test.");
        }

        loginPage.open();
        assertTrue(loginPage.continueWithUsername(username),
                "Salesforce should present the password prompt for the configured username.");
        loginPage.submitPassword(password);
        assertTrue(loginPage.waitForRedirectFromLogin(),
                "Valid credentials should redirect away from the Salesforce login host.");
        assertFalse(loginPage.currentUrl().contains("login.salesforce.com"),
                "The successful login should leave the Salesforce login page.");
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
