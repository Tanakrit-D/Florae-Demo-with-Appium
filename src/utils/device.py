from __future__ import annotations

import datetime
import logging
import time
from pathlib import Path

from selenium.webdriver.remote.webdriver import WebDriver

from src.utils.exception import AppRefreshFailureError, ContextSwitchingFailureError, ScreenshotFailureError


class Device:
    """Represents the connected device used during testing, providing associated methods for interaction."""

    def __init__(self, driver: WebDriver, activity: str, output_dir: str) -> None:
        """
        Initialize the Device instance.

        Args:
            driver (WebDriver): The driver instance for device control.
            activity (str): The activity name of the app being tested.
            output_dir (str): The directory for storing runtime files.

        """
        self.driver = driver
        self.activity = activity
        self.output_dir = output_dir
        self.logger = logging.getLogger(self.__class__.__name__)

    def screenshot(self) -> str:
        """
        Take a screenshot and save it to the output directory.

        Returns:
            str: The file path of the saved screenshot.

        """
        date = datetime.datetime.now(tz=datetime.UTC)
        file_name = f"screenshot_{date.strftime('%Y-%m-%d_%H-%M-%S')}.png"
        file_path = Path(self.output_dir) / file_name
        try:
            self.driver.save_screenshot(file_path)
            self.logger.info("Screenshot saved to: %s", file_path)
            return str(file_path)
        except Exception as e:
            error_message = "Failed to take screenshot: %s", str(e)
            self.logger.exception(error_message)
            raise ScreenshotFailureError(error_message, e) from e

    def refresh_app_instance(self) -> None:
        """Refresh the app by terminating and reactivating it."""
        try:
            self.driver.terminate_app(self.activity)
            time.sleep(1.5)
            self.driver.activate_app(self.activity)
            self.logger.info("App %s refreshed", self.activity)
        except Exception as e:
            error_message = "Failed to refresh app: %s", str(e)
            self.logger.exception(error_message)
            raise AppRefreshFailureError(error_message, e) from e

    def switch_context(self, context: str) -> None:
        """
        Switch the driver's context.

        Args:
            context (str): The context to switch to.

        Raises:
            Exception: If switching context fails.

        """
        try:
            self.driver.switch_to.context(context)
            self.logger.info("Switched to context: %s", context)
        except Exception as e:
            error_message = "Failed to switch to context %s: %s", context, str(e)
            self.logger.exception(error_message)
            raise ContextSwitchingFailureError(error_message, e) from e

    def switch_to_native(self) -> None:
        """Switch to the native app context."""
        self.switch_context("NATIVE_APP")

    def switch_to_webview(self) -> None:
        """
        Switch to the webview context.

        Raises:
            ValueError: If the webview context is not found.

        """
        webview = f"WEBVIEW_{self.activity}"
        contexts = self.driver.contexts
        for context_name in contexts:
            if webview in context_name:
                self.switch_context(context_name)
                return
        msg = f"Failed to switch to {webview}"
        raise ValueError(msg)

    def fix_permissions_issue(self) -> None:
        """Fix permissions issues by granting all permissions to the app."""
        params = {"permissions": "all", "appPackage": self.activity, "action": "grant"}
        self.driver.execute_script("mobile: changePermissions", params)
        self.logger.info("Permissions fixed for %s", self.activity)
