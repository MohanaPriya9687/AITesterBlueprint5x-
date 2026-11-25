from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, PageBreak, Table, TableStyle, ListFlowable, ListItem

OUTPUT_DIR = Path(__file__).resolve().parent
HTML_PATH = OUTPUT_DIR / "vwo_login_dashboard_test_plan_company_style.html"
PDF_PATH = OUTPUT_DIR / "vwo_login_dashboard_test_plan_company_style.pdf"

VWO_ORANGE = colors.HexColor("#F26B2C")
VWO_BLUE = colors.HexColor("#0F2B46")
VWO_LIGHT = colors.HexColor("#F7F7F8")
VWO_TEXT = colors.HexColor("#1F2A37")
VWO_MUTED = colors.HexColor("#5B6470")


def style_doc():
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='VWOTitle', fontName='Helvetica-Bold', fontSize=24, textColor=VWO_BLUE, leading=28, spaceAfter=10, alignment=1))
    styles.add(ParagraphStyle(name='VWOSection', fontName='Helvetica-Bold', fontSize=15, textColor=VWO_BLUE, leading=20, spaceBefore=18, spaceAfter=8, borderWidth=0))
    styles.add(ParagraphStyle(name='VWOBody', fontName='Helvetica', fontSize=10.5, textColor=VWO_TEXT, leading=15, spaceAfter=6))
    styles.add(ParagraphStyle(name='VWOBodyBold', parent=styles['VWOBody'], fontName='Helvetica-Bold'))
    styles.add(ParagraphStyle(name='VWOList', parent=styles['VWOBody'], leftIndent=18, bulletIndent=10, spaceAfter=4))
    styles.add(ParagraphStyle(name='VWOCaption', fontName='Helvetica', fontSize=9, textColor=VWO_MUTED, leading=12, alignment=1, spaceAfter=12))
    styles.add(ParagraphStyle(name='VWOHeader', fontName='Helvetica-Bold', fontSize=12, textColor=VWO_ORANGE, leading=16, spaceBefore=4, spaceAfter=6))
    return styles


def para(text, style_name='VWOBody'):
    return Paragraph(text, style_doc()[style_name])


def bullet_list(items):
    return ListFlowable(
        [ListItem(Paragraph(item, style_doc()['VWOList']), bulletType='1') for item in items],
        bulletType='1',
        leftIndent=20,
        style=style_doc()['VWOList'],
    )


