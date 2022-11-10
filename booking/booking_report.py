from selenium.webdriver.remote.webelement import WebElement


class BookingReport:
    def __init__(self, boxes_section_element:WebElement):
        self.boxes_section_element = boxes_section_element
        self.deal_boxes = self.pull_deal_boxes()

    def pull_deal_boxes(self):
        return self.boxes_section_element.find_elements_by_css_selector(
            'div[data-testid="property-card"]'
        )

    def pull_deal_box_attributes(self):
        collection = []
        for deal_box in self.deal_boxes:
            hotel_name = deal_box.find_element_by_css_selector(
                'div[data-testid="title"]'
            ).get_attribute('innerHTML').strip()
            
            if not deal_box.find_elements_by_css_selector('span[data-testid="price-and-discounted-price"]'):
                hotel_price = deal_box.find_element_by_css_selector(
                    'div[data-testid="price-and-discounted-price"]'
                ).find_element_by_tag_name('div').get_attribute('innerHTML').strip()
            else:
                hotel_price = deal_box.find_element_by_css_selector(
                    'span[data-testid="price-and-discounted-price"]'
                ).get_attribute('innerHTML').strip()
            
            try:
                hotel_score = deal_box.find_element_by_css_selector(
                    'div[aria-label*="Scored"]'
                ).get_attribute('innerHTML').strip()
            except:
                hotel_score = 'no'
            collection.append(
                [hotel_name, hotel_price, hotel_score]
            )
            print([hotel_name, hotel_price, hotel_score])
        return collection