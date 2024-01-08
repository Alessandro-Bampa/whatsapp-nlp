# the following installations are required
# python -m textblob.download_corpora
# python -m spacy download en_core_web_sm

import spacy
from spacytextblob.spacytextblob import SpacyTextBlob

from googletrans import Translator

# Instantiate the translator object
translator = Translator()

# Translate the text "Hello, world!" from English to French
translation = translator.translate("20/02/23, 14:14 - Alessandro: <Media omessi>", dest='en').text

print(translation)

nlp = spacy.load('en_core_web_lg')

nlp.add_pipe('spacytextblob')
text = translation
doc = nlp(text)
# range [-1.0, 1.0]
print("Popolarity " + str(doc._.blob.polarity))
# 0.0 is very objective and 1.0 is very subjective.
print("Subjectivity " + str(doc._.blob.subjectivity))

print("sentiment_assessments.assessments " + str(doc._.blob.sentiment_assessments.assessments))

print("ngrams " + str(doc._.blob.ngrams()))