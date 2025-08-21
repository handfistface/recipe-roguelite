
from pytest import mark
from lib.mealDbApi import MealDbApi


class TestMealDbApi:
    def arrange_mealDbApi(self):
        self.mealDbApi = MealDbApi()

    @mark.skip("Meant for manual testing")
    def test_listMealsByFirstLetter_DryRun(self):
        # Arrange
        self.arrange_mealDbApi()
        # Act
        actual = self.mealDbApi.listMealsByFirstLetter("a")
        # Assert
        assert len(actual) > 0