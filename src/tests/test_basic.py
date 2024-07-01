# pylint: disable=C0114,C0115,C0116,W0212

import allure
import pytest
from core import TestCore
from src.pages.home.page import HomePage
from src.pages.garden.page import GardenPage
from src.pages.plant.page import PlantPage
from src.utils.exception import TestFailure


@allure.title("Add New Plant Test")
@allure.id("very_cool_test_001")
@allure.tag("Smoke Test")
class TestsBasic(TestCore):

    def test_add_new_plant(self):
        try:
            with allure.step("Step 1. Open App"):
                self.home = HomePage(self.driver)
                self.garden = GardenPage(self.driver)
                self.plant = PlantPage(self.driver)
                self.home.confirm_ready()
            with allure.step("Step 2. Navigate to Add Plant"):
                self.home.open_add_plant()
            with allure.step("Step 3. Create New Plant"):
                self.plant.set_details("Tulips", "Very pretty!", "5th Floor Dungeon")
                details = self.plant.get_details()
                assert details == {
                    "Name": "Tulips",
                    "Desc": "Very pretty!",
                    "Location": "5th Floor Dungeon",
                }
                self.plant.set_day_planted("06/01/2024")
            with allure.step("Step 4. Verify New Plant"):
                self.garden.confirm_ready()
                self.garden.verify_plant("Tulips")
                allure.attach(
                    self.driver.get_screenshot_as_png(),
                    name="Plant Created",
                    attachment_type=allure.attachment_type.PNG,
                )
            self.platform.remove_output_folder()
        except TestFailure:
            allure.attach(
                self.driver.get_screenshot_as_png(),
                name="Test Failure",
                attachment_type=allure.attachment_type.PNG,
            )
            pytest.fail()
