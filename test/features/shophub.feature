Feature: E-Commerce Cart

  Scenario: Add and delete elements form cart
    Given I login into ShopHub
    When I serch product by "home" name
    Then I fill cart with 3 products
    And I delete 1 element from cart

    