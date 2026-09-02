@orangehrm @navigation
Feature: OrangeHRM main-menu navigation
  As an HR administrator
  I want to move between the modules
  So that I can manage every part of the organisation

  Background:
    Given I am signed in to OrangeHRM as the administrator

  @smoke
  Scenario: The dashboard is the landing page
    Then the "Dashboard" page is shown

  Scenario Outline: Opening the "<menu>" menu shows the "<title>" page
    When I open the "<menu>" menu
    Then the "<title>" page is shown

    # "Maintenance" is covered by the availability outline only - it prompts for
    # password re-authentication, so its breadcrumb is not immediate.
    Examples:
      | menu        | title       |
      | Admin       | Admin       |
      | PIM         | PIM         |
      | Leave       | Leave       |
      | Time        | Time        |
      | Recruitment | Recruitment |
      | Performance | Performance |
      | Directory   | Directory   |
      | Claim       | Claim       |
      | Buzz        | Buzz        |

  Scenario Outline: The "<menu>" menu item is available in the sidebar
    Then the "<menu>" menu is available

    Examples:
      | menu        |
      | Admin       |
      | PIM         |
      | Leave       |
      | Time        |
      | Recruitment |
      | My Info     |
      | Performance |
      | Dashboard   |
      | Directory   |
      | Maintenance |
      | Claim       |
      | Buzz        |

  Scenario: Logging out returns to the OrangeHRM login page
    When I log out of OrangeHRM
    Then the OrangeHRM login page is shown
