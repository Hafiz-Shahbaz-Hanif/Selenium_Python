@saucedemo @product
Feature: SauceDemo product detail page
  As a signed-in shopper
  I want to open a product
  So that I can read its details and add it to my cart

  Background:
    Given I am signed in to SauceDemo as the standard user

  @smoke
  Scenario: Opening a product shows its details
    When I open the "Sauce Labs Backpack" product page
    Then the product page shows that product's name
    And the product page shows the catalogue price
    And the product page shows a non-empty description

  Scenario Outline: The "<product>" page shows the right name, price and description
    When I open the "<product>" product page
    Then the product page shows that product's name
    And the product page shows the catalogue price
    And the product page shows a non-empty description

    Examples:
      | product                           |
      | Sauce Labs Backpack               |
      | Sauce Labs Bike Light             |
      | Sauce Labs Bolt T-Shirt           |
      | Sauce Labs Fleece Jacket          |
      | Sauce Labs Onesie                 |
      | Test.allTheThings() T-Shirt (Red) |

  Scenario Outline: Adding "<product>" to the cart from its page
    When I open the "<product>" product page
    And I add the product to the cart from its page
    Then the product page cart badge shows 1
    And the product page button reads "Remove"

    Examples:
      | product                           |
      | Sauce Labs Backpack               |
      | Sauce Labs Bike Light             |
      | Sauce Labs Bolt T-Shirt           |
      | Sauce Labs Fleece Jacket          |
      | Sauce Labs Onesie                 |
      | Test.allTheThings() T-Shirt (Red) |

  Scenario: Back to products returns to the catalogue
    When I open the "Sauce Labs Onesie" product page
    And I go back to the catalogue
    Then the catalogue is displayed
