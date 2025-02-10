from selenium.webdriver.common.by import By

from toolium.pageobjects.page_object import PageObject
from toolium.pageelements import InputText, Button


class LoginPageObject(PageObject):
    def init_page_elements(self):
        self.username = InputText(By.XPATH, "//input[@type='text']")
        self.password = InputText(By.XPATH, "//input[@type='password']")
        self.submit = Button(By.XPATH, "//button[@type='submit']")

    def open(self):
        """ Open login url in browser

        :returns: this page object instance
        """
        self.driver.get('{}'.format(self.config.get('Test', 'url')))
        return self


    def login(self):
        """ Fill login form and submit it

        :param user: dict with username and password values
        :returns: secure area page object instance
        """
        self.open()
        user = {
            'username': self.config.get('Test', 'username'),
            'password': self.config.get('Test', 'password')
        }
        self.username.text = user['username']
        self.password.text = user['password']
        self.submit.click()


    def wait_until_loaded(self):
        """ Wait until login page is loaded

        :returns: this page object instance
        """
        self.username.wait_until_visible()
        return self

