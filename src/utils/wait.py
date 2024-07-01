# pylint: disable=C0114

import logging
from typing import Dict, Union
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as Conditions
from appium.webdriver.common.appiumby import AppiumBy


class Wait:
    """
    A utility class for waiting on various element conditions in Appium tests.

    This class provides methods to wait for elements to be visible, invisible,
    present, or clickable.
    """

    def __init__(self, driver, timeout: int = 30):
        """
        Initialize the Wait class.

        Args:
            driver: The Appium driver instance.
            timeout (int): The maximum time to wait for a condition, in seconds.
        """
        self.driver = driver
        self.timeout = timeout
        self.logger = logging.getLogger(__name__)

    def _wait_for_condition(
        self, condition, by: str, value: Union[str, Dict, None], action: str
    ):
        """
        Generic method to wait for a specific condition.

        Args:
            condition: The expected condition to wait for.
            by (str): The locator strategy.
            value (Union[str, Dict, None]): The locator value.
            action (str): Description of the action being waited for.

        Raises:
            TimeoutException: If the condition is not met within the timeout period.
        """
        try:
            WebDriverWait(self.driver, timeout=self.timeout).until(
                condition((by, value))
            )
            self.logger.info("Element %s successfully: %s=%s", action, by, value)
        except TimeoutException:
            self.logger.error(
                "Timeout waiting for element to be %s: %s=%s", action, by, value
            )
            raise

    def for_element_to_be_visible(
        self, by: str = AppiumBy.ID, value: Union[str, Dict, None] = None
    ) -> None:
        """
        Wait for an element to be visible.

        Args:
            by (str): The locator strategy (default is AppiumBy.ID).
            value (Union[str, Dict, None]): The locator value.

        Raises:
            TimeoutException: If the element is not visible within the timeout period.
        """
        self._wait_for_condition(
            Conditions.visibility_of_element_located, by, value, "visible"
        )

    def for_element_to_be_invisible(
        self, by: str = AppiumBy.ID, value: Union[str, Dict, None] = None
    ) -> None:
        """
        Wait for an element to be invisible.

        Args:
            by (str): The locator strategy (default is AppiumBy.ID).
            value (Union[str, Dict, None]): The locator value.

        Raises:
            TimeoutException: If the element is still visible after the timeout period.
        """
        self._wait_for_condition(
            Conditions.invisibility_of_element_located, by, value, "invisible"
        )

    def for_element_to_be_present(
        self, by: str = AppiumBy.ID, value: Union[str, Dict, None] = None
    ) -> None:
        """
        Wait for an element to be present in the DOM.

        Args:
            by (str): The locator strategy (default is AppiumBy.ID).
            value (Union[str, Dict, None]): The locator value.

        Raises:
            TimeoutException: If the element is not present within the timeout period.
        """
        self._wait_for_condition(
            Conditions.presence_of_element_located, by, value, "present"
        )

    def for_element_to_be_clickable(
        self, by: str = AppiumBy.ID, value: Union[str, Dict, None] = None
    ) -> None:
        """
        Wait for an element to be clickable.

        Args:
            by (str): The locator strategy (default is AppiumBy.ID).
            value (Union[str, Dict, None]): The locator value.

        Raises:
            TimeoutException: If the element is not clickable within the timeout period.
        """
        self._wait_for_condition(
            Conditions.element_to_be_clickable, by, value, "clickable"
        )
