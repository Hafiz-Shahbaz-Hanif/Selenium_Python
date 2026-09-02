@saucedemo @login
Feature: SauceDemo authentication
  As a shopper
  I want to sign in to the store
  So that I can browse and buy products

  Background:
    Given the SauceDemo login page is open

  @smoke
  Scenario: Standard user signs in successfully
    When I sign in as the standard user
    Then the inventory page is displayed

  Scenario Outline: "<username>" can sign in and reach the catalogue
    When I sign in as "<username>"
    Then the inventory page is displayed

    Examples:
      | username                |
      | standard_user           |
      | problem_user            |
      | performance_glitch_user |
      | error_user              |
      | visual_user             |

  Scenario Outline: Sign in is rejected for bad input
    When I sign in with username "<username>" and password "<password>"
    Then I see the login error "<message>"

    Examples:
      | username        | password       | message                                                     |
      | locked_out_user | secret_sauce   | Sorry, this user has been locked out.                        |
      | standard_user   | wrong_password | Username and password do not match any user in this service  |
      | standard_user   | secret         | Username and password do not match any user in this service  |
      |                 | secret_sauce   | Username is required                                         |
      | standard_user   |                | Password is required                                        |

  Scenario: Signing out returns to the login page
    When I sign in as the standard user
    And I log out
    Then the login page is shown
