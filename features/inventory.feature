@saucedemo @inventory
Feature: SauceDemo product catalogue
  As a signed-in shopper
  I want to browse, sort and add products
  So that I can decide what to buy

  Background:
    Given I am signed in to SauceDemo as the standard user

  @smoke
  Scenario: The catalogue lists all products
    Then 6 products are listed

  Scenario Outline: Products can be sorted by "<order>"
    When I sort the products by "<order>"
    Then the products are ordered by "<order>"

    Examples:
      | order               |
      | Name (A to Z)       |
      | Name (Z to A)       |
      | Price (low to high) |
      | Price (high to low) |

  Scenario Outline: Adding "<product>" from the catalogue updates the cart
    When I add "<product>" to the cart
    Then the cart badge shows 1
    And the "<product>" catalogue button reads "Remove"
    And the cart contains "<product>"

    Examples:
      | product                           |
      | Sauce Labs Backpack               |
      | Sauce Labs Bike Light             |
      | Sauce Labs Bolt T-Shirt           |
      | Sauce Labs Fleece Jacket          |
      | Sauce Labs Onesie                 |
      | Test.allTheThings() T-Shirt (Red) |

  Scenario Outline: Adding then removing "<product>" clears it from the cart
    When I add "<product>" to the cart
    And I remove "<product>" from the cart on the catalogue
    Then the cart badge is empty
    And the "<product>" catalogue button reads "Add to cart"

    Examples:
      | product                           |
      | Sauce Labs Backpack               |
      | Sauce Labs Bike Light             |
      | Sauce Labs Bolt T-Shirt           |
      | Sauce Labs Fleece Jacket          |
      | Sauce Labs Onesie                 |
      | Test.allTheThings() T-Shirt (Red) |

  Scenario Outline: The shelf price of "<product>" is correct
    Then the shelf price of "<product>" matches the catalogue

    Examples:
      | product                           |
      | Sauce Labs Backpack               |
      | Sauce Labs Bike Light             |
      | Sauce Labs Bolt T-Shirt           |
      | Sauce Labs Fleece Jacket          |
      | Sauce Labs Onesie                 |
      | Test.allTheThings() T-Shirt (Red) |

  Scenario: The cart badge accumulates as products are added
    When I add "Sauce Labs Backpack" to the cart
    And I add "Sauce Labs Bike Light" to the cart
    And I add "Sauce Labs Onesie" to the cart
    Then the cart badge shows 3

  Scenario: Reset app state clears the cart
    When I add "Sauce Labs Backpack" to the cart
    And I add "Sauce Labs Onesie" to the cart
    And I reset the app state
    Then the cart badge is empty
