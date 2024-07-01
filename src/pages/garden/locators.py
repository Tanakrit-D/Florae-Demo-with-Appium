# pylint: disable=C0301

from appium.webdriver.common.appiumby import AppiumBy


class GardenLocators:
    """Garden Page Locators"""

    GARDEN_HEADING = (
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().description("Garden")',
    )
    PLACEHOLDER = (
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().description("Placeholder")',
    )
