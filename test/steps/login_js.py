import time

from behave import when, step

from pageobjects.login import LoginPageObject
from pageobjects.main_page import MainPagePageObject


@step('I login into Juice Shop')
def step_impl(context):
    
    context.driver.get('{}'.format('https://juice-shop.herokuapp.com'))
    import pdb; pdb.set_trace()



