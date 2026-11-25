from datetime import datetime
from html import escape
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    KeepTogether,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


OUTPUT = Path(__file__).resolve().parent / "V4-1_test_cases_draft.pdf"

NAVY = colors.HexColor("#0F2B46")
ORANGE = colors.HexColor("#F26B2C")
INK = colors.HexColor("#1F2A37")
MUTED = colors.HexColor("#5B6470")
PALE = colors.HexColor("#F3F6F8")
GRID = colors.HexColor("#D7DEE5")

STYLES = getSampleStyleSheet()
STYLES.add(
    ParagraphStyle(
        name="DocTitle",
        parent=STYLES["Title"],
        fontName="Helvetica-Bold",
        fontSize=22,
        leading=27,
        textColor=NAVY,
        alignment=TA_LEFT,
        spaceAfter=5,
    )
)
STYLES.add(
    ParagraphStyle(
        name="Subtitle",
        parent=STYLES["Normal"],
        fontName="Helvetica",
        fontSize=10,
        leading=14,
        textColor=MUTED,
        spaceAfter=9,
    )
)
STYLES.add(
    ParagraphStyle(
        name="Section",
        parent=STYLES["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=14,
        leading=18,
        textColor=NAVY,
        spaceBefore=12,
        spaceAfter=6,
        keepWithNext=True,
    )
)
STYLES.add(
    ParagraphStyle(
        name="CaseTitle",
        parent=STYLES["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=11,
        leading=14,
        textColor=NAVY,
        spaceBefore=9,
        spaceAfter=4,
        keepWithNext=True,
    )
)
STYLES.add(
    ParagraphStyle(
        name="Body",
        parent=STYLES["BodyText"],
        fontName="Helvetica",
        fontSize=8.8,
        leading=12,
        textColor=INK,
        spaceAfter=4,
    )
)
STYLES.add(
    ParagraphStyle(
        name="Small",
        parent=STYLES["BodyText"],
        fontName="Helvetica",
        fontSize=7.8,
        leading=10.2,
        textColor=INK,
        spaceAfter=2,
    )
)
STYLES.add(
    ParagraphStyle(
        name="Header",
        parent=STYLES["BodyText"],
        fontName="Helvetica-Bold",
        fontSize=8,
        leading=10,
        textColor=colors.white,
    )
)


def para(text, style="Body"):
    return Paragraph(escape(str(text)), STYLES[style])


def page_chrome(canvas, doc):
    canvas.saveState()
    width, _ = A4
    canvas.setStrokeColor(GRID)
    canvas.setLineWidth(0.5)
    canvas.line(18 * mm, 13 * mm, width - 18 * mm, 13 * mm)
    canvas.setFont("Helvetica", 7.5)
    canvas.setFillColor(MUTED)
    canvas.drawString(
        18 * mm,
        8.5 * mm,
        "V4-1 | Test case draft | Human review required",
    )
    canvas.drawRightString(width - 18 * mm, 8.5 * mm, f"Page {doc.page}")
    canvas.restoreState()


def info_table(rows):
    table = Table(
        [[para(label, "Small"), para(value, "Small")] for label, value in rows],
        colWidths=[43 * mm, 130 * mm],
    )
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (0, -1), PALE),
                ("GRID", (0, 0), (-1, -1), 0.4, GRID),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 5),
                ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]
        )
    )
    return table


def make_case(case):
    steps = Table(
        [
            [para("Step", "Header"), para("Action", "Header"), para("Expected result", "Header")]
        ]
        + [
            [para(str(index), "Small"), para(action, "Small"), para(expected, "Small")]
            for index, (action, expected) in enumerate(case["steps"], start=1)
        ],
        colWidths=[12 * mm, 72 * mm, 89 * mm],
        repeatRows=1,
        splitByRow=1,
    )
    steps.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), NAVY),
                ("GRID", (0, 0), (-1, -1), 0.4, GRID),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, PALE]),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 4),
                ("RIGHTPADDING", (0, 0), (-1, -1), 4),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]
        )
    )
    block = [
        Paragraph(
            escape(f'{case["id"]} — {case["title"]}'),
            STYLES["CaseTitle"],
        ),
        info_table(
            [
                ("ID", case["id"]),
                ("Title", case["title"]),
                ("Priority", case["priority"]),
                ("Type", case["type"]),
                ("Traceability", case["trace"]),
                ("Preconditions", case["preconditions"]),
                ("Test data", case["data"]),
            ]
        ),
        Spacer(1, 2 * mm),
        steps,
        Spacer(1, 2 * mm),
        para("Overall expected result: " + case["overall"]),
        para("Notes: " + case["notes"], "Small"),
        para("Postconditions / cleanup: " + case["cleanup"], "Small"),
        Spacer(1, 2 * mm),
    ]
    return block


