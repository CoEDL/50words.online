#!/usr/bin/env python

import base64
import json
import os
import os.path
from shutil import copyfile
import xlrd

class DataExtractor:
    def __init__(self):
        self.data = {}
        self.words = {}
        self.languages = {}
        self.repository = 'dist/repository'
    
    def extract(self):
        self.extract_aiatsis_geographies()
        self.extract_language_data()
        self.build_repository()
        self.write_master_indices()

    def extract_aiatsis_geographies(self):
        def parse_row(row):
            return {
                'code': row[0],
                'name': row[1],
                'lat': row[3],
                'lng': row[4],
                'asciiName': row[5],
                'glotto_id': row[6]
            }


        print("Extracting geography data")
        with xlrd.open_workbook('data/AIATSIS-geography.xlsx') as wb:
            sh = wb.sheet_by_index(0)  # or wb.sheet_by_name('name_of_the_sheet_here')
            for r in range(1, sh.nrows):
                row = parse_row(sh.row_values(r))
                self.data[row['code']] = row
            # with open('data/AIATSIS-geography.csv', 'w', newline="") as f:   # open('a_file.csv', 'w', newline="") for python 3
            #     c = csv.writer(f)
            #     for r in range(sh.nrows):
            #         print(sh.row_values(r))
            #         data[sh.row_values]
            #         c.writerow(sh.row_values(r))
    
    def extract_language_data(self):
        def parse_row(row):
            return {
                'english': row[0],
                'indigenous': row[1],
                'audio_file': row[2],
            }

        for root, dirs, files in os.walk('data'):
            for file in files:
                if 'xlsx' in file and not '~$' in file:
                    sheet = file 
            if root == 'data':
                continue
            sheet = os.path.join(root, sheet)
            print(f"Extracting language data from {sheet}")
            with xlrd.open_workbook(sheet) as wb:
                sh = wb.sheet_by_index(0)  # or wb.sheet_by_name('name_of_the_sheet_here')
                if (sh.nrows != 67):
                    print(f"ooops - {sheet} isn't exactly 67 rows - is it correct?")

                sheet = {
                    'language_name': sh.row_values(0)[1],
                    'code': sh.row_values(1)[1],
                    'words': []
                }
                print(f"Creating repository for {sh.row_values(1)[1]}")
                for r in range(10, sh.nrows):
                    data = parse_row(sh.row_values(r))
                    if data['audio_file']:
                        data['audio_file'] = os.path.join(root, data['audio_file'])
                    else:
                        data['audio_file'] = data['audio_file']

                    sheet['words'].append(data) 
            
            self.data[sheet['code']] = {
                **self.data[sheet['code']],
                **sheet,
                }
        
    def build_repository(self):
        self.makepath(self.repository)
        for key, item in self.data.items():
            item_path = os.path.join(self.repository, item['code'])
            self.languages[item['name']] = { 'name': item['name'], 'code': item['code'] , 'lat': item['lat'], 'lng': item['lng'] }
            self.makepath(item_path)

            if 'words' in item.keys():
                words = []
                for word in item['words']:
                    self.words[word['english']] = True
                    if word['audio_file']:
                        copyfile(word['audio_file'], os.path.join(item_path, os.path.basename(word['audio_file'])))
                        word['audio_file'] = os.path.join(item_path, os.path.basename(word['audio_file'])).replace('dist', '')
                    words.append(word)
                item['words'] = words

            with open(os.path.join(item_path, 'index.json'), 'w') as f:
                f.write(json.dumps(item))

    def makepath(self, path):
        try:
            os.makedirs(path)
        except:
            pass

    def write_master_indices(self):
        # print(self.data)
        with open(f"{self.repository}/index.json", 'w') as f:
            f.write(json.dumps(self.data))

        with open(f"{self.repository}/words.json", 'w') as f:
            f.write(json.dumps({ 'words': list(self.words.keys()) }))

        with open(f"{self.repository}/languages.json", 'w') as f:
            f.write(json.dumps({ 'languages': [ item for (key, item) in self.languages.items() ] }))


if __name__ == "__main__":
    d = DataExtractor()
    d.extract()

            