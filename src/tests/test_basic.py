# pylint: disable=C0114,C0115,C0116,W0212

import allure
import pytest
from appium.webdriver.common.appiumby import AppiumBy
from appium_swipe_actions.core import SeekDirection
from core import TestCore
from src.utils.exception import TestFailure

@allure.title("Basic Test")
@allure.id("test_basic_001")
@allure.tag("Smoke Test")
class TestDemo(TestCore):
    def test_element_search(self):
        try:
            with allure.step("Step 1. Open App"):
                self.wait.for_element_to_be_visible(
                    by=AppiumBy.ANDROID_UIAUTOMATOR,
                    value='new UiSelector().description("Today")',
                )
            with allure.step("Step 2. Navigate to Add Plant"):
                self.action.click(
                    by=AppiumBy.ANDROID_UIAUTOMATOR,
                    value='new UiSelector().className("android.widget.Button").instance(3)',
                )
            with allure.step("Step 3. Search for Day Planted"):
                self.wait.for_element_to_be_visible(
                    by=AppiumBy.XPATH,
                    value='//android.widget.Button[@content-desc="Save"]'
                )
                self.swipe.swipe_element_into_view(
                    AppiumBy.ANDROID_UIAUTOMATOR,
                    'new UiSelector().descriptionContains("Day planted")',
                    SeekDirection.DOWN,
                )
            self.platform.remove_output_folder()
        except TestFailure:
            allure.attach(
                self.device.screenshot(),
                name="Test Failure",
                attachment_type=allure.attachment_type.PNG,
            )
            pytest.fail()
