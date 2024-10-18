# pylint: disable=C0114,C0116

from __future__ import annotations

import logging

from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from src.utils.helpers import Helpers


class Action:
    """Handles various actions on mobile elements."""

    def __init__(self, driver: WebDriver) -> None:
        """
        Initialize the Action instance.

        Args:
            driver: The Appium driver instance.

        """
        self.driver = driver
        self.helpers = Helpers()
        self.logger = logging.getLogger(self.__class__.__name__)

    def _calculate_element_points(self, element: WebElement) -> dict[str, tuple[int, int]]:
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

    def click(
        self, by: str = AppiumBy.ID, value: str | dict | None = None,
    ) -> None:
        """
        Click an element.

        Args:
            by: The method to locate the element.
            value: The locator value.

        """
        self.driver.find_element(by, value).click()

    def click_element_centre(
        self, by: str = AppiumBy.ID, value: str | dict | None = None,
    ) -> None:
        """
        Click the mid-point of an element.

        Args:
            by: The method to locate the element.
            value: The locator value.

        """
        element = self.driver.find_element(by, value)
        element_points = self._calculate_element_points(element)
        action = ActionChains(self.driver)
        action.w3c_actions = ActionBuilder(
            self.driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"),
        )
        action.w3c_actions.pointer_action.move_to_location(
            element_points["mid"][0], element_points["mid"][1],
        )
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

    def send_keycode(self, keycode: int) -> None:
        """
        Send a keycode to the device.

        Args:
            keycode (int): The keycode to send.

        """
        self.driver.press_keycode(keycode)
        self.logger.info("Keycode %s sent", keycode)

    def send_keycodes(self, value: str) -> None:
        """
        Send keycodes to the device.

        These are converted/mapped from their regular values to the keycode value.

        Args:
            value (str): The values to send.

        """
        codes = self.helpers.convert_string_to_nativekey(value)
        for code in codes:
            self.send_keycode(code)

    def send_enter_key(self) -> None:
        """Send the enter key (keycode 66)."""
        self.send_keycode(66)
        self.logger.info("Keycode 66 (ENTER) sent")

    def send_back_key(self) -> None:
        """Send the back key (keycode 4)."""
        self.send_keycode(4)
        self.logger.info("Keycode 4 (BACK) sent")

    def dismiss_keyboard(self) -> None:
        """Dismiss the keyboard if it's visible."""
        self.driver.hide_keyboard()
        self.logger.info("Keyboard dismissed")

    def get_element_text(
        self, by: str = AppiumBy.ID, value: str | dict | None = None,
    ) -> str:
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
