import os
import configparser
from ast import literal_eval
from dataclasses import dataclass
from enum import Enum
from typing import Dict, Any
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium_swipe_actions.core import SwipeActions
from src.utils.action import Action
from src.utils.device import Device
from src.utils.platform import Platform
from src.utils.wait import Wait


CUR_DIR = os.path.dirname(__file__)
CONFIG_PATH = os.path.join(CUR_DIR, "../../config.cfg")


class DeviceType(Enum):
    """
    Connected device types.
    """

    PHYSICAL = "PHYSICAL"
    WIFI = "WIFI"
    VIRTUAL = "VIRTUAL"


@dataclass
class EnvConfig:
    """
    Configuration dataclass for Environment settings.

    Attributes:
        url (str): URL path.
        debug (bool): Flag for configuring various debugging behaviours.
    """

    url: str
    debug: bool


@dataclass
class AppiumConfig:
    """
    Configuration dataclass for Appium settings.

    Attributes:
        host (str): Appium server host.
        port (str): Appium server port.
        no_reset (bool): Flag to prevent app reset between sessions.
        full_reset (bool): Flag to perform a full reset before session.
        remote_apps_cache_limit (int): Limit for remote apps cache.
        new_command_timeout (int): Timeout for new commands.
        uiautomator2_server_install_timeout (int): Timeout for UIAutomator2 server installation.
        adb_exec_timeout (int): Timeout for ADB command execution.
    """

    host: str
    port: str
    no_reset: bool
    full_reset: bool
    remote_apps_cache_limit: int
    new_command_timeout: int
    uiautomator2_server_install_timeout: int
    adb_exec_timeout: int


@dataclass
class AndroidConfig:
    """
    Configuration dataclass for Android-specific settings.

    Attributes:
        connected_device (str): Identifier for the connected Android device.
        apk (str): Path to the Android APK file.
        package (str): Android package name.
        id_physical (str): Identifier for physical device.
        id_wifi (str): Identifier for WiFi-connected device.
        id_virtual (str): Identifier for virtual device.
    """

    connected_device: str
    apk: str
    package: str
    id_physical: str
    id_wifi: str
    id_virtual: str


@dataclass
class AppConfig:
    """
    Overall application configuration dataclass.

    Attributes:
        appium (AppiumConfig): Appium-specific configuration.
        android (AndroidConfig): Android-specific configuration.
    """

    env: EnvConfig
    appium: AppiumConfig
    android: AndroidConfig


class ConfigLoader:
    """
    Utility class for loading configuration from a file.
    """

    @staticmethod
    def load_config(config_path: str) -> AppConfig:
        """
        Load configuration from a specified file path.

        Args:
            config_path (str): Path to the configuration file.

        Returns:
            AppConfig: Loaded application configuration.
        """
        config = configparser.ConfigParser()
        config.read(config_path)

        env_config = EnvConfig(
            url=config.get("ENVIRONMENT", "url"),
            debug=config.get("ENVIRONMENT", "debug"),
        )

        appium_config = AppiumConfig(
            host=config.get("APPIUM", "appium_host"),
            port=config.get("APPIUM", "appium_port"),
            no_reset=literal_eval(config.get("APPIUM", "no_reset")),
            full_reset=literal_eval(config.get("APPIUM", "full_reset")),
            remote_apps_cache_limit=int(
                config.get("APPIUM", "remote_apps_cache_limit")
            ),
            new_command_timeout=int(config.get("APPIUM", "new_command_timeout")),
            uiautomator2_server_install_timeout=int(
                config.get("APPIUM", "uiautomator2_server_install_timeout")
            ),
            adb_exec_timeout=int(config.get("APPIUM", "adb_exec_timeout")),
        )

        android_config = AndroidConfig(
            connected_device=config.get("ANDROID", "android_connected_device"),
            apk=config.get("APP", "android_apk"),
            package=config.get("APP", "package"),
            id_physical=config.get("ANDROID", "android_id_physical"),
            id_wifi=config.get("ANDROID", "android_id_wifi"),
            id_virtual=config.get("ANDROID", "android_id_virtual"),
        )

        return AppConfig(env=env_config, appium=appium_config, android=android_config)


class DeviceOptionsFactory:
    """
    Factory class for creating device options based on configuration and device type.
    """

    @staticmethod
    def create_options(config: AppConfig) -> Dict[str, Any]:
        """
        Create device options for Appium based on the provided configuration and device type.

        Args:
            config (AppConfig): Application configuration.
            device_type (DeviceType): Type of the device (PHYSICAL, WIFI, or VIRTUAL).

        Returns:
            Dict[str, Any]: Dictionary of device options for Appium.
        """
        options: Dict[str, Any] = {
            "platformName": "Android",
            "automationName": "UIAutomator2",
            "noReset": config.appium.no_reset,
            "fullReset": config.appium.full_reset,
            "platformVersion": "13",
            "appPackage": "cat.naval.florae",
            "appActivity": ".MainActivity",
            "autoGrantPermissions": True,
            "ignoreUnimportantViews": False,
            "ensureWebviewsHavePages": True,
            "remoteAppsCacheLimit": config.appium.remote_apps_cache_limit,
            "newCommandTimeout": config.appium.new_command_timeout,
            "uiautomator2ServerInstallTimeout": config.appium.uiautomator2_server_install_timeout,
            "adbExecTimeout": config.appium.adb_exec_timeout,
        }

        if config.android.connected_device == "PHYSICAL":
            options["udid"] = config.android.id_physical
            options["deviceName"] = config.android.id_physical
        elif config.android.connected_device == "WIFI":
            options["deviceName"] = config.android.id_wifi
        else:
            options["avd"] = config.android.id_virtual
            options["deviceName"] = config.android.id_virtual

        options["app"] = os.path.join(os.getcwd(), config.android.apk)

        return options


class TestCore:
    """
    Core class for Appium-based testing, handling setup and teardown of test sessions.
    """

    @property
    def scheme(self) -> str:
        """
        Get the URL scheme for the Appium server.

        Returns:
            str: URL scheme (http://).
        """
        return "http://"

    @property
    def appium_url(self) -> str:
        """
        Get the full URL for the Appium server.

        Returns:
            str: Full Appium server URL.
        """
        return f"{self.scheme}{self.config.appium.host}:{self.config.appium.port}"

    def setup_method(self) -> None:
        """
        Set up the test environment before each test method.
        Initializes configuration, device options, and creates necessary objects for testing.
        """
        self.config = ConfigLoader.load_config(CONFIG_PATH)
        self.options = DeviceOptionsFactory.create_options(self.config)
        self.driver = webdriver.Remote(
            self.appium_url,
            options=UiAutomator2Options().load_capabilities(self.options),
        )
        self.action = Action(self.driver)
        self.platform = Platform(self.config.env.debug)
        self.device = Device(
            self.driver, self.config.android.package, self.platform.output_dir
        )
        self.swipe = SwipeActions(self.driver)
        self.wait = Wait(self.driver)

    def teardown_method(self) -> None:
        """
        Clean up the test environment after each test method.
        Quits the driver if it exists.
        """
        if not hasattr(self, "driver"):
            return
        self.driver.quit()
