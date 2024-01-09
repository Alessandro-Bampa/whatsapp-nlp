import re


class WhatsappChatParser:

    def __init__(self, file_path: str, dest_path: str, omitted_media_str: str, encoding='utf-8'):
        self.file_path = file_path
        self.dest_path = dest_path
        self.omitted_media_str = omitted_media_str
        self.encoding = encoding

    def parse_file(self, write_on_file=False) -> list[str]:
        users_set = set()
        # ex: '04/01/24, 19:21 - John:'
        pattern = re.compile(r'(\d{2}/\d{2}/\d{2}, \d{2}:\d{2}) - (.*?): (.+)')
        with open(self.file_path, 'r', encoding=self.encoding) as file:
            rows_data = []
            current_row = []
            if write_on_file: output = open(self.dest_path, 'w+', encoding=self.encoding)
            for line in file:
                match = pattern.match(line)
                # Se trova una corrispondenza con il pattern, inizia un nuovo blocco di dati
                if match:

                    # elaboro i dati del blocco precedente prima di iniziare il possimo
                    if current_row and write_on_file:
                        output.write(''.join(current_row) + "\n")

                    #  -------------------------------------  #

                    # if is a Media ignore row
                    if self.omitted_media_str in line:
                        current_row = []
                        continue

                    current_user = match.group(2)
                    users_set.add(current_user)

                    # Questo if ha senso solo per il primo giro
                    if current_row:
                        # add previus row to data and clean current_row
                        rows_data.append(''.join(current_row).strip())
                        current_row = []

                # append current line
                if current_row:
                    current_row.append(' ' + line.strip())
                else:
                    current_row.append(line.strip())
                # current_row.append(re.sub(pattern, '', line))

            # Aggiungi l'ultimo blocco alla lista (se presente)
            if current_row:
                rows_data.append(''.join(current_row))
                if write_on_file:
                    output.write(''.join(current_row))
            if write_on_file:
                output.close()
            return rows_data

    def members(self):
        member_list = set()
        # ex: '04/01/24, 19:21 - John:'
        pattern = re.compile(r'(\d{2}/\d{2}/\d{2}, \d{2}:\d{2}) - (.*?): (.+)')
        [member_list.add(pattern.match(message).group(2)) for message in self.parse_file()]
        return member_list