CASES = [
    {
        "id": "TC-V4-1-001",
        "title": "Display both new login options below Sign in with Google",
        "priority": "High (provisional; confirm case-level priority)",
        "type": "Functional / UI",
        "trace": "Scenario: Verify both new buttons are visible and correctly positioned; AC: UI Visibility",
        "preconditions": "Agreed V4-1 test environment is available; tester can access its login page.",
        "data": "D-UI-01: Agreed login-page environment. The URL is not specified in the ticket.",
        "steps": [
            ("Open the agreed V4-1 login page.", "The login page is displayed."),
            ("Locate the “Sign in with Google” option.", "The Google option is visible."),
            ("Locate the “Sign in using SSO” and “Sign in with Passkey” options.", "Both controls are visible and their labels match the acceptance criteria."),
            ("Compare each new option's position with the Google option.", "Both new options are displayed below the Google option. The ticket does not define the relative order of the two new options."),
        ],
        "overall": "Both correctly labelled options are visible below Sign in with Google.",
        "notes": "Do not infer a required order between SSO and Passkey; the ticket does not specify one.",
        "cleanup": "None.",
    },
    {
        "id": "TC-V4-1-002",
        "title": "Check login options for responsiveness",
        "priority": "Medium (provisional; confirm case-level priority)",
        "type": "UI / Responsive",
        "trace": "Scenario: Verify UI responsiveness and accessibility; AC: UI Visibility",
        "preconditions": "Agreed login-page environment is available; approved viewport/device matrix is supplied.",
        "data": "D-UI-02: Product-approved viewport and device matrix; not specified in the ticket.",
        "steps": [
            ("Open the login page at each viewport/device in the approved matrix.", "The login page loads for the selected test configuration."),
            ("Inspect the Google, SSO, and Passkey options at each configuration.", "Record visibility, labels, and layout at each configuration."),
            ("Compare the result with the approved responsive acceptance criteria.", "Pass/fail thresholds are applied only after the required breakpoints and layout expectations are confirmed."),
        ],
        "overall": "Responsive behavior is assessed against criteria to be supplied; the ticket does not specify screen sizes, breakpoints, or layout thresholds.",
        "notes": "Until viewport/device requirements are agreed, observations can be recorded but a definitive responsive pass/fail cannot be assigned.",
        "cleanup": "Restore the agreed default viewport.",
    },
    {
        "id": "TC-V4-1-003",
        "title": "Review keyboard and assistive-technology accessibility of login options",
        "priority": "Medium (provisional; confirm case-level priority)",
        "type": "Accessibility / UI",
        "trace": "Scenario: Verify UI responsiveness and accessibility",
        "preconditions": "Agreed login environment and approved accessibility criteria/assistive technology are available.",
        "data": "D-A11Y-01: Approved accessibility standard, browser, assistive technology, and test procedure; not specified in the ticket.",
        "steps": [
            ("Navigate the login page using the approved keyboard-only procedure.", "Record the focus sequence and focus presentation for both new options."),
            ("Inspect the accessible names and roles of the SSO and Passkey controls with the approved assistive technology.", "Record the names/roles exposed for both controls."),
            ("Compare observations with the approved accessibility criteria.", "Pass/fail result is based on the confirmed standard; the ticket does not name a standard or detailed accessibility criteria."),
        ],
        "overall": "Accessibility observations are captured; conformance cannot be declared until the standard and acceptance thresholds are confirmed.",
        "notes": "Do not treat an unprovided standard or focus order as an agreed Jira requirement.",
        "cleanup": "Return to the login page and close assistive technology if required.",
    },
    {
        "id": "TC-V4-1-004",
        "title": "Authenticate successfully with a configured SSO identity provider",
        "priority": "High (provisional; confirm case-level priority)",
        "type": "Functional / Authentication",
        "trace": "Scenario: Validate successful login via SSO; AC: SSO Login Flow",
        "preconditions": "V4-1 is available in the agreed environment; a valid test identity and configured SSO provider are available.",
        "data": "D-SSO-VALID: Provider and valid staging identity supplied securely by the identity-provider owner; do not record credentials in this document or logs.",
        "steps": [
            ("Open the agreed login page.", "The login page is displayed."),
            ("Select “Sign in using SSO.”", "The SSO sign-in flow is initiated; exact intermediate screens are not specified in the ticket."),
            ("Complete authentication using the approved valid test identity.", "The configured identity provider accepts the test identity."),
            ("Observe the resulting VWO page and authentication state.", "The user is successfully authenticated and redirected to the dashboard."),
        ],
        "overall": "A valid SSO identity authenticates successfully and the user is redirected to the dashboard.",
        "notes": "Dashboard route/URL, session evidence, provider names, and environment URL are not specified and require confirmation.",
        "cleanup": "Sign out using the approved procedure and revoke/expire test sessions as required.",
    },
    {
        "id": "TC-V4-1-005",
        "title": "Reject invalid SSO credentials with an appropriate error",
        "priority": "High (provisional; confirm case-level priority)",
        "type": "Negative / Authentication",
        "trace": "Scenario: Validate failed SSO login with incorrect credentials; AC: SSO Login Flow and Error Handling",
        "preconditions": "Agreed environment is available; an approved invalid/rejected SSO test identity or credential set is provided.",
        "data": "D-SSO-INVALID: Controlled invalid test identity/credentials from the identity-provider owner; never use or include real credentials.",
        "steps": [
            ("Open the agreed login page and select “Sign in using SSO.”", "The SSO sign-in flow is initiated."),
            ("Submit the approved invalid test identity/credentials through the configured test flow.", "The identity provider rejects the test authentication."),
            ("Observe the VWO login experience after the rejection.", "An appropriate error message is shown, as required by the ticket. Exact message text is not specified."),
        ],
        "overall": "Invalid SSO credentials produce an appropriate error. The ticket does not specify exact error copy or post-error navigation.",
        "notes": "Do not assume exact wording, retry behavior, or a particular redirect. Confirm those expectations with the product/identity-provider owner.",
        "cleanup": "End the test flow and clear the controlled test session using the approved procedure.",
    },
    {
        "id": "TC-V4-1-006",
        "title": "Show an appropriate error for failed SSO authentication",
        "priority": "High (provisional; confirm case-level priority)",
        "type": "Negative / Authentication",
        "trace": "AC: Error Handling — failed SSO authentication",
        "preconditions": "Agreed environment is available; an approved way to cause an SSO authentication failure is provided.",
        "data": "D-SSO-FAIL: Identity-provider rejection scenario supplied by the provider owner; mechanism not specified in the ticket.",
        "steps": [
            ("Open the login page and select “Sign in using SSO.”", "The SSO sign-in flow is initiated."),
            ("Run the approved failed-authentication scenario.", "The SSO authentication attempt fails."),
            ("Observe the message presented in the VWO login experience.", "An appropriate error message is displayed. The approved text and UI location must be confirmed."),
        ],
        "overall": "Failed SSO authentication is accompanied by an appropriate error message.",
        "notes": "Keep this distinct from invalid-credential testing if the agreed failure fixture exercises a different failure condition; do not invent provider failure modes.",
        "cleanup": "End the failed flow and reset the test identity if required.",
    },
    {
        "id": "TC-V4-1-007",
        "title": "Verify SSO across every configured identity provider",
        "priority": "High (provisional; confirm case-level priority)",
        "type": "Compatibility / Authentication",
        "trace": "Scenario: Validate successful login via SSO; AC: Compatibility — SSO across configured identity providers",
        "preconditions": "The owner supplies the complete configured identity-provider list and suitable approved test accounts.",
        "data": "D-SSO-MATRIX: One approved valid test identity and provider entry per configured identity provider; no provider list is present in the ticket.",
        "steps": [
            ("Obtain the confirmed configured-provider matrix.", "The provider list and test account mapping are available to the tester."),
            ("For each provider in the matrix, open the login page and select “Sign in using SSO.”", "The SSO flow can be initiated for that provider."),
            ("Authenticate with that provider's approved valid test identity.", "The provider accepts the approved identity."),
            ("Observe the VWO destination for each provider.", "The user is authenticated and redirected to the dashboard for each configured provider."),
        ],
        "overall": "SSO works across all configured identity providers. Execution remains incomplete until the complete provider list is supplied and each entry is tested.",
        "notes": "Provider configuration itself is explicitly out of scope; this case verifies compatibility with existing configured providers.",
        "cleanup": "Sign out and clean up each test session using the approved procedure.",
    },
    {
        "id": "TC-V4-1-008",
        "title": "Authenticate successfully with a registered passkey",
        "priority": "High (provisional; confirm case-level priority)",
        "type": "Functional / Authentication",
        "trace": "Scenario: Validate successful login via Passkey; AC: Passkey Login Flow",
        "preconditions": "Agreed environment and supported device/browser are available; test account already has a registered passkey.",
        "data": "D-PASSKEY-REGISTERED: Approved staging account with an existing registered passkey; enrollment is out of scope for V4-1.",
        "steps": [
            ("Open the agreed login page on the approved supported device/browser.", "The login page is displayed."),
            ("Select “Sign in with Passkey.”", "The passkey sign-in flow is initiated; exact prompt behavior is not specified in the ticket."),
            ("Complete verification using the account's registered test passkey.", "The registered passkey is available and verified."),
            ("Observe the resulting VWO page and authentication state.", "The user is logged in successfully and redirected to the dashboard."),
        ],
        "overall": "A registered and verified passkey authenticates the user and redirects to the dashboard.",
        "notes": "Use a passkey enrolled before this test; do not include passkey material or authentication secrets in evidence.",
        "cleanup": "Sign out and end the test session using the approved procedure. Do not alter passkey enrollment.",
    },
    {
        "id": "TC-V4-1-009",
        "title": "Show fallback or guidance when no passkey is registered",
        "priority": "High (provisional; confirm case-level priority)",
        "type": "Negative / Authentication",
        "trace": "Scenario: Validate behavior when no passkey is registered; AC: Passkey Login Flow",
        "preconditions": "Agreed environment and supported device/browser are available; test account has no registered passkey.",
        "data": "D-PASSKEY-NONE: Approved staging account verified by its owner to have no passkey; account setup details not supplied in the ticket.",
        "steps": [
            ("Open the login page and select “Sign in with Passkey.”", "The passkey sign-in flow is initiated."),
            ("Continue with the approved account that has no registered passkey.", "The account has no passkey available for verification."),
            ("Observe the resulting login experience.", "A fallback or guidance message is displayed, as required by the ticket. Exact copy and next action are not specified."),
        ],
        "overall": "A user with no available registered passkey receives fallback or guidance.",
        "notes": "Do not assume the fallback method, exact message, or required navigation; confirm with the feature owner.",
        "cleanup": "End the test flow. Do not enroll a passkey.",
    },
    {
        "id": "TC-V4-1-010",
        "title": "Show an appropriate error when passkey authentication fails",
        "priority": "High (provisional; confirm case-level priority)",
        "type": "Negative / Authentication",
        "trace": "AC: Error Handling — passkey authentication failure",
        "preconditions": "Supported test device/browser and an approved controlled passkey-verification failure procedure are available.",
        "data": "D-PASSKEY-FAIL: Test account/passkey and approved failure fixture; failure mechanism is not defined in the ticket.",
        "steps": [
            ("Open the login page and select “Sign in with Passkey.”", "The passkey sign-in flow is initiated."),
            ("Execute the approved controlled verification-failure procedure.", "Passkey verification fails."),
            ("Observe the resulting login experience.", "An appropriate passkey authentication error is displayed. Exact wording and recovery behavior are not specified."),
        ],
        "overall": "Passkey authentication failure displays an appropriate error message.",
        "notes": "Do not treat a user cancellation as equivalent to failed verification unless the owner confirms the expected behavior.",
        "cleanup": "End the test flow and reset the controlled test fixture if required.",
    },
    {
        "id": "TC-V4-1-011",
        "title": "Show an error for an unsupported passkey browser",
        "priority": "High (provisional; confirm case-level priority)",
        "type": "Compatibility / Negative",
        "trace": "Scenario: Validate behavior on unsupported browsers/devices; AC: Error Handling and Compatibility",
        "preconditions": "Product owner supplies a browser/device explicitly designated unsupported for passkeys.",
        "data": "D-UNSUPPORTED-BROWSER: Browser/version in the confirmed unsupported matrix; matrix is not specified in the ticket.",
        "steps": [
            ("Open the login page in the confirmed unsupported browser.", "The login page is displayed."),
            ("Select “Sign in with Passkey” if the control is available.", "The passkey attempt is made, or the absence of the option is recorded."),
            ("Observe the result.", "An unsupported-browser/device error message is provided as required. Whether the option is hidden or disabled is not specified."),
        ],
        "overall": "The unsupported passkey browser/device condition is handled with the required error/guidance; presentation and copy need confirmation.",
        "notes": "The ticket requires an error but does not state whether the control should be hidden, disabled, or remain selectable.",
        "cleanup": "Close the test browser session.",
    },
    {
        "id": "TC-V4-1-012",
        "title": "Show an error for an unsupported passkey device",
        "priority": "High (provisional; confirm case-level priority)",
        "type": "Compatibility / Negative",
        "trace": "Scenario: Validate behavior on unsupported browsers/devices; AC: Error Handling and Compatibility",
        "preconditions": "Product owner supplies a device explicitly designated unsupported for passkeys.",
        "data": "D-UNSUPPORTED-DEVICE: Device/OS combination in the confirmed unsupported matrix; matrix is not specified in the ticket.",
        "steps": [
            ("Open the login page on the confirmed unsupported device.", "The login page is displayed."),
            ("Select “Sign in with Passkey” if the control is available.", "The passkey attempt is made, or the absence of the option is recorded."),
            ("Observe the result.", "An unsupported-browser/device error message is provided as required. Whether the option is hidden or disabled is not specified."),
        ],
        "overall": "The unsupported passkey device condition is handled with the required error/guidance; presentation and copy need confirmation.",
        "notes": "The ticket does not enumerate unsupported devices or define how unsupported status is communicated.",
        "cleanup": "Close the test browser session.",
    },
    {
        "id": "TC-V4-1-013",
        "title": "Verify passkey login across supported browser and device combinations",
        "priority": "High (provisional; confirm case-level priority)",
        "type": "Compatibility / Authentication",
        "trace": "Scenario: Validate successful login via Passkey; AC: Compatibility — supported browsers/devices",
        "preconditions": "The product owner supplies the complete supported browser/device matrix; registered test passkey account is available for each required setup.",
        "data": "D-PASSKEY-MATRIX: Approved test account/passkey and each supported browser/device combination from the product matrix.",
        "steps": [
            ("Obtain the confirmed supported browser/device matrix.", "The supported combinations and required versions are documented for execution."),
            ("For each combination, open the login page and select “Sign in with Passkey.”", "The login page is displayed and passkey sign-in can be initiated."),
            ("Verify using the approved registered passkey.", "The passkey is accepted on that supported combination."),
            ("Observe the resulting page.", "The user is logged in and redirected to the dashboard for each tested supported combination."),
        ],
        "overall": "Passkey login works on the supported browsers/devices. Coverage cannot be complete until the supported matrix is confirmed.",
        "notes": "Do not infer browser names, minimum versions, device models, or OS versions.",
        "cleanup": "Sign out and end sessions using the approved procedure.",
    },
    {
        "id": "TC-V4-1-014",
        "title": "Verify each authentication flow uses its configured secure protocol",
        "priority": "High (provisional; confirm case-level priority)",
        "type": "Security",
        "trace": "AC: Security — secure OAuth/SAML/WebAuthn protocols",
        "preconditions": "Security owner identifies the configured protocol for each flow and approves staging validation method and evidence handling.",
        "data": "D-SEC-PROTOCOL: Approved flow-to-protocol mapping and sanitized staging diagnostics; exact provider/protocol mapping is not specified.",
        "steps": [
            ("Obtain the approved SSO and Passkey protocol mapping.", "Expected protocol is identified for each configured authentication flow."),
            ("Exercise the approved SSO login flow in staging and inspect approved, sanitized diagnostics.", "Evidence can be compared with the confirmed SSO protocol requirement without exposing credentials."),
            ("Exercise the approved Passkey login flow in staging and inspect approved, sanitized diagnostics.", "Evidence can be compared with the confirmed WebAuthn protocol requirement without exposing passkey material."),
            ("Compare each observed flow with the approved mapping.", "SSO uses its configured OAuth/SAML protocol and Passkey uses WebAuthn, as applicable to the documented design."),
        ],
        "overall": "Authentication flows follow the applicable secure protocol (OAuth/SAML/WebAuthn) specified in the approved design.",
        "notes": "Ticket names possible protocols but does not map providers to protocols or specify cryptographic/configuration checks. Security owner must define the test oracle.",
        "cleanup": "Securely discard only approved temporary evidence according to the organization's handling policy.",
    },
    {
        "id": "TC-V4-1-015",
        "title": "Confirm sensitive authentication data is not exposed in the UI",
        "priority": "High (provisional; confirm case-level priority)",
        "type": "Security",
        "trace": "AC: Security — no sensitive data exposed in UI",
        "preconditions": "Approved staging test identities and a safe procedure for inspecting UI/error states are available.",
        "data": "D-SEC-UI: Synthetic/approved test identities; no real user secrets or secret values are included in this case document.",
        "steps": [
            ("Execute approved successful and failed SSO test paths.", "The SSO UI and error states are available for inspection."),
            ("Execute approved successful and failed Passkey test paths.", "The Passkey UI and error states are available for inspection."),
            ("Inspect rendered pages and messages for sensitive authentication values.", "No sensitive authentication data is exposed in the UI, as required by the ticket."),
        ],
        "overall": "No sensitive authentication data is exposed in the UI.",
        "notes": "The organization/security owner must define the sensitive-data classification and safe evidence procedure; do not copy any secret into reports.",
        "cleanup": "Remove any approved temporary screenshots using the organization's evidence-handling policy.",
    },
    {
        "id": "TC-V4-1-016",
        "title": "Confirm sensitive authentication data is not exposed in network logs",
        "priority": "High (provisional; confirm case-level priority)",
        "type": "Security",
        "trace": "AC: Security — no sensitive data exposed in network logs",
        "preconditions": "Security owner approves staging diagnostics, access permissions, and a sanitized inspection procedure.",
        "data": "D-SEC-LOGS: Approved sanitized network-log evidence; log locations and sensitive-field classification are not specified.",
        "steps": [
            ("Execute approved SSO and Passkey authentication paths using approved test accounts.", "The authentication flows generate evidence in the approved staging environment."),
            ("Inspect authorized, sanitized network-log evidence.", "Evidence is inspected without exporting or retaining raw credentials or passkey material."),
            ("Compare observed fields with the approved sensitive-data classification.", "No sensitive authentication data is exposed in network logs, as required by the ticket."),
        ],
        "overall": "No sensitive authentication data is exposed in network logs.",
        "notes": "Do not record, copy, or attach raw network traffic containing secrets. Log sources, classification, and safe evidence method require security-owner confirmation.",
        "cleanup": "Securely discard temporary evidence under the organization's approved handling policy.",
    },
]


