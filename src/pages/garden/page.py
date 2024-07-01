# pylint: disable=C0116

import logging
from appium.webdriver.common.appiumby import AppiumBy
from src.pages.garden.locators import GardenLocators
from src.utils.action import Action
from src.utils.wait import Wait


class GardenPage:
    """
    Garden Page Object Model

    Locator tuples must be unpacked with * when called.
    """

    def __init__(self, driver):
        self.driver = driver
        self.action = Action(self.driver)
        self.wait = Wait(self.driver)
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.info("Interacting with: Garden Page")

    def confirm_ready(self) -> None:
        self.wait.for_element_to_be_visible(*GardenLocators.GARDEN_HEADING)

    def verify_plant(self, plant_name: str) -> None:
        value = f'new UiSelector().descriptionContains("{plant_name}")'
        self.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, value)
