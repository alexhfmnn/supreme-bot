class ProductDetails:
    KEYWORDS = "Script Logos"
    COLOUR = "Tan"
    SIZE = "Medium"

class UserDetails:
    NAME = ""
    EMAIL = ""
    TELE = ""
    ADDRESS_1 = ""
    ADDRESS_2 = ""
    ADDRESS_3 = ""
    CITY = ""
    POSTCODE = ""

class PaymentDetails:
    CARD_NUMBER = ""
    CVV = ""
    CARD_TYPE = ""              # Ensure card type is either "Visa", "American Express", "Mastercard" or "Solo"
    EXP_MONTH = ""              # Two digit month (i.e. January is "01")
    EXP_YEAR = ""               # Four digit year (2020)
