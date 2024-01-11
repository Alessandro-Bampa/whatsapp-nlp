import datetime
import re
import json

import spacy
from spacy import Language
from spacytextblob.spacytextblob import SpacyTextBlob
from pathlib import Path


class SentimentAnalysis:

    def __init__(self, file_path: Path, platform: str, nlp: Language, encoding='utf-8', ):
        self.file_path = file_path  # salgo di una route
        self.encoding = encoding
        self.platform = platform
        self.nlp = nlp

    def get_sentiment(self):
        if not self.file_path.is_file():
            raise FileNotFoundError("Wrong file or file path")

        match self.platform:
            case "whatsapp":
                self.whatsapp_sentiment()
                print("SentimentAnalysis completed")
            case _:
                print("Platform not found")

    # {
    #     "date": "2023-08-02T12:00:00",
    #     "user": "Mario Rossi",
    #     "content": "I had a really horrible day. It was the worst day ever! But every now and then I have a really good day that makes me happy.",
    #     "popolarity": -0.125
    #     "Subjectivity": 0.9
    #     "sentiment": "positive"
    # }
    def whatsapp_sentiment(self):
        sentiment_result_list = []
        with open(self.file_path, 'r', encoding=self.encoding) as file:
            for i, line in enumerate(file):
                sentiment_result_list.append(self.get_wh_row_sentiment(line))
                print(f"line {i} has been processed")

        with open('data.json', 'w+', encoding='utf-8') as f:
            json.dump(sentiment_result_list, f, ensure_ascii=False, indent=4)

        return sentiment_result_list

    def get_wh_row_sentiment(self, row: str) -> dict:
        pattern = re.compile(r'(\d{2}/\d{2}/\d{2}, \d{2}:\d{2}) - (.*?): (.+)')
        match = pattern.match(row)
        if match:
            date_time_str = match.group(1)
            date_obj = datetime.datetime.strptime(date_time_str, "%d/%m/%y, %H:%M")
            # Convert the datetime object to ISO format
            iso_date = date_obj.isoformat()
            user = match.group(2)
            content = match.group(3)
            doc = self.nlp(content)
            polarity = doc._.polarity
            subjectivity = doc._.subjectivity
            assessments = doc._.assessments

            return {
                "date": iso_date,
                "user": user,
                "content": content,
                "polarity": polarity,
                "subjectivity": subjectivity,
                "assessments": assessments
            }
        else:
            # maybe raise an exception
            # If the row doesn't match the expected format, return an empty dictionary
            return {}
