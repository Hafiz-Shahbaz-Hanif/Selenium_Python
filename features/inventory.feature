@saucedemo @inventory
Feature: SauceDemo product catalogue
  As a signed-in shopper
  I want to sort products and add them to my cart
  So that I can decide what to buy

  Background:
    Given I am signed in to SauceDemo as the standard user

  @smoke
  Scenario: The catalogue lists all products
    Then 6 products are listed

  Scenario Outline: Products can be sorted
    When I sort the products by "<order>"
    Then the products are ordered by "<order>"

    Examples:
      | order                |
      | Name (A to Z)        |
      | Name (Z to A)        |
      | Price (low to high)  |
      | Price (high to low)  |

  Scenario: Adding products updates the cart badge
    When I add "Sauce Labs Backpack" to the cart
    And I add "Sauce Labs Bike Light" to the cart
    Then the cart badge shows 2
    And the cart contains "Sauce Labs Backpack"
