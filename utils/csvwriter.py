from csv import DictWriter
import os


class CSVWriter():
    def __init__(self, file_name, headers):
        self.file_name = file_name
        self.headers = headers

    def write(self, values):
        with open(self.file_name, 'w', newline='', encoding='utf-8') as csv_file:
            writer = DictWriter(csv_file, fieldnames=self.headers)
            writer.writeheader()

            writer.writerows(values)
