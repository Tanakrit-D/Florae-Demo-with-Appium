# pylint: disable=C0116
from __future__ import annotations

import logging

from appium.swipe.actions import SeekDirection, SwipeActions
from selenium.webdriver.remote.webdriver import WebDriver

from src.pages.plant.locators import PlantLocators
from src.utils.action import Action
from src.utils.wait import Wait


class PlantPage:
    """
    Plant Page Object Model.

    Locator tuples must be unpacked with * when called.
    """

    def __init__(self, driver: WebDriver) -> None:
        self.driver = driver
        self.action = Action(self.driver)
        self.swipe = SwipeActions(self.driver)
        self.wait = Wait(self.driver)
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.info("Interacting with: Plant Page")

    def set_details(self, name: str, desc: str, location: str) -> None:
        name_field = self.driver.find_element(*PlantLocators.NAME_FIELD)
        name_field.click()
        name_field.send_keys(name)
        self.action.dismiss_keyboard()

        desc_field = self.driver.find_element(*PlantLocators.DESC_FIELD)
        desc_field.click()
        desc_field.send_keys(desc)
        self.action.dismiss_keyboard()

        location_field = self.driver.find_element(*PlantLocators.LOCATION_FIELD)
        location_field.click()
        location_field.send_keys(location)
        self.action.dismiss_keyboard()

    def get_details(self) -> dict[str, str]:
        name_text = self.action.get_element_text(*PlantLocators.NAME_TEXT)
        desc_text = self.action.get_element_text(*PlantLocators.DESC_TEXT)
        location_text = self.action.get_element_text(*PlantLocators.LOCATION_TEXT)
        return {
            "Name": name_text,
            "Desc": desc_text,
            "Location": location_text,
        }

    def set_day_planted(self, date: str) -> None:
        self.swipe.swipe_element_into_view(
            *PlantLocators.DAY_PLANTED, SeekDirection.DOWN,
        )
        self.action.click(*PlantLocators.DAY_PLANTED)
        self.wait.for_element_to_be_clickable(*PlantLocators.DATE_PICKER_EDIT)
        self.action.click(*PlantLocators.DATE_PICKER_EDIT)
        self.action.send_keycodes(date)
        self.action.send_enter_key()
        self.action.click(*PlantLocators.DATE_PICKER_OK)
        self.wait.for_element_to_be_clickable(*PlantLocators.SAVE_BUTTON)
        self.action.click(*PlantLocators.SAVE_BUTTON)
