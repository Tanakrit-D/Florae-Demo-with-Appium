# pylint: disable=C0114,C0116

import logging
from typing import Dict, Union, Tuple
from enum import Enum, unique
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput

@unique
class Direction(Enum):
    """Enumeration for swipe directions."""
    DOWN = "down"
    UP = "up"
    RIGHT = "right"
    LEFT = "left"

class Action:
    """Handles various actions on mobile elements."""

    def __init__(self, driver):
        """
        Initialize the Action instance.

        Args:
            driver: The Appium driver instance.
        """
        self.driver = driver
        self.logger = logging.getLogger(self.__class__.__name__)

    def _calculate_element_points(self, element) -> Dict[str, Tuple[int, int]]:
        """
        Calculate various points on an element.

        Args:
            element: The WebElement to calculate points for.

        Returns:
            A dictionary containing coordinates of various points on the element.
        """
        x, y = element.location["x"], element.location["y"]
        width, height = element.size["width"], element.size["height"]

        return {
            "top_left": (x, y),
            "top_mid": (x + width // 2, y),
            "top_right": (x + width, y),
            "left_mid": (x, y + height // 2),
            "mid": (x + width // 2, y + height // 2),
            "right_mid": (x + width, y + height // 2),
            "bottom_left": (x, y + height),
            "bottom_mid": (x + width // 2, y + height),
            "bottom_right": (x + width, y + height),
        }

    def click(self, by: str = AppiumBy.ID, value: Union[str, Dict, None] = None) -> None:
        """
        It clicks! It just clicks!

        Args:
            by: The method to locate the element.
            value: The locator value.
        """
        self.driver.find_element(by, value).click()

    def click_element_centre(self, by: str = AppiumBy.ID, value: Union[str, Dict, None] = None) -> None:
        """
        Click the mid-point of an element.

        Args:
            by: The method to locate the element.
            value: The locator value.
        """
        element = self.driver.find_element(by, value)
        element_points = self._calculate_element_points(element)
        action = ActionChains(self.driver)
        action.w3c_actions = ActionBuilder(self.driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
        action.w3c_actions.pointer_action.move_to_location(element_points["mid"][0], element_points["mid"][1])
        action.w3c_actions.pointer_action.pointer_down()
        action.w3c_actions.pointer_action.pause(1)
        action.w3c_actions.pointer_action.release()
        action.perform()
        self.logger.info("Successfully clicked element: %s=%s", by, value)

    def send_keys(self, value: str) -> None:
        """
        Input text into the active element.

        Args:
            value: The text to input.
        """
        actions = ActionChains(self.driver)
        actions.pause(1)
        actions.send_keys(value)
        actions.perform()
        self.logger.info("Successfully sent keys: %s", value)

    def get_element_text(self, by: str = AppiumBy.ID, value: Union[str, Dict, None] = None) -> str:
        """
        Get the text of an element.

        Args:
            by: The method to locate the element.
            value: The locator value.

        Returns:
            The text of the element.
        """
        element = self.driver.find_element(by, value)
        text = element.text
        self.logger.info("Successfully retrieved text from element: %s=%s", by, value)
        return text
