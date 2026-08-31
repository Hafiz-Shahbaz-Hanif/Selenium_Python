from behave import given, then, when
from hamcrest import assert_that, contains_string, equal_to

from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage


@given("my cart contains")
def seed_cart(context):
    for row in context.table:
        context.inventory_page.add_to_cart(row["product"])
    context.inventory_page.go_to_cart()
    context.cart_page = CartPage(context.driver)
    context.cart_page.wait_until_loaded()
    assert_that(context.cart_page.item_count(), equal_to(len(context.table.rows)))


@when('I check out with details "{first}", "{last}", "{postal}"')
def checkout_with_details(context, first, last, postal):
    context.cart_page.checkout()
    context.checkout_page = CheckoutPage(context.driver)
    context.checkout_page.fill_information(first, last, postal)


@when("I finish the order")
def finish_order(context):
    context.checkout_page.finish()


@then('I see the confirmation "{message}"')
def see_confirmation(context, message):
    assert_that(context.checkout_page.confirmation_message(), contains_string(message))


@when("I proceed to checkout without entering details")
def checkout_no_details(context):
    context.cart_page.checkout()
    context.checkout_page = CheckoutPage(context.driver)
    context.checkout_page.continue_without_details()


@then('I see the checkout error "{message}"')
def checkout_error(context, message):
    assert_that(context.checkout_page.error_message(), contains_string(message))
