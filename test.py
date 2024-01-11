# the following installations are required
# python -m textblob.download_corpora
# python -m spacy download en_core_web_sm
import re

import spacy
from spacytextblob.spacytextblob import SpacyTextBlob

from googletrans import Translator

# Instantiate the translator object
translator = Translator()
pattern = re.compile(r'(\d{2}/\d{2}/\d{2}, \d{2}:\d{2}) - (.*?): (.+)')

row = "21/02/23, 12:20 - Edo Baldan: Ho aperto il cofank della macchina e trovato una punta cicca nella batteria"
match = pattern.match(row)
# Translate the text "Hello, world!" from English to French
translation = translator.translate(match.group(3), dest='en').text
final_result = match.group(1) + " - " + match.group(2) + ": " + match.group(3)
print(match.groups())
print(match.group(3))
print(final_result)



# nlp = spacy.load('en_core_web_lg')
#
# nlp.add_pipe('spacytextblob')
# text = "I hate my job, I would like to tell everyone to fuck off"
# doc = nlp(text)
# # range [-1.0, 1.0]
# print("Popolarity " + str(doc._.blob.polarity))
# # 0.0 is very objective and 1.0 is very subjective.
# print("Subjectivity " + str(doc._.blob.subjectivity))
#
# print("sentiment_assessments.assessments " + str(doc._.blob.sentiment_assessments.assessments))
#
# print("ngrams " + str(doc._.blob.ngrams()))
