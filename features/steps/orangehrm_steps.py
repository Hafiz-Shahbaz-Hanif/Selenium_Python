from behave import given, then, when
from hamcrest import assert_that, contains_string

from pages.orangehrm_dashboard_page import OrangeHrmDashboardPage
from pages.orangehrm_login_page import OrangeHrmLoginPage


@given("the OrangeHRM login page is open")
def open_orangehrm(context):
    context.orangehrm = OrangeHrmLoginPage(context.driver)
    context.orangehrm.open()


@when("I sign in to OrangeHRM as the administrator")
def orangehrm_admin(context):
    context.orangehrm.login_as_admin()
    context.dashboard = OrangeHrmDashboardPage(context.driver)


@when('I sign in to OrangeHRM with username "{username}" and password "{password}"')
def orangehrm_login(context, username, password):
    context.orangehrm.login(username, password)


@then("the OrangeHRM dashboard is displayed")
def orangehrm_dashboard(context):
    assert_that(context.dashboard.current_page_title(), contains_string("Dashboard"))


@then('I see the OrangeHRM error "{message}"')
def orangehrm_error(context, message):
    assert_that(context.orangehrm.error_message(), contains_string(message))
