#!/usr/bin/env python

import base64
import json
import hashlib
import os
import os.path
import pprint
from shutil import copyfile
import xlrd
pp = pprint.PrettyPrinter(compact=True)

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
                'glotto_id': row[6]
            }


        print("Extracting geography data")
        with xlrd.open_workbook('data/AIATSIS-geography.xlsx') as wb:
            sh = wb.sheet_by_index(0)
            for r in range(1, sh.nrows):
                row = parse_row(sh.row_values(r))
                self.data[row['code']] = row
    
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
                if (sh.nrows != 66):
                    print(f"ERROR::: oops - {sheet} isn't exactly 66 rows - is it correct?")
                    continue

                sheet = {
                    'language': {
                        'name': sh.row_values(0)[1],
                        'audio_file':  os.path.join(root, sh.row_values(8)[2]) if sh.row_values(8)[2] else ''
                    },
                    'code': sh.row_values(1)[1],
                    'words': [],
                    'speaker': {
                        'name': sh.row_values(7)[1],
                        'audio_file':  os.path.join(root, sh.row_values(7)[2]) if sh.row_values(7)[2] else ''
                    }, 
                    'thankyou': sh.row_values(3)[1]
                }
                # pp.pprint(sheet)
                if sheet['code'] not in self.data.keys():
                    print(f"ERROR::: ooops - {sheet['code']} not in AIATSIS-geography.xlsx")
                    continue

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
            self.languages[item['code']] = { 
                'name': item['name'], 
                'code': item['code'] , 
                'lat': item['lat'], 
                'lng': item['lng'],
            }
            if 'speaker' in item:
                self.languages[item['code']]['speaker'] = item['speaker']
            self.makepath(item_path)

            self.languages[item['code']]['words'] = False

            if 'language' in item and item['language']['audio_file']:
                try:
                    copyfile(item['language']['audio_file'], os.path.join(item_path, os.path.basename(item['language']['audio_file'])))
                    item['language']['audio_file'] = os.path.join(item_path, os.path.basename(item['language']['audio_file'])).replace('dist', '')
                except FileNotFoundError: 
                    print(f"ERRROR::: missing file {item['language']['audio_file']}")

            if 'speaker' in item and item['speaker']['audio_file']:
                try:
                    copyfile(item['speaker']['audio_file'], os.path.join(item_path, os.path.basename(item['speaker']['audio_file'])))
                    item['speaker']['audio_file'] = os.path.join(item_path, os.path.basename(item['speaker']['audio_file'])).replace('dist', '')
                except FileNotFoundError: 
                    print(f"ERRROR::: missing file {item['speaker']['audio_file']}")

            if 'words' in item.keys():
                words = []
                for word in item['words']:
                    if word['english'] not in self.words.keys():
                        self.words[word['english']] = []

                    if word['audio_file']:
                        try:
                            copyfile(word['audio_file'], os.path.join(item_path, os.path.basename(word['audio_file'])))
                            word['audio_file'] = os.path.join(item_path, os.path.basename(word['audio_file'])).replace('dist', '')
                        except FileNotFoundError: 
                            print(f"ERRROR::: missing file {word['audio_file']}")

                    words.append(word)
                    word['language'] = item['name']
                    word['code'] = item['code']
                    self.words[word['english']].append(word)
                self.languages[item['code']]['words'] = True
                item['words'] = words

            with open(os.path.join(item_path, 'index.json'), 'w') as f:
                f.write(json.dumps(item))

    def makepath(self, path):
        try:
            os.makedirs(path)
        except:
            pass

    def write_master_indices(self):
        with open(f"{self.repository}/index.json", 'w') as f:
            f.write(json.dumps(self.data))

        with open(f"{self.repository}/languages.json", 'w') as f:
            f.write(json.dumps({ 'languages': [ item for (key, item) in self.languages.items() ] }))
        

        words = []
        for (key, item) in self.words.items():
            m = hashlib.sha256()
            m.update(key.encode())
            word = m.hexdigest()
            words.append({ 'name': item[0]['english'], 'index': f"{word}.json" })
            with open(f"{self.repository}/{word}.json", 'w') as f:
                f.write(json.dumps(item))

        with open(f"{self.repository}/words.json", 'w') as f:
            f.write(json.dumps({ 'words': words }))

if __name__ == "__main__":
    d = DataExtractor()
    d.extract()

            