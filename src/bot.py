from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium import webdriver
import requests
import json
import time
import re
from tabulate import tabulate
from config import ProductDetails, UserDetails, PaymentDetails, ChromeOptions
from exceptions import ProductDoesntExist, SizeUnavailable, ItemSoldOut

headers = {'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, '
                         'like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1'}

mobile_emulation = {
    "deviceMetrics": {"width": 360, "height": 640, "pixelRatio": 3.0},
    "userAgent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) "
                 "Version/13.0.3 Mobile/15E148 Safari/604.1"}

prefs = {'disk-cache-size': 4096}

options = Options()
options.add_argument("user-data-dir=" + ChromeOptions.USER_DATA_PATH)
options.add_experimental_option("mobileEmulation", mobile_emulation)
options.add_experimental_option('prefs', prefs)
options.add_experimental_option("useAutomationExtension", False)

caps = DesiredCapabilities().CHROME
caps["pageLoadStrategy"] = "eager"

driver = webdriver.Chrome(desired_capabilities=caps, options=options, executable_path=ChromeOptions.CHROME_DRIVER_PATH)
wait = WebDriverWait(driver, 10)
session = requests.Session()


def get_new_items():
    """
    Get upcoming released items and return their names, colours and sizes as a table
    """

    driver.close()
    driver.quit()

    url = 'https://www.supremenewyork.com/mobile_stock.json'

    output = session.get(url=url, headers=headers, timeout=10).json()
    release_date = time.strftime('%d.%M.%Y', time.strptime(output['release_date'], '%M/%d/%Y'))
    new_items = []
    for item in output['products_and_categories']['new']:
        new_item = [release_date]
        new_item.append(re.sub('<br>', '', item['name']))
        new_item.append(str(item['price_euro'])[:-2] + ",00€")
        url = 'https://www.supremenewyork.com/shop/' + str(item['id']) + '.json'
        item_specs = session.get(url=url, headers=headers, timeout=10).json()

        colours = []
        for colour in item_specs['styles']:
            colours.append(colour['name'])
        colours = ", ".join(colours)
        new_item.append(colours)


        sizes = []
        for size in item_specs['styles'][0]['sizes']:
            sizes.append(size['name'])
        sizes = ", ".join(sizes)
        new_item.append(sizes)

        new_items.append(new_item)

    print(tabulate(new_items, headers=["Release Date", "Product Name", "Price", "Colours", "Sizes"]))


def find_newitem_id(name):
    """
    Find newly added Item on Supreme web-store and return its unique item ID
    """

    url = 'https://www.supremenewyork.com/mobile_stock.json'

    output = session.get(url=url, headers=headers, timeout=10).json()

    for item in output['products_and_categories']['new']:
        if name.lower() in item['name'].lower():
            return item['id']

    close_driver()
    raise ProductDoesntExist(name)


def find_item_id(name):
    """
    Find Item on Supreme web-store and return its unique item ID
    """

    url = 'https://www.supremenewyork.com/mobile_stock.json'

    output = session.get(url=url, headers=headers, timeout=10).json()

    for category in output['products_and_categories']:
        for item in output['products_and_categories'][category]:
            if name.lower() in item['name'].lower():
                return item['id']

    close_driver()
    raise ProductDoesntExist(name)


def find_item(product_id, colour, size):
    """
    Finds and returns the unique colour ID for the chosen item
    """

    url = 'https://www.supremenewyork.com/shop/' + str(product_id) + '.json'

    output = session.get(url=url, headers=headers, timeout=10).json()

    for product_colours in output['styles']:
        if colour.lower() in product_colours['name'].lower():
            for product_size in product_colours['sizes']:
                if size.lower() in product_size['name'].lower():
                    return product_colours['id']


def get_product(product_id, product_colour_id, size):
    """
    Opens Chrome instance and adds product to card
    """

    url = 'https://www.supremenewyork.com/mobile/#products/' + str(product_id) + '/' + str(product_colour_id)

    driver.get(url)

    # wait.until(EC.presence_of_element_located((By.ID, 'style-image')))
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'cart-button')))

    if (size):
        options = Select(driver.find_element_by_id('size-options'))
        try:
            options.select_by_visible_text(size)
        except NoSuchElementException:
            close_driver()
            SizeUnavailable(product_id)

    if (not driver.find_elements(By.CLASS_NAME, 'sold-out')):
        driver.find_element_by_class_name('cart-button').click()
    else:
        close_driver()
        raise ItemSoldOut(product_id)

    wait.until(EC.element_to_be_clickable((By.ID, 'checkout-now')))


def checkout():
    """
    Inputs checkout details
    """

    driver.get('https://www.supremenewyork.com/mobile/#checkout')

    wait.until(EC.presence_of_element_located((By.ID, 'order_billing_name')))
    driver.execute_script(
        f'document.getElementById("order_billing_name").value="{UserDetails.NAME}";'
        f'document.getElementById("order_email").value="{UserDetails.EMAIL}";'
        f'document.getElementById("order_tel").value="{UserDetails.TELE}";'
        f'document.getElementById("order_billing_address").value="{UserDetails.ADDRESS_1}";'
        f'document.getElementById("order_billing_address_2").value="{UserDetails.ADDRESS_2}";'
        f'document.getElementById("order_billing_address_3").value="{UserDetails.ADDRESS_3}";'
        f'document.getElementById("order_billing_city").value="{UserDetails.CITY}";'
        f'document.getElementById("order_billing_zip").value="{UserDetails.POSTCODE}";'
        f'document.getElementById("credit_card_number").value="{PaymentDetails.CARD_NUMBER}";'
        f'document.getElementById("credit_card_cvv").value="{PaymentDetails.CVV}";'
    )

    card_month = Select(driver.find_element_by_id('credit_card_month'))
    card_month.select_by_value(str(PaymentDetails.EXP_MONTH))

    card_year = Select(driver.find_element_by_id('credit_card_year'))
    card_year.select_by_value(str(PaymentDetails.EXP_YEAR))

    driver.find_element_by_id('order_terms').click()

    driver.find_element_by_id('submit_button').click()


def close_driver():
    session.close()
    driver.close()
    driver.quit()


def buy():
    if (ProductDetails.NEW):
        product_id = find_newitem_id(ProductDetails.KEYWORDS)
    else:
        product_id = find_item_id(ProductDetails.KEYWORDS)
    product_colour_id = find_item(product_id, ProductDetails.COLOUR, ProductDetails.SIZE)
    get_product(product_id, product_colour_id, ProductDetails.SIZE)
    checkout()




if __name__ == '__main__':
#    t1 = time.time()
#    get_new_items()
    buy()
#    t0 = time.time()
#    print('TIME: ', t0 - t1)
