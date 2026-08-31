from behave import given

from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage


@given("I am signed in to SauceDemo as the standard user")
def signed_in(context):
    LoginPage(context.driver).open().login_as_standard_user()
    context.inventory_page = InventoryPage(context.driver)
    context.inventory_page.wait_until_loaded()
