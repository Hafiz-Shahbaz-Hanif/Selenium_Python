from behave import given, then, when
from hamcrest import assert_that, contains_string, equal_to, is_

from pages.orangehrm_dashboard_page import OrangeHrmDashboardPage
from pages.orangehrm_login_page import OrangeHrmLoginPage


@given("I am signed in to OrangeHRM as the administrator")
def signed_in_orangehrm(context):
    OrangeHrmLoginPage(context.driver).open().login_as_admin()
    context.dashboard = OrangeHrmDashboardPage(context.driver)
    context.dashboard.wait_until_loaded()


@when('I open the "{menu}" menu')
def open_menu(context, menu):
    context.dashboard.open_menu(menu)


@then('the "{title}" page is shown')
def page_shown(context, title):
    assert_that(context.dashboard.current_page_title(), contains_string(title))


@then('the "{menu}" menu is available')
def menu_available(context, menu):
    assert_that(context.dashboard.is_menu_present(menu), is_(True))


@when("I log out of OrangeHRM")
def logout_orangehrm(context):
    context.orangehrm = context.dashboard.logout()


@then("the OrangeHRM login page is shown")
def orangehrm_login_shown(context):
    assert_that(context.driver.current_url, contains_string("auth/login"))


@then("the OrangeHRM dashboard is shown")
def orangehrm_dashboard_shown(context):
    assert_that(context.dashboard.current_page_title(), equal_to("Dashboard"))
