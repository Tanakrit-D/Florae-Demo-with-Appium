import time
import logging
from datetime import datetime
from pathlib import Path


class Device:
    """
    Represents a device for automation testing, providing methods for
    screenshot capture, app management, context switching, and key events.
    """

    def __init__(self, driver, activity: str, output_dir: str):
        """
        Initialize the Device instance.

        Args:
            driver: The driver instance for device control.
            activity (str): The activity name of the app being tested.
            output_directory (str): The directory for storing runtime files.
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
        date = datetime.now()
        file_name = f"screenshot_{date.strftime('%Y-%m-%d_%H-%M-%S')}.png"
        file_path = Path(self.output_dir) / file_name
        try:
            self.driver.save_screenshot(file_path)
            self.logger.info("Screenshot saved to: %s", file_path)
            return str(file_path)
        except Exception as e:
            error_message = "Failed to take screenshot: %s", str(e)
            self.logger.error(error_message)
            raise ScreenshotFailure(error_message, e) from e

    def refresh_app_instance(self) -> None:
        """
        Refresh the app by terminating and reactivating it.
        """
        try:
            self.driver.terminate_app(self.activity)
            time.sleep(1.5)
            self.driver.activate_app(self.activity)
            self.logger.info("App %s refreshed", self.activity)
        except Exception as e:
            error_message = "Failed to refresh app: %s", str(e)
            self.logger.error(error_message)
            raise AppRefreshFailure(error_message, e) from e

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
            self.logger.error(error_message)
            raise ContextSwitchingFailure(error_message, e) from e

    def switch_to_native(self) -> None:
        """
        Switch to the native app context.
        """
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
        raise ValueError(f"Failed to switch to {webview}")

    def fix_permissions_issue(self) -> None:
        """
        Fix permissions issues by granting all permissions to the app.
        """
        params = {"permissions": "all", "appPackage": self.activity, "action": "grant"}
        self.driver.execute_script("mobile: changePermissions", params)
        self.logger.info("Permissions fixed for %s", self.activity)


class AppRefreshFailure(Exception):
    """Custom exception raised when an app refresh operation fails."""

    def __init__(self, message: str, original_error: Exception = None):
        self.message = message
        self.original_error = original_error
        super().__init__(self.message)


class ContextSwitchingFailure(Exception):
    """Custom exception raised when an context switching operation fails."""

    def __init__(self, message: str, original_error: Exception = None):
        self.message = message
        self.original_error = original_error
        super().__init__(self.message)


class ScreenshotFailure(Exception):
    """Custom exception raised when a screenshot operation fails."""

    def __init__(self, message: str, original_error: Exception = None):
        self.message = message
        self.original_error = original_error
        super().__init__(self.message)
