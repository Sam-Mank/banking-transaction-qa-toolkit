from pathlib import Path

from playwright.sync_api import Page, expect


DEMO_PAGE = Path(__file__).with_name("ui_demo.html")


def test_active_account_shows_demo_approval(page: Page) -> None:
    page.goto(DEMO_PAGE.as_uri())

    page.get_by_label("Transaction ID").fill("TX-DEMO-001")
    page.get_by_label("Amount").fill("125.50")
    page.get_by_label("Account").select_option("active")
    page.get_by_role("button", name="Validate transaction").click()

    expect(page.get_by_role("status")).to_have_text(
        "Demo transaction TX-DEMO-001 approved for £125.50. No transaction was saved."
    )


def test_amount_over_limit_is_rejected(page: Page) -> None:
    page.goto(DEMO_PAGE.as_uri())

    page.get_by_label("Transaction ID").fill("TX-DEMO-002")
    page.get_by_label("Amount").fill("5000.01")
    page.get_by_role("button", name="Validate transaction").click()

    expect(page.get_by_role("status")).to_have_text(
        "Amount exceeds the demo limit of 5000."
    )


def test_inactive_account_is_rejected(page: Page) -> None:
    page.goto(DEMO_PAGE.as_uri())

    page.get_by_label("Transaction ID").fill("TX-DEMO-003")
    page.get_by_label("Amount").fill("25.00")
    page.get_by_label("Account").select_option("inactive")
    page.get_by_role("button", name="Validate transaction").click()

    expect(page.get_by_role("status")).to_have_text(
        "The selected demo account is inactive."
    )