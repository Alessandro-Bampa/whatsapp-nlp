import re

import spacy
from googletrans import Translator
from pathlib import Path
from config import *
from nlp.sentiment_analysis import SentimentAnalysis
from parser.whatsapp_chat_parser import WhatsappChatParser

import logging

wh_file_path = Path('translation/wh_translation')

chat_rows_list = WhatsappChatParser(INPUT_NAME, DESTINATION_PATH, OMITTED_MEDIA_STRING).parse_file()
print(len(chat_rows_list))
translator = Translator()

nlp = spacy.load('en_core_web_lg')
nlp.add_pipe('spacytextblob')

# Traduco su un file la chat esportata

if FORCE_TRANSLATE or not wh_file_path.is_file():
    # TODO considerare di fare file multipli con timestamp uguale all'output parsato
    # TODO switch case per le varie piattaforme
    with open('translation/wh_translation', 'w+', encoding='utf-8') as tr_file:
        pattern = re.compile(r'(\d{2}/\d{2}/\d{2}, \d{2}:\d{2}) - (.*?): (.+)')
        for i, row in enumerate(chat_rows_list):
            match = pattern.match(row)
            text_translated = translator.translate(match.group(3), dest=TRANSLATE_TO).text
            complete_row = match.group(1) + " - " + match.group(2) + ": " + text_translated
            tr_file.write(complete_row + "\n")
            print(f'Translated {i+1} row')
        print('Translation file: wh_translation COMPLETED!')

wh_analysis = SentimentAnalysis(wh_file_path, 'whatsapp', nlp)

wh_analysis.get_sentiment()
