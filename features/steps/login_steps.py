import parse
from behave import given, register_type, then, when
from hamcrest import assert_that, contains_string, equal_to

from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage


@parse.with_pattern(r'[^"]*')
def parse_optional(text: str) -> str:
    """A quoted value that is allowed to be empty (``""``)."""
    return text


register_type(Optional=parse_optional)


@given("the SauceDemo login page is open")
def open_login(context):
    context.login_page = LoginPage(context.driver)
    context.login_page.open()


@when("I sign in as the standard user")
def sign_in_standard(context):
    context.login_page.login_as_standard_user()


@when('I sign in with username "{username:Optional}" and password "{password:Optional}"')
def sign_in_with(context, username, password):
    context.login_page.login(username, password)


@then("the inventory page is displayed")
def inventory_displayed(context):
    inventory = InventoryPage(context.driver)
    inventory.wait_for_url_contains("/inventory.html")
    assert_that(inventory.item_count(), equal_to(6))


@then('I see the login error "{message}"')
def login_error(context, message):
    assert_that(context.login_page.error_message(), contains_string(message))
