from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
import time


def number_converter(self):
    multiplier = {
        "million": 1000000,
        "billion": 1000000000,
        "trillion": 1000000000000,
        "quadrillion": 1000000000000000,
    }

    words = self.split()
    for word in words:
        if word in multiplier:
            multiplier_value = multiplier[word]
            number = float(self.replace(word, "").strip())
            self = int(number * multiplier_value)

    return self


# Initialise Chrome
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

# Initialise driver
driver = webdriver.Chrome(options=chrome_options)
driver.get("https://orteil.dashnet.org/cookieclicker/")
driver.maximize_window()
actions = ActionChains(driver)

# Bypass cookies
consent_button = driver.find_element(By.CSS_SELECTOR, value=".fc-cta-consent")
consent_button.click()

time.sleep(2)

# Bypass language selection
english_button = driver.find_element(By.CSS_SELECTOR, value="#langSelect-EN")
english_button.click()

time.sleep(5)

# Define products
products = driver.find_elements(by=By.CSS_SELECTOR, value=".productName")
product_ids = [product.get_attribute("id") for product in products]

# Define game Stages
current_time = time.time()
timeout = time.time() + 3
early_game = current_time + 90
mid_game = current_time + 210
late_game = current_time + 600

while True:
    # Clicker
    big_button = driver.find_element(By.ID, value="bigCookie")
    big_button.click()
    big_button.click()

    # Check player cookie count
    if time.time() > timeout:
        money_element = driver.find_element(by=By.ID, value="cookies").text
        try:
            cookie_count = int(money_element.split()[0].replace(",", ""))
        except ValueError:
            cookie_count = number_converter(money_element)

        try:
            # UPGRADE PURCHASE SECTION
            upgrade = driver.find_element(By.ID, value="upgrade0")
            if "enabled" in upgrade.get_attribute("class"):
                upgrade.click()
        except NoSuchElementException:
            pass

        try:
            # PRODUCT PURCHASE SECTION
            # Gather all product costs
            all_prices = driver.find_elements(by=By.CSS_SELECTOR, value=".price")
            product_prices = []
            # Reformat the prices to int
            for price in all_prices:
                element_text = price.text
                if element_text != "":
                    try:
                        cost = int(element_text.strip().replace(",", ""))
                        product_prices.append(cost)
                    except ValueError:
                        cost = number_converter(element_text)
                        product_prices.append(cost)

            # Create product-price dictionary
            cookie_products = {}
            for n in range(len(product_prices)):
                cookie_products[product_prices[n]] = product_ids[n]

            # Check for products that are affordable
            affordable_products = {}
            for cost, id in cookie_products.items():
                if cookie_count > cost:
                    affordable_products[cost] = id

            # If the dictionary isn't empty, purchase the highest value one
            if affordable_products:
                highest_price_affordable_product = max(affordable_products)
                to_purchase_id = affordable_products[highest_price_affordable_product]
                item_to_purchase = driver.find_element(by=By.ID, value=to_purchase_id)
                actions.move_to_element(item_to_purchase).click().perform()

        except StaleElementReferenceException:
            pass

        # Set the next purchase time based on the game stage
        current_time = time.time()
        if current_time < early_game:
            timeout = time.time() + 4
        elif early_game <= current_time < mid_game:
            timeout = time.time() + 16
        elif mid_game <= current_time < late_game:
            timeout = time.time() + 64
        elif late_game <= current_time:
            timeout = time.time() + 128

# driver.quit()

