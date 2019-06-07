#!/usr/bin/env python

import base64
import coloredlogs
import json
import hashlib
import logging as log
import os
import os.path
import pprint
from shutil import copyfile
import subprocess
import sys
import xlrd
coloredlogs.install()
pp = pprint.PrettyPrinter(compact=True)

log.basicConfig(level=log.INFO)

class SheetVerifier:
    def __init__(self, sheet):
        self.sheet = sheet
        self.ok = True
    
    def verify(self):
        self.check(0, 0, "Language name")
        self.check(0, 1)
        self.check(0, 2)
        self.check(1, 0, "AIATSIS code")
        self.check(1, 1)
        self.check(2, 0, "Speaker's name")
        self.check(2, 1)
        self.check(2, 2)
        self.check(3, 0, "Other people who helped to get the list produced")
        self.check(3, 1)
        self.check(4, 0, "Permission form received (Y/N)?")
        self.check(4, 1)
        self.check(5, 0, "Source")
        self.check(5, 1)
        self.check(6, 0, "Date received")
        self.check(6, 1)
        self.check(7, 1, 'Word')
        self.check(7, 2, 'Audio filename')
        for i in range(8, 65):
            self.check(i, 0)
            self.check(i, 1)
            self.check(i, 2)

    def check(self, row, column, value=None):
        if value and self.sheet.row_values(row)[column] != value:
            self.ok = False
            log.error(f"""Unexpected value in row: {row}, column: {column}."""
            f"""Expected: {value}, Got: {self.sheet.row_values(row)[column]}""")
        elif not self.sheet.row_values(row)[column]:
            log.warning(f"Empty cell found at row: {row+1}, column: {column+1}. Value expected.")

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
            data = {
                'english': row[0],
                'indigenous': row[1],
                'audio_file': row[2],
            }
            if len(row) == 4 and row[3]:
                data['english_alternate'] = row[3]
            return data

        for root, dirs, files in os.walk('data'):
            sheet = []
            for file in files:
                if 'xlsx' in file and not '~$' in file:
                    sheet.append(file)
            if root == 'data':
                continue
            print("")
            log.info(f"Processing: {root}")
            if len(sheet) > 1:
                log.error('Found more than one data spreadsheet. Skipping this folder.')
                continue
            sheet = sheet[0]
            sheet = os.path.join(root, sheet)
            with xlrd.open_workbook(sheet) as wb:
                sh = wb.sheet_by_index(0) 
                if (sh.nrows != 65):
                    log.error(f"{sheet} isn't exactly 65 rows - is it correct?")
                    continue

                log.info(f"Verifying {sheet}")
                v = SheetVerifier(sh)
                v.verify()
                if not v.ok:
                    log.error('Errors found in sheet - skipping this folder.')
                    continue

                log.info(f"Extracting language data from {sheet}")
                sheet = {
                    'language': {
                        'name': sh.row_values(0)[1],
                        'audio_file':  os.path.join(root, sh.row_values(0)[2]) if sh.row_values(0)[2] else ''
                    },
                    'code': sh.row_values(1)[1],
                    'words': [],
                    'speaker': {
                        'name': sh.row_values(2)[1],
                        'audio_file':  os.path.join(root, sh.row_values(2)[2]) if sh.row_values(2)[2] else ''
                    }, 
                    'thankyou': sh.row_values(3)[1]
                }
                # pp.pprint(sheet)
                if sheet['code'] not in self.data.keys():
                    log.error(f"{sheet['code']} not in AIATSIS-geography.xlsx")
                    continue

                log.info(f"Creating repository for {sh.row_values(1)[1]}")
                for r in range(8, sh.nrows):
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
        def get_target_name(path, file, ext):
            return os.path.join(path, os.path.splitext(os.path.basename(file))[0]) + ext

        def transcode(item, target):
            if not os.path.exists(target):
                log.info(f"Transcoding {item} to webm and mp3")
                subprocess.run(['ffmpeg', '-hide_banner', '-loglevel',  'panic', '-i', item, target])
            
        self.makepath(self.repository)
        for key, item in self.data.items():
            log.info(f"Building repository for {item['code']}")
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
                    transcode(item['language']['audio_file'], get_target_name(item_path, item['language']['audio_file'], '.webm'))
                    transcode(item['language']['audio_file'], get_target_name(item_path, item['language']['audio_file'], '.mp3'))
                    copyfile(item['language']['audio_file'], os.path.join(item_path, os.path.basename(item['language']['audio_file'])))
                    audio_files = [
                        get_target_name(item_path, item['language']['audio_file'], '.webm').replace('dist', ''),
                        get_target_name(item_path, item['language']['audio_file'], '.mp3').replace('dist', '')
                    ]
                    if 'wav' in item['language']['audio_file']:
                        audio_files.append(os.path.join(item_path, os.path.basename(item['language']['audio_file'])).replace('dist', ''))
                    item['language']['audio_file'] = audio_files
                        
                except FileNotFoundError: 
                    log.error(f"missing file {item['language']['audio_file']}")

            if 'speaker' in item and item['speaker']['audio_file']:
                try:
                    transcode(item['speaker']['audio_file'], get_target_name(item_path, item['speaker']['audio_file'], '.webm'))
                    transcode(item['speaker']['audio_file'], get_target_name(item_path, item['speaker']['audio_file'], '.mp3'))
                    copyfile(item['speaker']['audio_file'], os.path.join(item_path, os.path.basename(item['speaker']['audio_file'])))
                    audio_files = [
                        get_target_name(item_path, item['speaker']['audio_file'], '.webm').replace('dist', ''),
                        get_target_name(item_path, item['speaker']['audio_file'], '.mp3').replace('dist', '')
                    ]
                    if 'wav' in item['speaker']['audio_file']:
                        audio_files.append(os.path.join(item_path, os.path.basename(item['speaker']['audio_file'])).replace('dist', ''))
                    item['speaker']['audio_file'] = audio_files
                except FileNotFoundError: 
                    log.error(f"missing file {item['speaker']['audio_file']}")

            if 'words' in item.keys():
                words = []
                for word in item['words']:
                    if word['english'] not in self.words.keys():
                        self.words[word['english']] = []

                    if word['audio_file']:
                        try:
                            transcode(word['audio_file'], get_target_name(item_path, word['audio_file'], '.webm'))
                            transcode(word['audio_file'], get_target_name(item_path, word['audio_file'], '.mp3'))
                            copyfile(word['audio_file'], os.path.join(item_path, os.path.basename(word['audio_file'])))
                            audio_files = [
                                get_target_name(item_path, word['audio_file'], '.webm').replace('dist', ''),
                                get_target_name(item_path, word['audio_file'], '.mp3').replace('dist', '')
                            ]
                            if 'wav' in word['audio_file']:
                                audio_files.append(os.path.join(item_path, os.path.basename(word['audio_file'])).replace('dist', ''))
                            word['audio_file'] = audio_files
                        except FileNotFoundError: 
                            log.error(f"missing file {word['audio_file']}")

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

            