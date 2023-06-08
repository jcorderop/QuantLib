"""
Created: 22.05.2023
Description:
    * This Module offers common functionality used for the OpenAPi personalization.
"""
__author__ = "OE - JC"
from app.util.config.ProjectSpecifics import *
__version__ = API_VERSION
__license__ = LICENSE

# Import modules
from enum import Enum


class Tags(Enum):
    yield_curve = "Yield Curve"
    option_pricing = "Option Pricing"
    market_data = "Market Data"
    fixed_income_pricing = "Fixed Income Pricing"
    user = "User"


API_PREFIX = '/api/v1'


DESCRIPTION = """
Oepfelbaum API main goal is to gather and share knowledge. 🚀

## Items

* Vanilla Option Pricer **European** and **American**.

## Contributors

* **Create users** (_not implemented_).
* **Read users** (_not implemented_).
"""

TITLE = "Oepfelbaum IT Management AG"
VERSION = API_VERSION
TERMS_OF_SERVICES = "https://www.oepfelbaum.com/#personen"
CONTACT = {
        "name": "Oepfelbaum Team",
        "url": "https://www.oepfelbaum.com/#kontakt",
        "email": "info@oepfelbaum.com",
    }
LICENSE_INFO = {
        "name": f'License: {LICENSE}',
        "url": LICENSE_URL,
    }
