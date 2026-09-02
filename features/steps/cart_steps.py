from behave import then, when
from hamcrest import assert_that, contains_string, equal_to, is_in

from pages.cart_page import CartPage
from utils.products import price_of


def _cart(context) -> CartPage:
    if not getattr(context, "cart_page", None):
        context.cart_page = CartPage(context.driver)
    return context.cart_page


@when("I open the cart")
def open_cart(context):
    context.inventory_page.go_to_cart()
    context.cart_page = CartPage(context.driver)
    context.cart_page.wait_until_loaded()


@then('the cart lists "{product}"')
def cart_lists(context, product):
    assert_that(product, is_in(_cart(context).item_names()))


@then("the cart has {count:d} items")
@then("the cart has {count:d} item")
def cart_item_count(context, count):
    assert_that(_cart(context).item_count(), equal_to(count))


@then("the cart is empty")
def cart_empty(context):
    assert_that(_cart(context).item_count(), equal_to(0))


@when('I remove "{product}" from the cart')
def remove_from_cart(context, product):
    _cart(context).remove(product)


@when("I continue shopping")
def continue_shopping(context):
    _cart(context).continue_shopping()


@then("the catalogue page is shown")
def catalogue_shown(context):
    context.inventory_page.wait_until_loaded()
    assert_that(context.driver.current_url, contains_string("inventory.html"))


@then("every cart price matches the catalogue")
def cart_prices_match(context):
    cart = _cart(context)
    for name, price in zip(cart.item_names(), cart.item_prices()):
        assert_that(price, equal_to(price_of(name)))
