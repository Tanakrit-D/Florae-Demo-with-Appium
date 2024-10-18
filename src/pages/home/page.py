# pylint: disable=C0116

import logging

from selenium.webdriver.remote.webdriver import WebDriver

from src.pages.home.locators import HomeLocators
from src.utils.action import Action
from src.utils.wait import Wait


class HomePage:
    """
    Home Page Object Model.

    Locator tuples must be unpacked with * when called.
    """

    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.action = Action(self.driver)
        self.wait = Wait(self.driver)
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.info("Interacting with: Home Page")

    def confirm_ready(self) -> None:
        self.wait.for_element_to_be_visible(*HomeLocators.TODAY_HEADING)

    def open_add_plant(self) -> None:
        self.wait.for_element_to_be_clickable(*HomeLocators.ADD_PLANT_BUTTON)
        self.driver.find_element(*HomeLocators.ADD_PLANT_BUTTON).click()
        self.wait.for_element_to_be_visible(*HomeLocators.NEW_HEADING)
