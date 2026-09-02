from behave import then, when
from hamcrest import assert_that, close_to, equal_to, is_in

from pages.cart_page import CartPage
from utils.products import price_of


@then("{count:d} products are listed")
def products_listed(context, count):
    assert_that(context.inventory_page.item_count(), equal_to(count))


@when('I sort the products by "{order}"')
def sort_products(context, order):
    context.inventory_page.sort_by(order)


@then('the products are ordered by "{order}"')
def products_ordered(context, order):
    order = order.strip().lower()
    if order.startswith("name"):
        actual = context.inventory_page.product_names()
        expected = sorted(actual, reverse="z to a" in order)
    else:
        actual = context.inventory_page.product_prices()
        expected = sorted(actual, reverse="high to low" in order)
    assert_that(actual, equal_to(expected))


@when('I add "{product}" to the cart')
def add_to_cart(context, product):
    context.inventory_page.add_to_cart(product)


@when('I remove "{product}" from the cart on the catalogue')
def remove_from_cart_catalogue(context, product):
    context.inventory_page.remove_from_cart(product)


@then("the cart badge shows {count:d}")
def cart_badge(context, count):
    assert_that(context.inventory_page.cart_count(), equal_to(count))


@then("the cart badge is empty")
def cart_badge_empty(context):
    assert_that(context.inventory_page.cart_count(), equal_to(0))


@then('the cart contains "{product}"')
def cart_contains(context, product):
    context.inventory_page.go_to_cart()
    assert_that(product, is_in(CartPage(context.driver).item_names()))


@then('the "{product}" catalogue button reads "{label}"')
def catalogue_button_label(context, product, label):
    assert_that(context.inventory_page.button_label_for(product), equal_to(label))


@then('the shelf price of "{product}" matches the catalogue')
def shelf_price_matches(context, product):
    assert_that(context.inventory_page.price_of(product), close_to(price_of(product), 0.001))


@when("I reset the app state")
def reset_app_state(context):
    context.inventory_page.reset_app_state()
