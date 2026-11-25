1. Test case title
User should be locked out after 5 failed login attempts.

2. Preconditions
- The application is available and accessible.
- A valid user account exists with a known email and password.
- The user is on the login page.
- The system is configured to lock the account after 5 consecutive failed login attempts.
- Test data for invalid passwords is available.

3. Step-by-step actions
1. Navigate to the login page.
2. Enter a valid email address for the user.
3. Enter an incorrect password.
4. Click the Login button.
5. Repeat steps 2 to 4 four more times using the same email and an incorrect password each time.
6. Attempt to log in again using the same valid email and incorrect password.
7. Observe the account behavior and login status.

4. Expected results
- After the first four failed attempts, the user remains on the login page and can continue attempting to log in.
- After the fifth failed attempt, the account is locked out.
- A clear message is displayed indicating that the account has been temporarily locked due to too many failed login attempts.
- The user cannot log in successfully with the same credentials until the lockout period ends or the account is manually unlocked.
- The system does not allow unlimited retry attempts beyond the configured threshold.
- The error message is clear, accurate, and does not disclose any sensitive account information.
