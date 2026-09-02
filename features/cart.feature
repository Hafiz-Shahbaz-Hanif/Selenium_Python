@saucedemo @cart
Feature: SauceDemo shopping cart
  As a signed-in shopper
  I want my cart to reflect what I added
  So that I can review it before checkout

  Background:
    Given I am signed in to SauceDemo as the standard user

  @smoke
  Scenario: A product added on the catalogue appears in the cart
    When I add "Sauce Labs Backpack" to the cart
    And I open the cart
    Then the cart lists "Sauce Labs Backpack"
    And the cart has 1 item

  Scenario Outline: "<product>" added on the catalogue is listed in the cart
    When I add "<product>" to the cart
    And I open the cart
    Then the cart lists "<product>"

    Examples:
      | product                           |
      | Sauce Labs Backpack               |
      | Sauce Labs Bike Light             |
      | Sauce Labs Bolt T-Shirt           |
      | Sauce Labs Fleece Jacket          |
      | Sauce Labs Onesie                 |
      | Test.allTheThings() T-Shirt (Red) |

  Scenario Outline: Removing "<product>" from the cart empties it
    Given my cart contains:
      | product   |
      | <product> |
    When I remove "<product>" from the cart
    Then the cart is empty

    Examples:
      | product                           |
      | Sauce Labs Backpack               |
      | Sauce Labs Bike Light             |
      | Sauce Labs Bolt T-Shirt           |
      | Sauce Labs Fleece Jacket          |
      | Sauce Labs Onesie                 |
      | Test.allTheThings() T-Shirt (Red) |

  Scenario: Continue shopping returns to the catalogue
    When I add "Sauce Labs Backpack" to the cart
    And I open the cart
    And I continue shopping
    Then the catalogue page is shown

  Scenario: Cart prices match the catalogue
    Given my cart contains:
      | product                  |
      | Sauce Labs Backpack      |
      | Sauce Labs Fleece Jacket |
      | Sauce Labs Onesie        |
    Then every cart price matches the catalogue

  Scenario: The cart holds several products at once
    Given my cart contains:
      | product                           |
      | Sauce Labs Backpack               |
      | Sauce Labs Bike Light             |
      | Sauce Labs Bolt T-Shirt           |
      | Sauce Labs Fleece Jacket          |
      | Sauce Labs Onesie                 |
      | Test.allTheThings() T-Shirt (Red) |
    Then the cart has 6 items
