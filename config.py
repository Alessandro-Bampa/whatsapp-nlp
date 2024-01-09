import calendar
import time

TRANSLATE_TO = 'en'
FORCE_TRANSLATE = False
OMITTED_MEDIA_STRING = "<Media omessi>"
INPUT_NAME = "test.txt"
TIMESTAMP = calendar.timegm(time.gmtime())
DESTINATION_PATH = "./output_%d" % TIMESTAMP
