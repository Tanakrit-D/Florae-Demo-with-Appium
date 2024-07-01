from appium.webdriver.common.appiumby import AppiumBy


class HomeLocators:
    """Home Page Locators"""

    TODAY_HEADING = (
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().description("Today")',
    )
    ADD_PLANT_BUTTON = (
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().className("android.widget.Button").instance(3)',
    )
    NEW_HEADING = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("New")')
