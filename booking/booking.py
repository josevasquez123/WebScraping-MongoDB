import booking.constants as const
from selenium import webdriver
from booking.booking_filtration import BookingFiltration
from prettytable import PrettyTable
from booking.booking_report import BookingReport
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from booking.mongoDB import MongoDB

class Booking:

    def __init__(self, driver_path=r"D:/AnalisisDatos/Python/Selenium/drivers/chromedriver.exe", teardown = False):
        self.driver_path = driver_path
        self.teardown = teardown
 
    def __enter__(self):
        
        options = webdriver.ChromeOptions()    
        options.add_experimental_option("excludeSwitches", ['enable-automation'])
        self.driver = webdriver.Chrome(self.driver_path)
        self.driver.implicitly_wait(2)
        self.driver.maximize_window()
        return self
 
    def __exit__(self, exc_type, exc_value, traceback):
        if self.teardown:
            self.driver.quit()
 
    def land_first_page(self):
        self.driver.get(const.BASE_URL)
    
    def change_currency(self, currency=None):
        currency_element = self.driver.find_element_by_css_selector(
            'button[data-tooltip-text="Choose your currency"]'
        )
        currency_element.click()

        selected_currency_element = self.driver.find_element_by_css_selector(
            f'a[data-modal-header-async-url-param*="selected_currency={currency}"]'
        )
        selected_currency_element.click()
    
    def select_place_to_go(self, place_to_go):
        search_field = self.driver.find_element_by_css_selector("input[name='ss']")
        search_field.clear()
        search_field.send_keys(place_to_go)

        #self.driver.execute_script('return')
        first_result = WebDriverWait(self.driver,10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'li[data-i="0"]'))
        )
        """ first_result = self.driver.find_element_by_css_selector(
            'li[data-i="0"]'
        ) """
        first_result.click()
    
    def select_dates(self, check_in_date, check_out_date):
        check_in_element = self.driver.find_element_by_css_selector(
            f'td[data-date="{check_in_date}"]'
        )
        check_in_element.click()

        check_out_element = self.driver.find_element_by_css_selector(
            f'td[data-date="{check_out_date}"]'
        )
        check_out_element.click()

    def select_adults(self, count=1):
        selection_element = self.driver.find_element_by_id('xp__guests__toggle')
        selection_element.click()

        while True:
            decrease_adults_element = self.driver.find_element_by_css_selector(
                'button[aria-label="Decrease number of Adults"]'
            )
            decrease_adults_element.click()
            #If the value of adults reaches 1, then we should get out
            #of the while loop
            adults_value_element = self.driver.find_element_by_id('group_adults')
            adults_value = adults_value_element.get_attribute(
                'value'
            ) # Should give back the adults count

            if int(adults_value) == 1:
                break

        increase_button_element = self.driver.find_element_by_css_selector(
            'button[aria-label="Increase number of Adults"]'
        )
        
        for _ in range(count - 1):
            increase_button_element.click()

    def click_search(self):
        search_button = self.driver.find_element_by_css_selector(
            'button[type="submit"]'
        )
        search_button.click()

    def close_popup_apply_filtration(self):
        try:
            popup = self.driver.find_element_by_css_selector("button[arial-label='Ignorar información sobre el inicio de sesión.']")
            popup.click()
            self.apply_filtrations()
        except:
            self.apply_filtrations()
    
    def apply_filtrations(self):
        filtration = BookingFiltration(driver=self.driver)
        filtration.sort_price_lower_first()
        filtration.apply_star_rating(3,4)
        self.driver.refresh()
    
    def one_page_report_results(self, mongo_driver:MongoDB):
        hotel_boxes = self.driver.find_element_by_id(
            'search_results_table'
        )

        report = BookingReport(hotel_boxes)
        table = PrettyTable(
            field_names=["Hotel Name", "Hotel Price", "Hotel Score"]
        )
        hotel_info = report.pull_deal_box_attributes()
        mongo_driver.insert_documents(hotel_info)
        table.add_rows(hotel_info)
        print(table)
    
    def next_page(self):
        next_page_button = self.driver.find_element_by_css_selector('button[aria-label="Next page"]')
        next_page_button.click()
        self.driver.refresh()
    
    def all_pages_report_results(self):
        mongo_driver = MongoDB()
        
        while True:
            self.one_page_report_results(mongo_driver)
            
            if self.driver.find_element_by_css_selector('button[aria-label="Next page"]').is_enabled()==False:
                break

            self.next_page()