import time

from behave import when, step

from pageobjects.login import LoginPageObject
from pageobjects.main_page import MainPagePageObject


@step('I login into ShopHub')
def step_impl(context):
    
    LoginPageObject().login()
    MainPagePageObject().wait_until_loaded()


@step('I serch product by "{product_name}" name')
def step_impl(context, product_name):
    
    MainPagePageObject().search_products(product_name)


@step('I fill cart with 3 products')
def step_impl(context):
    
    MainPagePageObject().add_element_1.click()
    MainPagePageObject().add_element_2.click()
    MainPagePageObject().add_element_3.click()

@step('I delete 1 element from cart')
def step_impl(context):
    MainPagePageObject().expand_cart.click()
    MainPagePageObject().delete_element_1.click()
