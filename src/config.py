class ChromeOptions:
    CHROME_DRIVER_PATH = "C:/chromedriver.exe"
    USER_DATA_PATH = "C:/Users/<USER>/AppData/Local/Google/Chrome/User Data"

class ProductDetails:
    KEYWORDS = ""
    COLOUR = ""
    SIZE = ""
    NEW = True

class UserDetails:
    NAME = ""
    EMAIL = ""
    TELE = ""
    ADDRESS_1 = ""
    ADDRESS_2 = ""
    ADDRESS_3 = ""
    CITY = ""
    POSTCODE = ""
    COUNTRY = "DE"                  # Two letter country code (i.e. Germany is "DE")

class PaymentDetails:
    CARD_NUMBER = ""
    CVV = ""
    EXP_MONTH = "01"                # Two digit month (i.e. January is "01")
    EXP_YEAR = "2022"               # Four digit year (2020)