def make_html_doc():
    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8" />
      <meta name="viewport" content="width=device-width, initial-scale=1.0" />
      <title>VWO Login Dashboard Test Plan</title>
      <style>
        body { font-family: Arial, Helvetica, sans-serif; margin: 32px; color: #1f2a37; background: #ffffff; }
        .header { background: #0F2B46; color: white; padding: 24px 28px; border-radius: 10px; }
        .header h1 { margin: 0; font-size: 30px; }
        .small { font-size: 12px; letter-spacing: 0.04em; text-transform: uppercase; color: #f5f5f5; }
        .section { margin-top: 28px; padding-top: 10px; border-top: 3px solid #F26B2C; }
        h2 { color: #0F2B46; margin-bottom: 10px; font-size: 18px; }
        h3 { color: #F26B2C; margin-bottom: 8px; font-size: 14px; }
        p, li { font-size: 12px; line-height: 1.7; }
        table { width: 100%; border-collapse: collapse; margin-top: 10px; }
        th, td { border: 1px solid #dfe3e8; padding: 8px 10px; font-size: 12px; vertical-align: top; }
        th { background: #F7F7F8; color: #0F2B46; text-align: left; }
        ul { padding-left: 22px; }
        .meta { background: #F7F7F8; border: 1px solid #e6e9ed; padding: 16px; border-radius: 8px; }
      </style>
    </head>
    <body>
      <div class="header">
        <div class="small">VWO | Quality Engineering</div>
        <h1>Login Dashboard Test Plan</h1>
      </div>

      <div class="meta" style="margin-top: 18px;">
        <p><strong>Product:</strong> VWO Login Dashboard</p>
        <p><strong>Environment:</strong> app.vwo.com</p>
        <p><strong>Purpose:</strong> Validate secure access, login usability, and dashboard onboarding experience.</p>
      </div>

      <div class="section">
        <h2>1. Objective</h2>
        <p>The goal of this test plan is to validate that the VWO login dashboard provides secure, reliable, and user-friendly access to the platform while supporting responsive usage across desktop and mobile environments.</p>
        <p>Testing will confirm that users can successfully sign in, recover access when needed, and move into the VWO experience without friction, while preserving consistent accessibility and data integrity.</p>
      </div>

      <div class="section">
        <h2>2. Scope</h2>
        <p>This plan covers the VWO login dashboard and related authentication journey, including sign-in, validation, recovery flows, accessibility, responsiveness, and onboarding transition to the main product experience.</p>
        <ul>
          <li>Functional validation for login and recovery flows</li>
          <li>Security and data handling checks for authentication inputs and session management</li>
          <li>Responsive and cross-browser validation for web and mobile experiences</li>
          <li>Accessibility reviews for keyboard, focus, and screen reader support</li>
          <li>Regression validation after changes to authentication logic or UI updates</li>
        </ul>
      </div>

      <div class="section">
        <h2>3. Inclusions</h2>
        <ul>
          <li>Login with email and password</li>
          <li>Validation for required fields and incorrect credentials</li>
          <li>Forgot password flow and account recovery support</li>
          <li>Remember me functionality</li>
          <li>Registration link and trial onboarding entry point</li>
          <li>Session timeout and secure redirect behavior</li>
          <li>Responsive behavior across desktop and mobile breakpoints</li>
          <li>Accessibility checks for labels, focus order, and keyboard interaction</li>
        </ul>
      </div>

      <div class="section">
        <h2>4. Test Environments</h2>
        <table>
          <tr><th>Category</th><th>Configuration</th></tr>
          <tr><td>Primary URL</td><td>https://app.vwo.com/login</td></tr>
          <tr><td>Desktop Browsers</td><td>Windows 10: Chrome, Firefox, Edge</td></tr>
          <tr><td>Mobile Browsers</td><td>Android: Chrome; iPhone: Safari</td></tr>
          <tr><td>Operating Systems</td><td>Windows 10, macOS, Android, iPhone OS</td></tr>
          <tr><td>Network</td><td>Wi-Fi, mobile data, and standard broadband conditions</td></tr>
          <tr><td>Access Model</td><td>Standard user, trial user, and account recovery scenarios</td></tr>
        </table>
      </div>

      <div class="section">
        <h2>5. Test Strategy</h2>
        <p>The testing approach follows a layered strategy combining functional validation, UX review, cross-environment checks, accessibility evaluation, and regression monitoring.</p>
        <h3>Design Techniques</h3>
        <ul>
          <li>Equivalence class partitioning</li>
          <li>Boundary value analysis</li>
          <li>Decision table testing</li>
          <li>State transition testing</li>
          <li>Use case testing</li>
          <li>Error guessing and exploratory testing</li>
        </ul>
        <h3>Execution Model</h3>
        <ul>
          <li>Smoke testing for critical login flows before detailed validation</li>
          <li>Detailed functional, UI, and accessibility validation on stable builds</li>
          <li>Parallel execution across supported environments when feasible</li>
          <li>Regression checks after each change that affects authentication or navigation</li>
        </ul>
      </div>

      <div class="section">
        <h2>6. Test Schedule</h2>
        <table>
          <tr><th>Activity</th><th>Planned Window</th></tr>
          <tr><td>Test planning and scope confirmation</td><td>Week 1</td></tr>
          <tr><td>Test case design</td><td>Week 1-2</td></tr>
          <tr><td>Smoke and functional validation</td><td>Week 2-3</td></tr>
          <tr><td>Responsive and accessibility review</td><td>Week 3</td></tr>
          <tr><td>Regression and sign-off</td><td>Week 4</td></tr>
        </table>
      </div>

      <div class="section">
        <h2>7. Entry and Exit Criteria</h2>
        <h3>Entry Criteria</h3>
        <ul>
          <li>Requirements and user flows are clearly defined</li>
          <li>Build is available for each target environment</li>
          <li>Test data supports valid and invalid authentication scenarios</li>
          <li>Acceptance criteria for login and recovery flows are documented</li>
        </ul>
        <h3>Exit Criteria</h3>
        <ul>
          <li>All critical and high-priority test cases are executed</li>
          <li>Defects are triaged and either resolved or accepted with justification</li>
          <li>Regression checks are completed</li>
          <li>Test summary and sign-off evidence are prepared</li>
        </ul>
      </div>

      <div class="section">
        <h2>8. Test Execution</h2>
        <h3>Core Functional Scenarios</h3>
        <ul>
          <li>Successful login using valid email and password</li>
          <li>Validation when email format is invalid</li>
          <li>Validation when password is missing or incorrect</li>
          <li>Maintained session behavior after login</li>
          <li>Redirect to the main dashboard after successful sign-in</li>
          <li>Forgot password flow with secure reset confirmation</li>
          <li>Remember me behavior across sessions</li>
          <li>Registration flow and onboarding journey entry</li>
        </ul>
        <h3>Usability and Accessibility Scenarios</h3>
        <ul>
          <li>Keyboard-only navigation through login form</li>
          <li>Visible focus states on all interactive controls</li>
          <li>Clickable labels and proper field association</li>
          <li>Touch-friendly target sizing on mobile devices</li>
          <li>Screen reader compatibility for form instructions and errors</li>
          <li>High-contrast readability across light and dark modes</li>
        </ul>
      </div>

      <div class="section">
        <h2>9. Defect Reporting Procedure</h2>
        <p>All defects are logged with clear reproduction steps, expected result, actual result, environment details, and screenshots or screen recordings where helpful. Each issue is classified by severity and priority and reviewed before closure.</p>
        <ul>
          <li>Capture accurate reproduction steps and browser/device context</li>
          <li>Attach evidence such as screenshots, logs, or recordings</li>
          <li>Associate each finding to relevant user flow or requirement</li>
          <li>Confirm fix status and retest with the original scenario</li>
        </ul>
      </div>

      <div class="section">
        <h2>10. Tools</h2>
        <ul>
          <li>JIRA for defect tracking and issue management</li>
          <li>Browser developer tools for validation and debugging</li>
          <li>Screen capture tools for evidence collection</li>
          <li>Documentation tools for test case and summary reporting</li>
        </ul>
      </div>

      <div class="section">
        <h2>11. Deliverables</h2>
        <ul>
          <li>Test plan</li>
          <li>Test scenarios and test cases</li>
          <li>Execution report</li>
          <li>Defect log and summary</li>
          <li>Final sign-off report</li>
        </ul>
      </div>

      <div class="section">
        <h2>12. Approvals</h2>
        <p>Testing will continue only after the required documentation is reviewed and approved for the relevant release milestone. Approval checkpoints include the test plan, execution readiness, and the final summary report.</p>
      </div>
    </body>
    </html>
    """
    return html


def build_pdf():
    styles = style_doc()
    story = []

    story.append(Paragraph("VWO Login Dashboard", styles['VWOTitle']))
    story.append(Paragraph("Test Plan", styles['VWOCaption']))
    story.append(Spacer(1, 8 * mm))

    title_table = Table(
        [[Paragraph("Product", styles['VWOBodyBold']), Paragraph("VWO Login Dashboard", styles['VWOBody'])],
         [Paragraph("Target URL", styles['VWOBodyBold']), Paragraph("https://app.vwo.com/login", styles['VWOBody'])],
         [Paragraph("Objective", styles['VWOBodyBold']), Paragraph("Validate secure, consistent, and user-friendly access to the platform and the onboarding path into the main dashboard experience.", styles['VWOBody'])]],
        colWidths=[40 * mm, 125 * mm],
        style=TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), VWO_LIGHT),
            ('GRID', (0, 0), (-1, -1), 0.5, VWO_BLUE),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('ROWBACKGROUNDS', (0, 0), (-1, -1), [colors.white, VWO_LIGHT]),
        ])
    )
    story.append(title_table)
    story.append(Spacer(1, 8 * mm))

    def add_section(title, body_lines=None, bullet_lines=None):
        story.append(Paragraph(title, styles['VWOSection']))
        if body_lines:
            for line in body_lines:
                story.append(Paragraph(line, styles['VWOBody']))
        if bullet_lines:
            for line in bullet_lines:
                story.append(Paragraph(f"• {line}", styles['VWOList']))
        story.append(Spacer(1, 4 * mm))

    add_section(
        "1. Objective",
        [
            "The goal of this test plan is to validate that the VWO login dashboard provides secure, reliable, and intuitive access to the platform while supporting responsive usage across desktop and mobile environments.",
            "Testing will confirm that users can successfully sign in, recover access when needed, and move into the VWO experience without friction while preserving accessibility and data integrity."
        ]
    )

    add_section(
        "2. Scope",
        [
            "This test plan covers the VWO login dashboard and related authentication journey, including sign-in, validation, recovery flows, accessibility, responsiveness, and onboarding transition to the main product experience."
        ],
        [
            "Functional validation of login and recovery flows",
            "Validation of secure access behavior and session handling",
            "Responsive and cross-browser experience checks",
            "Accessibility validation for keyboard and screen reader support",
            "Regression verification after authentication or UI changes"
        ]
    )

    add_section(
        "3. Inclusions",
        bullet_lines=[
            "Login with email and password",
            "Validation for required fields and incorrect credentials",
            "Forgot password flow and account recovery support",
            "Remember Me functionality",
            "Registration link and onboarding entry point",
            "Session timeout and secure redirect behavior",
            "Responsive behavior across desktop and mobile layouts",
            "Accessibility checks for labels, focus order, and keyboard interaction"
        ]
    )

    env_table = Table(
        [[Paragraph("Category", styles['VWOBodyBold']), Paragraph("Environment / Configuration", styles['VWOBodyBold'])],
         [Paragraph("Primary URL", styles['VWOBody']), Paragraph("https://app.vwo.com/login", styles['VWOBody'])],
         [Paragraph("Desktop Browsers", styles['VWOBody']), Paragraph("Windows 10: Chrome, Firefox, Edge", styles['VWOBody'])],
         [Paragraph("Mobile Browsers", styles['VWOBody']), Paragraph("Android: Chrome; iPhone: Safari", styles['VWOBody'])],
         [Paragraph("Operating Systems", styles['VWOBody']), Paragraph("Windows 10, macOS, Android, iPhone OS", styles['VWOBody'])],
         [Paragraph("Network", styles['VWOBody']), Paragraph("Wi-Fi, mobile data, and standard broadband conditions", styles['VWOBody'])],
         [Paragraph("Access Model", styles['VWOBody']), Paragraph("Standard user, trial user, and account recovery scenarios", styles['VWOBody'])]],
        colWidths=[48 * mm, 110 * mm],
        style=TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), VWO_LIGHT),
            ('GRID', (0, 0), (-1, -1), 0.5, VWO_BLUE),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ])
    )
    story.append(Paragraph("4. Test Environments", styles['VWOSection']))
    story.append(env_table)
    story.append(Spacer(1, 6 * mm))

    add_section(
        "5. Test Strategy",
        [
            "The testing approach follows a layered strategy combining functional validation, user experience review, accessibility assessment, and regression verification."
        ],
        [
            "Equivalence class partitioning",
            "Boundary value analysis",
            "Decision table testing",
            "State transition testing",
            "Use case testing",
            "Error guessing and exploratory testing",
            "Smoke testing before deeper validation",
            "Parallel validation across supported environments where feasible"
        ]
    )

    schedule_table = Table(
        [[Paragraph("Activity", styles['VWOBodyBold']), Paragraph("Planned Window", styles['VWOBodyBold'])],
         [Paragraph("Test planning and scope confirmation", styles['VWOBody']), Paragraph("Week 1", styles['VWOBody'])],
         [Paragraph("Test case design", styles['VWOBody']), Paragraph("Week 1-2", styles['VWOBody'])],
         [Paragraph("Smoke and functional validation", styles['VWOBody']), Paragraph("Week 2-3", styles['VWOBody'])],
         [Paragraph("Responsive and accessibility review", styles['VWOBody']), Paragraph("Week 3", styles['VWOBody'])],
         [Paragraph("Regression and sign-off", styles['VWOBody']), Paragraph("Week 4", styles['VWOBody'])]],
        colWidths=[90 * mm, 60 * mm],
        style=TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), VWO_LIGHT),
            ('GRID', (0, 0), (-1, -1), 0.5, VWO_BLUE),
        ])
    )
    story.append(Paragraph("6. Test Schedule", styles['VWOSection']))
    story.append(schedule_table)
    story.append(Spacer(1, 6 * mm))

    add_section(
        "7. Entry and Exit Criteria",
        None,
        [
            "Entry criteria: requirements and user flows are clearly defined; build is available for target environments; test data covers valid and invalid scenarios; acceptance criteria are documented.",
            "Exit criteria: all critical and high priority scenarios are executed; defects are triaged and resolved or accepted with justification; regression checks are complete; summary evidence is ready for sign-off."
        ]
    )

    add_section(
        "8. Test Execution",
        [
            "The execution phase validates the critical success path and the key exception paths for login and recovery behavior."
        ],
        [
            "Successful login with valid credentials",
            "Validation for missing, invalid, or incorrect email and password entries",
            "Forgot password and account recovery checks",
            "Remember Me persistence behavior",
            "Redirect and session continuity after successful authentication",
            "Keyboard-only navigation and form accessibility checks",
            "Mobile responsiveness across common device widths",
            "Regression checks after authentication and layout updates"
        ]
    )

    add_section(
        "9. Defect Reporting Procedure",
        [
            "All defects are logged with clear reproduction steps, expected result, actual result, environment details, and supporting evidence such as screenshots or screen recordings."
        ],
        [
            "Capture accurate reproduction steps and environment context",
            "Attach screenshots, logs, or recordings when relevant",
            "Associate the issue with the affected user flow or requirement",
            "Verify resolution with retesting before closure"
        ]
    )

    add_section(
        "10. Tools",
        None,
        [
            "JIRA for issue management and defect tracking",
            "Browser developer tools for validation and debugging",
            "Screen capture tools for evidence collection",
            "Documentation tools for test case and summary reporting"
        ]
    )

    add_section(
        "11. Deliverables",
        None,
        [
            "Test plan",
            "Test scenarios and test cases",
            "Execution report",
            "Defect log and summary",
            "Final sign-off report"
        ]
    )

    add_section(
        "12. Approvals",
        [
            "Testing continues only after the required documentation is reviewed and approved for the relevant release milestone. Approval checkpoints include the test plan, execution readiness, and the final summary report."
        ]
    )

    story.append(Paragraph("Prepared for: VWO Product Quality Review", styles['VWOCaption']))

    doc = SimpleDocTemplate(
        str(PDF_PATH),
        pagesize=A4,
        leftMargin=18 * mm,
        rightMargin=18 * mm,
        topMargin=16 * mm,
        bottomMargin=16 * mm,
    )
    doc.build(story)


def write_html_file():
    with open(HTML_PATH, "w", encoding="utf-8") as f:
        f.write(make_html_doc())


if __name__ == "__main__":
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    write_html_file()
    build_pdf()
    print(f"HTML: {HTML_PATH}")
    print(f"PDF: {PDF_PATH}")
