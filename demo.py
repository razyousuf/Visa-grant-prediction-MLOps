from us_visa.logger import logging
from us_visa.exception import USvisaException
import sys

logging.info("This is to test the custom logging.")

try:
    a = 2/0
    print(a)
except Exception as e:
    raise USvisaException(e, sys)