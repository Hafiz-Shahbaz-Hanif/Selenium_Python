from behave import given, then, when
from hamcrest import assert_that, close_to, contains_string, is_in

from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from utils.products import price_of

DETAILS = ("Hafiz", "QA", "54000")
TAX_RATE = 0.08


def _checkout(context) -> CheckoutPage:
    if not getattr(context, "checkout_page", None):
        context.checkout_page = CheckoutPage(context.driver)
    return context.checkout_page


@given('my cart contains only "{product}"')
def cart_one_product(context, product):
    context.inventory_page.add_to_cart(product)
    context.inventory_page.go_to_cart()
    context.cart_page = CartPage(context.driver)
    context.cart_page.wait_until_loaded()
    context.bought_products = [product]


@when('I check out with details "{first}", "{last}", "{postal}"')
def checkout_with_details(context, first, last, postal):
    context.cart_page.checkout()
    context.checkout_page = CheckoutPage(context.driver)
    context.checkout_page.fill_information(first, last, postal)


@when("I check out with valid details")
def checkout_valid(context):
    checkout_with_details(context, *DETAILS)


@when("I finish the order")
def finish_order(context):
    _checkout(context).finish()


@then('I see the confirmation "{message}"')
def see_confirmation(context, message):
    assert_that(_checkout(context).confirmation_message(), contains_string(message))


@then("the order is confirmed")
def order_confirmed(context):
    assert_that(
        _checkout(context).confirmation_message(),
        contains_string("Thank you for your order!"),
    )


@when("I proceed to checkout without entering details")
def checkout_no_details(context):
    context.cart_page.checkout()
    context.checkout_page = CheckoutPage(context.driver)
    context.checkout_page.continue_without_details()


@when(
    'I proceed to checkout and continue with first "{first:Optional}", '
    'last "{last:Optional}", postal "{postal:Optional}"'
)
def checkout_partial(context, first, last, postal):
    context.cart_page.checkout()
    context.checkout_page = CheckoutPage(context.driver)
    context.checkout_page.wait_until_information_step()
    if first:
        context.checkout_page.type(CheckoutPage.FIRST_NAME, first)
    if last:
        context.checkout_page.type(CheckoutPage.LAST_NAME, last)
    if postal:
        context.checkout_page.type(CheckoutPage.POSTAL_CODE, postal)
    context.checkout_page.continue_without_details()


@then('I see the checkout error "{message}"')
def checkout_error(context, message):
    assert_that(_checkout(context).error_message(), contains_string(message))


@then("the tax is 8% of the subtotal")
def tax_is_8_percent(context):
    page = _checkout(context)
    assert_that(page.tax(), close_to(round(page.subtotal() * TAX_RATE, 2), 0.01))


@then("the total is the subtotal plus tax")
def total_is_subtotal_plus_tax(context):
    page = _checkout(context)
    assert_that(page.displayed_total(), close_to(page.subtotal() + page.tax(), 0.01))


@then("the subtotal equals the catalogue price of the ordered products")
def subtotal_matches_catalogue(context):
    expected = round(sum(price_of(p) for p in context.bought_products), 2)
    assert_that(_checkout(context).subtotal(), close_to(expected, 0.01))


@then('the checkout overview lists "{product}"')
def overview_lists(context, product):
    assert_that(product, is_in(_checkout(context).overview_item_names()))


@when("I cancel on the information step")
def cancel_info(context):
    context.cart_page.checkout()
    context.checkout_page = CheckoutPage(context.driver)
    context.checkout_page.wait_until_information_step()
    context.checkout_page.cancel_information_step()


@when("I cancel on the overview step")
def cancel_overview(context):
    context.cart_page.checkout()
    context.checkout_page = CheckoutPage(context.driver)
    context.checkout_page.fill_information(*DETAILS)
    context.checkout_page.cancel_overview_step()


@then("the cart page is shown")
def cart_page_shown(context):
    assert_that(context.driver.current_url, contains_string("cart.html"))


@then("the catalogue is shown")
def catalogue_is_shown(context):
    assert_that(context.driver.current_url, contains_string("inventory.html"))
