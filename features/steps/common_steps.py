from behave import given

from config.config import CONFIG
from pages.cart_page import CartPage
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage


def _sign_in(context, username: str) -> None:
    LoginPage(context.driver).open().login_expecting_inventory(
        username, CONFIG.saucedemo_password
    )
    context.inventory_page = InventoryPage(context.driver)
    context.inventory_page.wait_until_loaded()


@given("I am signed in to SauceDemo as the standard user")
def signed_in_standard(context):
    _sign_in(context, CONFIG.saucedemo_user)


@given('I am signed in to SauceDemo as "{username}"')
def signed_in_as(context, username):
    _sign_in(context, username)


@given("my cart contains")
def seed_cart(context):
    context.bought_products = [row["product"] for row in context.table]
    for product in context.bought_products:
        context.inventory_page.add_to_cart(product)
    context.inventory_page.go_to_cart()
    context.cart_page = CartPage(context.driver)
    context.cart_page.wait_until_loaded()