def build():
    doc = SimpleDocTemplate(
        str(OUTPUT),
        pagesize=A4,
        leftMargin=18 * mm,
        rightMargin=18 * mm,
        topMargin=16 * mm,
        bottomMargin=19 * mm,
        title="V4-1 Test Cases - Draft for Review",
        author="VWO Quality Engineering",
        subject="Detailed test cases based on live Jira issue V4-1",
    )

    story = [
        para("TEST CASES — V4-1", "DocTitle"),
        para(
            "[VWO] Add Passkey and SSO Login Options to VWO Login Page",
            "Subtitle",
        ),
        info_table(
            [
                ("Source", "Live Jira issue V4-1; type: Story; status: To Do"),
                ("Ticket priority", "Medium (as returned by Jira; individual case priorities below are provisional)"),
                ("Template", "testcase_writer_skill_a/references/test-case-template.md"),
                ("Environment", "Not specified in the issue; confirm the staging URL and build before execution."),
                ("Prepared", datetime.now().astimezone().strftime("%d %b %Y")),
                ("Document status", "Final draft for human review; not approved or executed"),
            ]
        ),
        Spacer(1, 3 * mm),
        Paragraph("How to use this draft", STYLES["Section"]),
        para(
            "Each case follows the supplied template fields: ID, title, priority, type, preconditions, "
            "steps, expected result, and notes. Every step has its own observable expected result. "
            "Traceability points to the issue's listed scenario and/or acceptance-criteria area."
        ),
        para(
            "Case-level High/Medium priorities are proposed for planning only; the Jira issue supplies "
            "only an overall Medium priority. No concrete credentials, passkey material, or secret test "
            "values are included. Test-data identifiers refer to secure test fixtures that must be supplied "
            "by the relevant owners."
        ),
        para(
            "Where the issue does not state an exact message, route, browser matrix, viewport, accessibility "
            "standard, provider list, protocol mapping, or security evidence procedure, the case marks the "
            "expected result or execution threshold for confirmation rather than inventing one."
        ),
        Paragraph("In-scope acceptance criteria", STYLES["Section"]),
        info_table(
            [
                ("UI Visibility", "Show “Sign in using SSO” and “Sign in with Passkey” below “Sign in with Google”."),
                ("SSO Login Flow", "Valid SSO credentials authenticate and redirect to the dashboard; invalid credentials show appropriate errors."),
                ("Passkey Login Flow", "A registered, verified passkey logs in and redirects to the dashboard; no passkey gives fallback/guidance."),
                ("Error Handling", "Appropriate errors for failed SSO, failed Passkey authentication, and unsupported passkey browser/device."),
                ("Compatibility", "Passkey works on supported browsers/devices; SSO works across all configured identity providers."),
                ("Security", "Use secure OAuth/SAML/WebAuthn protocols; no sensitive data in UI or network logs."),
                ("Out of scope", "Passkey registration and SSO provider configuration are excluded by the issue."),
            ]
        ),
        Spacer(1, 2 * mm),
        Paragraph("Test cases", STYLES["Section"]),
    ]
    for case in CASES:
        story.extend(make_case(case))

    story.extend(
        [
            PageBreak(),
            Paragraph("Open questions and execution blockers", STYLES["Section"]),
            para(
                "The following details are absent from the Jira issue and must be confirmed before "
                "a definitive pass/fail oracle or complete execution is possible:"
            ),
        ]
    )
    blockers = [
        "Staging URL, deployed build/version, and supported test environment.",
        "Complete configured SSO provider list; approved test identities and invalid-credential/failure fixtures for each provider.",
        "Complete passkey-supported and unsupported browser/device/version matrix, plus test accounts that already have a passkey or are confirmed not to have one.",
        "Exact expected error messages, error placement, and expected recovery/navigation behavior for SSO failure, passkey failure, no passkey, and unsupported environments.",
        "Canonical dashboard destination/URL and the observable criterion for successful authentication.",
        "Responsive viewport/device matrix and measurable layout acceptance criteria.",
        "Accessibility standard, required assistive technologies, and pass/fail criteria.",
        "Protocol mapping for configured SSO providers and approved security-validation method.",
        "Sensitive-data classification, authorized network-log sources, and safe sanitized evidence procedure.",
        "Confirmation that registration and provider configuration are already available in staging; both are explicitly out of scope here.",
    ]
    for item in blockers:
        story.append(para("- " + item))

    story.extend(
        [
            Paragraph("Coverage and limits", STYLES["Section"]),
            para(
                f"This draft contains {len(CASES)} cases. It covers the ticket's listed scenarios and all "
                "stated acceptance-criteria areas. A coverage claim does not imply execution or approval. "
                "No test results are recorded in this document."
            ),
            Paragraph("HUMAN REVIEW GATE — APPROVAL REQUIRED", STYLES["Section"]),
            para(
                "Review the test data references, provisional case priorities, open questions, and "
                "unconfirmed expected results. Provide the missing environment and product/security "
                "criteria, then approve or edit these cases before they enter the test suite or are used "
                "for automation. This draft is not final sign-off.",
            ),
        ]
    )

    doc.build(story, onFirstPage=page_chrome, onLaterPages=page_chrome)
    return OUTPUT


if __name__ == "__main__":
    print(build())
