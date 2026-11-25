from datetime import datetime
from html import escape
from io import BytesIO
from pathlib import Path

from PIL import Image as PILImage
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    Image,
    KeepTogether,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "01_advance_skills" / "testplan_creator_skill_a"
OUTPUT = Path(__file__).resolve().parent / "VWO-49_test_plan.pdf"
LOGO = SKILL_DIR / "misc" / "company.png"

NAVY = colors.HexColor("#0F2B46")
ORANGE = colors.HexColor("#F26B2C")
INK = colors.HexColor("#1F2A37")
MUTED = colors.HexColor("#5B6470")
PALE = colors.HexColor("#F3F6F8")
GRID = colors.HexColor("#D7DEE5")

STYLES = getSampleStyleSheet()
STYLES.add(
    ParagraphStyle(
        name="PlanTitle",
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
        name="PlanSubtitle",
        parent=STYLES["Normal"],
        fontName="Helvetica",
        fontSize=11,
        leading=15,
        textColor=MUTED,
        spaceAfter=12,
    )
)
STYLES.add(
    ParagraphStyle(
        name="SectionHeading",
        parent=STYLES["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=15,
        leading=19,
        textColor=NAVY,
        spaceBefore=13,
        spaceAfter=7,
        keepWithNext=True,
    )
)
STYLES.add(
    ParagraphStyle(
        name="SubHeading",
        parent=STYLES["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=11,
        leading=14,
        textColor=ORANGE,
        spaceBefore=7,
        spaceAfter=4,
        keepWithNext=True,
    )
)
STYLES.add(
    ParagraphStyle(
        name="PlanBody",
        parent=STYLES["BodyText"],
        fontName="Helvetica",
        fontSize=9.3,
        leading=13,
        textColor=INK,
        spaceAfter=5,
    )
)
STYLES.add(
    ParagraphStyle(
        name="PlanSmall",
        parent=STYLES["PlanBody"],
        fontSize=8,
        leading=10.5,
        spaceAfter=2,
    )
)
STYLES.add(
    ParagraphStyle(
        name="TableHead",
        parent=STYLES["PlanSmall"],
        fontName="Helvetica-Bold",
        textColor=colors.white,
    )
)
STYLES.add(
    ParagraphStyle(
        name="ScenarioTitle",
        parent=STYLES["PlanBody"],
        fontName="Helvetica-Bold",
        fontSize=9.5,
        leading=12,
        textColor=NAVY,
        spaceBefore=5,
        spaceAfter=2,
        keepWithNext=True,
    )
)
STYLES.add(
    ParagraphStyle(
        name="ReviewGate",
        parent=STYLES["PlanBody"],
        fontName="Helvetica-Bold",
        fontSize=10,
        leading=14,
        textColor=NAVY,
    )
)


def p(text, style="PlanBody"):
    return Paragraph(escape(str(text)), STYLES[style])


def bullet(text):
    return Paragraph(
        f"- {escape(str(text))}",
        ParagraphStyle(
            name="BulletInline",
            parent=STYLES["PlanBody"],
            leftIndent=12,
            firstLineIndent=-8,
            spaceAfter=3,
        ),
    )


def header_cell(text):
    return p(text, "TableHead")


def body_cell(text):
    return p(text, "PlanSmall")


def section(title):
    return Paragraph(escape(title), STYLES["SectionHeading"])


def subsection(title):
    return Paragraph(escape(title), STYLES["SubHeading"])


def make_logo():
    with PILImage.open(LOGO) as source:
        image = source.convert("RGBA")
        buffer = BytesIO()
        image.save(buffer, format="PNG")
    buffer.seek(0)
    return Image(buffer, width=38 * mm, height=14 * mm, kind="proportional")


def page_chrome(canvas, doc):
    canvas.saveState()
    width, height = A4
    canvas.setStrokeColor(GRID)
    canvas.setLineWidth(0.5)
    canvas.line(18 * mm, 13 * mm, width - 18 * mm, 13 * mm)
    canvas.setFont("Helvetica", 7.5)
    canvas.setFillColor(MUTED)
    canvas.drawString(18 * mm, 8.5 * mm, "VWO Quality Engineering | VWO-49 | Draft for human review")
    canvas.drawRightString(width - 18 * mm, 8.5 * mm, f"Page {doc.page}")
    canvas.restoreState()


def add_scenario(story, case_id, priority, title, trace, steps, expected):
    story.append(
        KeepTogether(
            [
                Paragraph(
                    escape(f"{case_id} | {priority} | {title}"),
                    STYLES["ScenarioTitle"],
                ),
                p(f"Trace: {trace}", "PlanSmall"),
                p(f"Steps: {steps}", "PlanSmall"),
                p(f"Expected: {expected}", "PlanSmall"),
                Spacer(1, 2 * mm),
            ]
        )
    )


def build():
    if not LOGO.is_file():
        raise FileNotFoundError(f"Company logo not found: {LOGO}")

    doc = SimpleDocTemplate(
        str(OUTPUT),
        pagesize=A4,
        leftMargin=18 * mm,
        rightMargin=18 * mm,
        topMargin=16 * mm,
        bottomMargin=19 * mm,
        title="VWO-49 Test Plan - Passkey and SSO Login Options",
        author="VWO Quality Engineering",
        subject="Review-ready test plan based on Jira issue VWO-49",
    )
    story = []

    brand = Table(
        [[make_logo(), p("QUALITY ENGINEERING<br/>JIRA STORY TEST PLAN", "PlanSmall")]],
        colWidths=[48 * mm, 125 * mm],
    )
    brand.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("ALIGN", (1, 0), (1, 0), "RIGHT"),
                ("LINEBELOW", (0, 0), (-1, -1), 2, ORANGE),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ]
        )
    )
    story.extend(
        [
            brand,
            Spacer(1, 7 * mm),
            Paragraph("VWO-49 Test Plan", STYLES["PlanTitle"]),
            Paragraph(
                "[VWO] Add Passkey and SSO Login Options to VWO Login Page",
                STYLES["PlanSubtitle"],
            ),
        ]
    )

    metadata = [
        ("Issue / project", "VWO-49 / VWO Project"),
        ("Type / status", "Story / To Do (as recorded in the supplied Jira export)"),
        ("Ticket priority", "Medium in issue metadata; High is also stated in the description - clarification required"),
        ("Epic / owner", "Authentication Enhancements / Assignee unassigned"),
        ("Reporter / resolution", "Pramod / Unresolved"),
        ("Components / labels", "None / None"),
        ("Affects / fix versions", "None / None"),
        ("Created / updated", "19 Apr 2026 / 20 Oct 2026"),
        ("Sprint / estimates", "Not specified; estimates and time spent are not specified"),
        ("Prepared", datetime.now().astimezone().strftime("%d %b %Y")),
        ("Review status", "Draft only - not approved for execution or sign-off"),
    ]
    meta = Table(
        [
            [body_cell(label), body_cell(value)]
            for label, value in metadata
        ],
        colWidths=[42 * mm, 131 * mm],
        repeatRows=0,
    )
    meta.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (0, -1), PALE),
                ("GRID", (0, 0), (-1, -1), 0.4, GRID),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )
    story.extend([meta, Spacer(1, 3 * mm)])

    story.extend(
        [
            section("1. Scope and objectives"),
            p(
                "Validate the two new login choices - Sign in using SSO and Sign in with Passkey - "
                "on the VWO login page. Confirm visibility and placement, successful and unsuccessful "
                "authentication behavior, supported-environment behavior, and the security and usability "
                "expectations stated in VWO-49."
            ),
            p(
                "The story describes users signing in more securely and conveniently without relying "
                "solely on email/password authentication. The test plan is limited to the login options "
                "and related authentication outcomes described in the ticket."
            ),
            subsection("In scope"),
            bullet("Visibility, label, and placement of both options relative to Sign in with Google."),
            bullet("SSO success, failed authentication, configured-provider compatibility, and error handling."),
            bullet("Passkey success, missing passkey, authentication failure, unsupported browser/device, and guidance."),
            bullet("Responsive and accessibility checks, plus protocol and sensitive-data checks from the ticket."),
            subsection("Out of scope per ticket"),
            bullet("Passkey registration flow; the ticket says this is covered by a separate story."),
            bullet("SSO provider configuration."),
            section("2. Ticket requirements and traceability"),
        ]
    )

    requirements = [
        ("AC-01", "UI visibility", "Both buttons are visible below Sign in with Google.", "T01-T02"),
        ("AC-02", "SSO login", "Valid SSO authenticates and reaches the dashboard; invalid credentials show an appropriate error.", "T03-T06"),
        ("AC-03", "Passkey login", "A registered, verified passkey authenticates and reaches the dashboard; no passkey gives fallback guidance.", "T07-T10"),
        ("AC-04", "Error handling", "Show appropriate errors for SSO failure, passkey failure, and unsupported passkey environments.", "T05-T06, T09-T11"),
        ("AC-05", "Compatibility", "Passkey works on supported browsers/devices; SSO works across configured identity providers.", "T02, T06, T11-T12"),
        ("AC-06", "Security", "Use secure OAuth/SAML/WebAuthn flows; expose no sensitive data in UI or network logs.", "T13-T15"),
        ("NFR-01", "Usability", "Ticket lists responsive behavior and accessibility as test scenarios.", "T02, T16"),
    ]
    req_table = Table(
        [[header_cell("ID"), header_cell("Area"), header_cell("Ticket requirement"), header_cell("Scenarios")]]
        + [
            [body_cell(value) for value in row]
            for row in requirements
        ],
        colWidths=[15 * mm, 28 * mm, 99 * mm, 31 * mm],
        repeatRows=1,
        splitByRow=1,
    )
    req_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), NAVY),
                ("GRID", (0, 0), (-1, -1), 0.4, GRID),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, PALE]),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 5),
                ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )
    story.extend(
        [
            req_table,
            p(
                "Priority key (provisional): P0 = release-blocking authentication/security failure; "
                "P1 = core acceptance-criteria failure; P2 = lower-risk usability or compatibility issue. "
                "Confirm this scale and the ticket's conflicting Medium/High priority before execution.",
                "PlanSmall",
            ),
            section("3. Test scenarios"),
            p(
                "Use only approved staging accounts and identity-provider configuration. Do not place "
                "real passwords, passkey material, tokens, or other secrets in screenshots, test notes, "
                "or logs."
            ),
            subsection("Test approach"),
            bullet("Use positive and negative testing for SSO and Passkey authentication, with equivalence classes for valid, invalid, missing, and unsupported conditions."),
            bullet("Use state-transition checks for login, provider redirects, authenticator prompts, cancellation, errors, and dashboard access."),
            bullet("Use compatibility and responsive checks against the approved browser/device matrix; use keyboard and assistive-technology checks for the new controls."),
            bullet("Use security-focused validation for authentication outcomes and sensitive-data exposure, limited to approved staging diagnostics."),
        ]
    )

    scenarios = [
        ("T01", "P1", "New login options are visible and correctly ordered", "AC-01; historical blocked check TC-01", "Open the agreed login page at desktop width. Compare the Google, SSO, and Passkey controls and their labels.", "Both new controls are visible below Sign in with Google. The issue's earlier test expected SSO followed by Passkey; confirm that order is intended."),
        ("T02", "P1", "Buttons remain usable across layout and accessibility checks", "AC-01; NFR-01; ticket test scenarios", "Check approved desktop and mobile viewport sizes. Navigate to both controls using keyboard and inspect focus, accessible name, contrast, and activation.", "Controls remain visible, operable, distinguishable, and correctly positioned without overlap or clipping. Exact viewport/device support and accessibility target remain to be confirmed."),
        ("T03", "P1", "Successful SSO authentication reaches the dashboard", "AC-02; historical blocked check TC-02", "From the login page select SSO, authenticate using an approved valid staging identity, and observe the resulting page and session.", "User is authenticated and reaches the VWO dashboard. The ticket's historical test expected a URL containing /dashboard; confirm the canonical route."),
        ("T04", "P1", "Invalid SSO credentials are rejected with an appropriate error", "AC-02; historical blocked check TC-03", "Start SSO and use an approved invalid test identity or credentials in the staging IdP.", "Authentication is denied, a clear non-sensitive error is shown, and no authenticated dashboard session is created. Historical test data expected 'Invalid credentials'; confirm approved copy."),
        ("T05", "P1", "SSO provider error or unavailable response is handled", "AC-02, AC-04; gap-derived", "In staging, exercise an IdP rejection or controlled provider error using the approved test configuration.", "A safe, understandable error is shown; the user is not authenticated and can retry or return to login. Error copy and retry behavior need product confirmation."),
        ("T06", "P1", "SSO works with each configured identity provider", "AC-05", "Repeat the successful and rejected SSO paths for every configured provider in the approved staging environment.", "Each configured provider follows the expected flow and returns to the correct VWO state. Provider inventory and per-provider expectations must be supplied."),
        ("T07", "P1", "Registered passkey authenticates the user", "AC-03", "Use an approved account with an enrolled passkey on a supported browser/device; choose Passkey and complete verification.", "User is authenticated and reaches the dashboard without falling back to email/password."),
        ("T08", "P1", "Account without a registered passkey receives fallback guidance", "AC-03; historical blocked check TC-04", "Use an approved staging account with no registered passkey and select Passkey.", "No authenticated session is created; actionable fallback/guidance is displayed and the user remains able to use another permitted login method."),
        ("T09", "P1", "Failed passkey verification is handled safely", "AC-04", "On a supported device, initiate Passkey and use an approved negative test path such as user cancellation or verification failure.", "A suitable non-sensitive error or recovery guidance is shown; no session is granted. Confirm whether cancellation and verification failure use distinct UX."),
        ("T10", "P2", "User cancellation of passkey or SSO can recover", "Gap-derived from authentication UX", "Cancel the browser authenticator prompt and, separately, cancel/return from the configured SSO flow.", "The user is not authenticated, receives the agreed feedback, and can retry or choose another login method without a broken page."),
        ("T11", "P1", "Unsupported passkey environment gives a clear fallback", "AC-04, AC-05", "Open the login page in an approved unsupported browser/device configuration and select Passkey if the UI permits.", "Unsupported capability is detected or handled; clear guidance appears; no authentication is granted; other login options remain usable."),
        ("T12", "P1", "Passkey compatibility across supported environments", "AC-05", "Repeat T07 on each browser/device combination in the product-approved support matrix.", "Passkey succeeds on each supported combination. The support matrix and minimum versions must be provided before test execution."),
        ("T13", "P0", "Authentication exchange uses the approved secure protocol", "AC-06", "For approved staging flows, inspect the documented integration and sanitized browser/network evidence for the configured OAuth/SAML SSO and WebAuthn passkey exchanges.", "Each flow uses the approved secure protocol and transport; no secrets are exposed. Avoid capturing or retaining live credentials/assertions."),
        ("T14", "P0", "Sensitive authentication data is not exposed", "AC-06", "Inspect rendered UI, browser-visible errors, and approved sanitized network/application logs during positive and negative runs.", "Passwords, tokens, assertions, private key material, and other sensitive values do not appear in UI or logs. Logging locations and retention/access policy need confirmation."),
        ("T15", "P1", "Authentication failure never creates a dashboard session", "AC-02 to AC-04; security assertion", "After the negative SSO and Passkey cases, attempt to open the dashboard directly and inspect only approved session indicators.", "Failed or canceled authentication leaves no authenticated session; protected dashboard access is denied or redirected to login."),
        ("T16", "P2", "Login choices are accessible and responsive", "Ticket test scenarios; NFR-01", "Check keyboard-only operation, visible focus, accessible names/roles, reading order, zoom/reflow, and approved mobile widths.", "The new controls are understandable and operable without pointer-only interaction and remain usable at supported sizes. Confirm the required accessibility standard."),
    ]
    for scenario in scenarios:
        add_scenario(story, *scenario)

    story.extend(
        [
            section("4. Test data and environment"),
            subsection("Environment"),
            bullet("Jira lists app.vwo.com as the application URL in several run records; other records use https://app.wingify.com/#/login. Confirm the canonical staging URL and ensure the test environment is not production."),
            bullet("The ticket Definition of Done requires deployment to staging. Record build/version, browser/device, OS, locale, and identity-provider configuration for each run."),
            bullet("Use the approved support matrix for passkey-capable and unsupported browser/device combinations. The ticket does not enumerate versions or devices."),
            bullet("Use the configured SSO identity providers in staging; their names, protocols, and coverage order are not present in the export."),
            subsection("Required test accounts and data"),
            bullet("Staging account with a valid SSO identity for each configured provider."),
            bullet("Controlled invalid/rejected SSO identity or credentials approved by the identity-provider owner."),
            bullet("Staging account with a registered passkey and supported authenticator/device."),
            bullet("Staging account with no registered passkey, plus approved passkey failure/cancellation test paths."),
            bullet("No real secrets in evidence. Use the organization's approved secret-handling and log-access processes."),
            section("5. Risks, gaps, and questions for the author"),
        ]
    )

    gaps = [
        ("Priority conflict", "Jira metadata says Medium while the description says High. Which is authoritative? Confirm the P0/P1/P2 policy for this feature."),
        ("Order of buttons", "The acceptance criterion says both are below Google; earlier test notes expect SSO then Passkey. Is that the required order?"),
        ("Error wording", "The acceptance criteria require appropriate errors. Historical test notes expect the exact text 'Invalid credentials' for SSO. What exact user-facing messages are approved for SSO and Passkey failures?"),
        ("Success destination", "The story says dashboard; historical test notes expect a URL containing /dashboard. What is the canonical destination and expected post-login state?"),
        ("Identity providers", "Which SSO providers are configured for staging, and which SSO protocols/flows are in scope per provider?"),
        ("Passkey support", "Which browsers, device types, OS versions, and authenticator configurations are supported or unsupported?"),
        ("Cancellation and recovery", "What should happen after a user cancels an SSO redirect or browser passkey prompt? Should the error differ from an authentication failure?"),
        ("Security evidence", "Which sanitized network/application logs can QA inspect, and what sensitive fields must be redacted?"),
        ("Accessibility and responsive targets", "Which accessibility standard and viewport/device breakpoints are required?"),
        ("Scope and dependencies", "Passkey registration and SSO provider configuration are out of scope. Identify the prerequisite story/build/configuration and confirm both are ready in staging."),
        ("Historical execution", "The export records six automated runs (10, 13, 17, and 20 Oct 2026), each inconclusive with 0 passed, 0 failed, and 4 blocked. Actual-result fields are blank. What blocked execution, and are the environment and test accounts now available?"),
    ]
    for title, detail in gaps:
        story.append(bullet(f"{title}: {detail}"))
    story.append(
        p(
            "Risk summary: the login experience is an authentication boundary. A failure can prevent legitimate access, while incorrect failure handling or session creation can permit unauthorized access. The repeated blocked runs mean there is no recorded pass/fail evidence in this export; readiness, environments, and test identities are the main execution risks."
        )
    )

    story.extend(
        [
            section("6. Prior execution evidence from the Jira export"),
            p(
                "Six automated runs are recorded in comments dated 10, 13, 17, and 20 Oct 2026. "
                "Each reports INCONCLUSIVE: 0 passed, 0 failed, 4 blocked. The same four checks recur: "
                "button visibility/order, successful SSO redirect, failed SSO error, and no-passkey fallback. "
                "The actual-result fields are blank, so these records are not evidence that the feature passed or failed."
            ),
            p(
                "Recorded application addresses vary between app.vwo.com and app.wingify.com/#/login. "
                "The latest recorded run is 20 Oct 2026. Resolve the URL and blocked prerequisites before retesting."
            ),
            section("7. Entry and exit criteria"),
            subsection("Entry criteria"),
            bullet("Human review of this plan and resolution of blocking questions above."),
            bullet("VWO-49 is deployed to the agreed staging environment and build/version is recorded."),
            bullet("Configured SSO providers, supported passkey matrix, and test identities are available."),
            bullet("Passkey registration is already available for the test account (registration itself remains out of scope)."),
            bullet("Testers have approved access to sanitized diagnostics and know how to avoid recording secrets."),
            subsection("Exit criteria"),
            bullet("All approved P0/P1 scenarios have been executed with reproducible results and evidence."),
            bullet("P2 scenarios are executed or explicitly deferred with owner approval."),
            bullet("No unresolved critical/high defects remain, consistent with the Jira Definition of Done."),
            bullet("Authentication/security failures are triaged; blocked cases are recorded as blocked, never as passed."),
            bullet("Required feature documentation is updated."),
            bullet("Requirements, test results, defects, and any accepted risks are linked back to VWO-49."),
            section("8. Assumptions and limitations"),
            bullet("This plan is based on the local VWO-49 Jira export at resource/VWO-49.doc, not a live Jira API response; Jira credentials were not present in the current environment."),
            bullet("The supplied company-details file describes VWO as a Bingify product, states a company size of 5,000 employees, and describes its focus as A/B testing. This is included as supplied context and is not independently verified."),
            bullet("No test execution has been performed while preparing this plan. Historical blocked runs are reported as context only."),
            bullet("Scenario details beyond explicit acceptance criteria are marked gap-derived or provisional and require reviewer confirmation."),
            section("9. Human review gate - approval required"),
            p(
                "This is a review-ready draft, not a final or approved test plan. Confirm the priority, button order, exact errors, redirect destination, staging URL, provider inventory, browser/device support, diagnostic access, and blocked-run prerequisites. Approve or edit the plan before execution; do not treat any scenario as passed until it is run and evidenced.",
                "ReviewGate",
            ),
            Spacer(1, 3 * mm),
            p("Prepared for: VWO Product Quality Review | Source issue: VWO-49", "PlanSmall"),
        ]
    )

    doc.build(story, onFirstPage=page_chrome, onLaterPages=page_chrome)
    return OUTPUT


if __name__ == "__main__":
    print(build())
