from behave import given, then, when
from hamcrest import assert_that, close_to, equal_to, greater_than

from pages.product_page import ProductPage
from utils.products import price_of


@when('I open the "{product}" product page')
@given('I am on the "{product}" product page')
def open_product(context, product):
    context.inventory_page.open_product(product)
    context.product_page = ProductPage(context.driver)
    context.product_page.wait_until_loaded()
    context.current_product = product


@then("the product page shows that product's name")
def product_page_name(context):
    assert_that(context.product_page.name(), equal_to(context.current_product))


@then("the product page shows the catalogue price")
def product_page_price(context):
    assert_that(context.product_page.price(), close_to(price_of(context.current_product), 0.001))


@then("the product page shows a non-empty description")
def product_page_description(context):
    assert_that(len(context.product_page.description()), greater_than(0))


@when("I add the product to the cart from its page")
def add_from_product_page(context):
    context.product_page.add_to_cart()


@then('the product page button reads "{label}"')
def product_page_button(context, label):
    assert_that(context.product_page.button_label(), equal_to(label))


@then("the product page cart badge shows {count:d}")
def product_page_badge(context, count):
    assert_that(context.product_page.cart_count(), equal_to(count))


@when("I go back to the catalogue")
def back_to_catalogue(context):
    context.product_page.back_to_products()


@then("the catalogue is displayed")
def catalogue_displayed(context):
    context.inventory_page.wait_until_loaded()
    assert_that(context.inventory_page.item_count(), equal_to(6))
