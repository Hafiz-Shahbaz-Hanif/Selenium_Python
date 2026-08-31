@saucedemo @checkout
Feature: SauceDemo checkout
  As a signed-in shopper
  I want to check out the items in my cart
  So that I can complete my purchase

  Background:
    Given I am signed in to SauceDemo as the standard user
    And my cart contains:
      | product               |
      | Sauce Labs Backpack   |
      | Sauce Labs Bike Light |

  @smoke @e2e
  Scenario: Complete a purchase
    When I check out with details "Hafiz", "QA", "54000"
    And I finish the order
    Then I see the confirmation "Thank you for your order!"

  Scenario: Checkout requires customer details
    When I proceed to checkout without entering details
    Then I see the checkout error "First Name is required"
