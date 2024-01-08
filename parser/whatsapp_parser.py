import re

class WhatsappParser:

    def __init__(self, file_path: str, dest_path: str, omitted_media_str: str, encoding='utf-8'):
        self.file_path = file_path
        self.dest_path = dest_path
        self.omitted_media_str = omitted_media_str
        self.encoding = encoding

    def parse_file(self):
        users_set = set()
        # ex: '04/01/24, 19:21 - John:'
        pattern = re.compile(r'\d{2}/\d{2}/\d{2}, \d{2}:\d{2} - (.*?): ')
        with open(self.file_path, 'r', encoding=self.encoding) as file:
            rows_data = []
            current_data = []
            current_user = None
            for line in file:
                match = pattern.match(line)
                # Se trova una corrispondenza con il pattern, inizia un nuovo blocco di dati
                if match:
                    # elaboro i dati del blocco precedente prima di iniziare il possimo
                    current_user = match.group(1)
                    users_set.add(current_user)
                    # Questo if ha senso solo per il primo giro
                    if current_data:
                        rows_data.append(''.join(current_data))
                        current_data = []

                # Aggiungi la riga corrente al blocco corrente eliminando il prefisso con data, ora e utente
                current_data.append(re.sub(pattern, '', line))

            # Aggiungi l'ultimo blocco alla lista (se presente)
            if current_data:
                rows_data.append(''.join(current_data))

