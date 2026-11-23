from playwright.sync_api import Page, expect
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage


def test_valid_login(page: Page):
    """Verify a standard user can log in and view the product inventory."""
    login_page = LoginPage(page)
    inventory_page = InventoryPage(page)

    login_page.navigate()
    login_page.login("standard_user", "secret_sauce")

    expect(page).to_have_url("https://www.saucedemo.com/inventory.html")
    expect(inventory_page.page_title).to_have_text("Products")


def test_locked_out_user_login(page: Page):
    """Verify appropriate error handling when a locked-out user attempts to log in."""
    login_page = LoginPage(page)

    login_page.navigate()
    login_page.login("locked_out_user", "secret_sauce")

    expect(login_page.error_message).to_be_visible()
    expect(login_page.error_message).to_contain_text("Sorry, this user has been locked out.")


def test_invalid_credentials(page: Page):
    """Verify error message when submitting wrong password."""
    login_page = LoginPage(page)

    login_page.navigate()
    login_page.login("standard_user", "wrong_password_123")

    expect(login_page.error_message).to_be_visible()
    expect(login_page.error_message).to_contain_text("Username and password do not match")


def test_add_item_to_cart(page: Page):
    """Verify adding an item updates the shopping cart badge count."""
    login_page = LoginPage(page)
    inventory_page = InventoryPage(page)

    login_page.navigate()
    login_page.login("standard_user", "secret_sauce")
    inventory_page.add_backpack_to_cart()

    expect(inventory_page.cart_badge).to_have_text("1")