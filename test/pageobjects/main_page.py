from selenium.webdriver.common.by import By

from toolium.pageobjects.page_object import PageObject
from toolium.pageelements import Text, InputText, Button


class MainPagePageObject(PageObject):
    def init_page_elements(self):
        self.header = Text(By.XPATH, '//h1[text()="ShopHub"]')
        self.search = InputText(By.XPATH, '//input[@placeholder="Search products..."]')
        self.add_element_1 = Button(By.XPATH, '(//button[text()="Add to Cart"])[1]')
        self.add_element_2 = Button(By.XPATH, '(//button[text()="Add to Cart"])[2]')
        self.add_element_3 = Button(By.XPATH, '(//button[text()="Add to Cart"])[3]')
        self.delete_element_1 = Button(By.XPATH, '(//button[contains(@class, "text-red")])[1]')
        self.expand_cart = Button(By.XPATH, '(//button[contains(@class, "p-2 hover:bg-gray-100 rounded-full")])[1]')

    def search_products(self, product_name):

        self.search.text = product_name
        return self

    def wait_until_loaded(self):
        """ Wait until login page is loaded

        :returns: this page object instance
        """
        self.header.wait_until_visible()
        return self

