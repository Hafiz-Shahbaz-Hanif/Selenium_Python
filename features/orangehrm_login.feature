@orangehrm @login
Feature: OrangeHRM authentication
  As an HR administrator
  I want to sign in to OrangeHRM
  So that I can manage the organisation

  Background:
    Given the OrangeHRM login page is open

  @smoke
  Scenario: Administrator signs in successfully
    When I sign in to OrangeHRM as the administrator
    Then the OrangeHRM dashboard is displayed

  Scenario: Invalid credentials are rejected
    When I sign in to OrangeHRM with username "Admin" and password "wrong-password"
    Then I see the OrangeHRM error "Invalid credentials"
