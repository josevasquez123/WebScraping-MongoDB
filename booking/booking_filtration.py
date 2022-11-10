from selenium.webdriver.remote.webdriver import WebDriver

class BookingFiltration:
    def __init__(self, driver:WebDriver):
        self.driver = driver
    
    def apply_star_rating(self, *star_values):
        star_filtration_box = self.driver.find_element_by_css_selector('div[data-filters-group="class"]')
        star_child_elements = star_filtration_box.find_elements_by_css_selector('*')
        
        for star_value in star_values:
            for star_element in star_child_elements:
                if str(star_element.get_attribute('innerHTML')).strip() == f'{star_value} stars':
                    star_element.click()
        
    
    def sort_price_lower_first(self):
        element = self.driver.find_element_by_css_selector(
            'button[data-selected-sorter="popularity"]'
        )

        element.click()

        lower_price = self.driver.find_element_by_css_selector(
            'button[data-id="price"]'
        )

        lower_price.click()
