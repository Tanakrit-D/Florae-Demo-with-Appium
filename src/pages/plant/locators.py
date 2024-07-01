# pylint: disable=C0301

from appium.webdriver.common.appiumby import AppiumBy


class PlantLocators:
    """Plant Page Locators"""

    NEW_HEADING = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("New")')
    NAME_FIELD = (
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().className("android.widget.EditText").instance(0)',
    )
    DESC_FIELD = (
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().className("android.widget.EditText").instance(1)',
    )
    LOCATION_FIELD = (
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().className("android.widget.EditText").instance(2)',
    )
    NAME_TEXT = (
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().className("android.view.View").instance(6).childSelector(className("android.widget.EditText").instance(0))',
    )
    DESC_TEXT = (
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().className("android.view.View").instance(6).childSelector(className("android.widget.EditText").instance(1))',
    )
    LOCATION_TEXT = (
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().className("android.view.View").instance(6).childSelector(className("android.widget.EditText").instance(2))',
    )
    DAY_PLANTED = (
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().descriptionContains("Day planted")',
    )
    DATE_PICKER_EDIT = (
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().className("android.widget.Button").instance(0)',
    )
    DATE_PICKER_OK = (
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().description("OK")',
    )
    SAVE_BUTTON = (
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().description("Save")',
    )
