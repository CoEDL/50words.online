# /usr/bin/env python

import base64
import coloredlogs
from datetime import datetime
import json
import hashlib
import logging as log
import os
import os.path
import pprint
from shutil import copyfile
import subprocess
import sys
from types import SimpleNamespace
import xlrd

coloredlogs.install()
pp = pprint.PrettyPrinter(compact=True)

log.basicConfig(level=log.INFO)


class SheetVerifier:
    def __init__(self, sheet, sheet_name):
        self.sheet_name = sheet_name
        self.sheet = sheet
        self.ok = True
        self.errors = []

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
        self.check(7, 1, "Word")
        self.check(7, 2, "Audio filename")
        for i in range(8, 65):
            self.check(i, 0)
            self.check(i, 1)
            self.check(i, 2)
        return self.errors

    def check(self, row, column, value=None):
        if value and self.sheet.row_values(row)[column] != value:
            self.ok = False
            self.errors.append(
                {
                    "type": "Sheet verification incorrect data",
                    "level": "error",
                    "msg": f"'{self.sheet_name}': Unexpected value in row: {row}, column: {column}. Expected: {value}, Got: {self.sheet.row_values(row)[column]}",
                }
            )
        elif not self.sheet.row_values(row)[column]:
            self.errors.append(
                {
                    "type": "Sheet verification missing data",
                    "level": "warning",
                    "msg": f"'{self.sheet_name}': Empty cell found at row: {row+1}, column: {column+1}. Value expected.",
                }
            )


class DataExtractor:
    def __init__(self):
        self.aiatsis_geographies = {}
        self.gambay_geographies = {}
        self.data = {}
        self.words = {}
        self.languages = {}
        self.gambay_additions = []
        self.errors = []
        self.data_path = "/srv/data"
        self.repository = "/srv/dist/repository"
        self.gambay_geographies_geojson = "/srv/data/gambay-languages.geojson"

    def extract(self):
        self.extract_aiatsis_geographies()
        self.extract_gambay_geographies()
        self.map_gambay_and_aiatsis_geographies()
        self.extract_language_data()
        self.build_repository()
        self.write_master_indices()

    def extract_aiatsis_geographies(self):
        def parse_row(row):
            return {
                "code": row[0],
                "name": row[1],
                "lat": row[3],
                "lng": row[4],
                "glottoid": row[6],
            }

        print("Extracting geography data")
        with xlrd.open_workbook(f"{self.data_path}/AIATSIS-geography.xlsx") as wb:
            sh = wb.sheet_by_index(0)
            for r in range(1, sh.nrows):
                row = parse_row(sh.row_values(r))
                self.aiatsis_geographies[row["name"]] = row
        # for item in self.aiatsis_geographies.items():
        #     pp.pprint(item)

    def extract_gambay_geographies(self):
        with open(self.gambay_geographies_geojson, "r") as f:
            gambay_data = json.load(f)

        for language in gambay_data["features"]:
            language_name = language["properties"]["name"]
            self.gambay_geographies[language_name] = language
        # for item in self.gambay_geographies.items():
        #     pp.pprint(item)

    def map_gambay_and_aiatsis_geographies(self):
        def add(prop, feature, data, language_name):
            addition = []
            if prop not in feature["properties"] and data:
                addition = [{"property": prop, "value": data, "name": language_name}]
                feature["properties"][prop] = data
            return (addition, feature)

        for (language_name, language) in self.gambay_geographies.items():
            language["properties"]["source"] = "Gambay"
            if "code" in language["properties"]:
                self.data[language["properties"]["code"]] = language
            else:
                if language_name in self.aiatsis_geographies:
                    if self.aiatsis_geographies[language_name]["code"]:
                        (additions, language) = add(
                            "code",
                            language,
                            self.aiatsis_geographies[language_name]["code"],
                            language_name,
                        )
                        self.gambay_additions.extend(additions)
                        self.data[language["properties"]["code"]] = language
                    else:
                        self.errors.append(
                            {
                                "type": "Missing code in Austlang",
                                "level": "error",
                                "msg": f"Gambay language '{language_name}' found in Austlang but no code was present - language excluded",
                            }
                        )
            # self.errors.append(
            #     {
            #         "type": "Gambay language excluded",
            #         "level": "error",
            #         "msg": f"Gambay language '{language_name}' has not been included",
            #     }
            # )
            # else:
            #     self.errors.append(
            #         {
            #             "type": "Gambay name not found in Austlang",
            #             "level": "error",
            #             "msg": f"'{language_name}' not found in AIATSIS-geographies.xlsx - language excluded",
            #         }
            #     )
            # self.errors.append(
            #     {
            #         "type": "Gambay language excluded",
            #         "level": "error",
            #         "msg": f"Gambay language '{language_name}' has not been include",
            #     }
            # )

        # self.data = {}
        # for language in languages:
        #         self.data[language["properties"]["code"]] = language
        # for data in self.data.items():
        #     print(data)

    def extract_language_data(self):
        def parse_row(row):
            data = {
                "english": row[0],
                "indigenous": row[1].lower(),
                "audio_file": row[2],
            }
            if len(row) == 4 and row[3]:
                data["english_alternate"] = row[3]
            return data

        for root, dirs, files in os.walk(self.data_path):
            sheet = []
            for file in files:
                if "xlsx" in file and not "~$" in file:
                    sheet.append(file)
            if root == "/srv/data":
                continue
            log.info(f"Processing: {root}")
            if len(sheet) > 1:
                self.errors.append(
                    {
                        "type": "Multiple spreadsheets",
                        "level": "error",
                        "msg": f"Found more than one data spreadsheet in folder '{root}'. Skipping this folder.",
                    }
                )
                continue
            sheet = sheet[0]
            sheet = os.path.join(root, sheet)
            with xlrd.open_workbook(sheet) as wb:
                sh = wb.sheet_by_index(0)
                if sh.nrows != 65:
                    self.errors.append(
                        {
                            "type": "Bad spreadsheet",
                            "level": "error",
                            "msg": f"'{sheet}' in '{root}' isn't exactly 65 rows - is it correct?",
                        }
                    )
                    continue

                log.info(f"Verifying {sheet}")
                v = SheetVerifier(sh, sheet)
                errors = v.verify()
                self.errors.extend(errors)
                if not v.ok:
                    log.error("Errors found in sheet - skipping this folder.")
                    continue

                log.info(f"Extracting language data from {sheet}")
                sheet = {
                    "language": {
                        "name": sh.row_values(0)[1].strip(),
                        "audio_file": os.path.join(root, sh.row_values(0)[2].strip())
                        if sh.row_values(0)[2]
                        else "",
                    },
                    "date_received": sh.row_values(6)[1],
                    "code": sh.row_values(1)[1].strip(),
                    "words": [],
                    "speaker": {
                        "name": sh.row_values(2)[1].strip(),
                        "audio_file": os.path.join(root, sh.row_values(2)[2].strip())
                        if sh.row_values(2)[2].strip()
                        else "",
                    },
                    "thankyou": sh.row_values(3)[1].strip(),
                }
                if sheet["code"] not in self.data.keys():
                    try:
                        if self.aiatsis_geographies[sheet["language"]["name"]]:
                            aiatsis_data = self.aiatsis_geographies[
                                sheet["language"]["name"]
                            ]
                            self.data[sheet["code"]] = {
                                "geometry": {
                                    "coordinates": [
                                        aiatsis_data["lng"],
                                        aiatsis_data["lat"],
                                    ],
                                    "type": "Point",
                                },
                                "properties": {
                                    "source": "Austlang",
                                    "code": aiatsis_data["code"],
                                    "name": aiatsis_data["name"],
                                },
                                "type": "Feature",
                            }
                            self.errors.append(
                                {
                                    "type": "Using Austlang data",
                                    "level": "warning",
                                    "msg": f"Using AIATAIS data for '{sheet['code']}' '{sheet['language']['name']}'",
                                }
                            )
                    except KeyError as e:
                        self.errors.append(
                            {
                                "type": f"Language not found in Gambay or Austlang",
                                "level": "error",
                                "msg": f"'{sheet['code']}' '{sheet['language']['name']}' not found in either the Gambay or Austlang data",
                            }
                        )
                        continue

                for r in range(8, sh.nrows):
                    data = parse_row(sh.row_values(r))
                    if data["audio_file"]:
                        data["audio_file"] = os.path.join(root, data["audio_file"])
                    else:
                        data["audio_file"] = data["audio_file"]

                    sheet["words"].append(data)

                self.data[sheet["code"]]["properties"] = {
                    **sheet,
                    **self.data[sheet["code"]]["properties"],
                }

    def build_repository(self):
        def get_target_name(path, file, ext):
            return os.path.join(path, os.path.splitext(os.path.basename(file))[0]) + ext

        def transcode(item, target, format):
            if not os.path.exists(target):
                log.info(f"Transcoding {item} to {format}")
                subprocess.run(
                    ["ffmpeg", "-hide_banner", "-loglevel", "panic", "-i", item, target]
                )

        def transcode_and_copy_to_repository(item_path, audio_file):
            if not audio_file:
                return []

            if "wav" not in audio_file:
                self.errors.append(
                    {
                        "type": "Incorrect audio format",
                        "level": "warning",
                        "msg": f"'{audio_file}' is not a 'wav' file. I'll work with this but you should provide 'wav' files as input",
                    }
                )
            try:
                transcode(
                    audio_file, get_target_name(item_path, audio_file, ".webm"), "webm"
                )
                transcode(
                    audio_file, get_target_name(item_path, audio_file, ".mp3"), "mp3"
                )
                audio_files = [
                    get_target_name(item_path, audio_file, ".webm").replace(
                        "/srv/dist", ""
                    ),
                    get_target_name(item_path, audio_file, ".mp3").replace(
                        "/srv/dist", ""
                    ),
                ]
                if "wav" in audio_file:
                    copyfile(
                        audio_file,
                        os.path.join(item_path, os.path.basename(audio_file)),
                    )
                    audio_files.append(
                        os.path.join(item_path, os.path.basename(audio_file)).replace(
                            "/srv/dist", ""
                        )
                    )
                return audio_files

            except FileNotFoundError:
                self.errors.append(
                    {
                        "type": "Audio file missing",
                        "level": "error",
                        "msg": f"{audio_file} not found",
                    }
                )

        def push_to_words(word, item):
            item = {**item}
            if word["english"] not in self.words:
                self.words[word["english"]] = []
            # item["word"] = word
            # if "words" in item["properties"]:
            #     del item["properties"]["words"]
            word["language"] = {
                "code": item["properties"]["code"],
                "name": item["properties"]["name"],
            }
            item["properties"] = word
            # pp.pprint(item)
            self.words[word["english"]].append(item)

        self.makepath(self.repository)
        for key, item in self.data.items():
            item_geometry = SimpleNamespace(**item["geometry"])
            item_properties = SimpleNamespace(**item["properties"])

            log.info(f"Building repository for {item_properties.code}")
            item_path = os.path.join(self.repository, item_properties.code)
            self.makepath(item_path)

            self.languages[item_properties.code] = item

            if "speaker" in item["properties"]:
                item["properties"]["speaker"][
                    "audio_file"
                ] = transcode_and_copy_to_repository(
                    item_path, item_properties.speaker["audio_file"]
                )
                # pp.pprint(item["properties"]["speaker"])

            if "language" in item["properties"]:
                item["properties"]["language"][
                    "audio_file"
                ] = transcode_and_copy_to_repository(
                    item_path, item_properties.language["audio_file"]
                )
                # pp.pprint(item["properties"]["language"])

            if "words" in item["properties"]:
                words = []
                for word in item_properties.words:
                    word["audio_file"] = transcode_and_copy_to_repository(
                        item_path, word["audio_file"]
                    )
                    push_to_words(word, item)
                    words.append(word)
                    # pp.pprint(word)
                item["properties"]["words"] = words
                # pp.pprint(item["properties"]["words"])

            # pp.pprint(item)
            with open(os.path.join(item_path, "index.json"), "w") as f:
                f.write(json.dumps(item))

    def makepath(self, path):
        try:
            os.makedirs(path)
        except:
            pass

    def write_master_indices(self):
        languages = []
        for (code, language) in self.languages.items():
            language["properties"]["words"] = (
                True if "words" in language["properties"] else False
            )
            languages.append(language)

        with open(f"{self.repository}/languages.json", "w") as f:
            f.write(json.dumps({"languages": languages}))

        words = []
        for (key, word) in self.words.items():
            m = hashlib.sha256()
            m.update(key.encode())
            index = m.hexdigest()
            words.append({"name": key, "index": f"{index}.json"})
            with open(f"{self.repository}/{index}.json", "w") as f:
                f.write(json.dumps(word))

        with open(f"{self.repository}/words.json", "w") as f:
            f.write(json.dumps({"words": words}))

        with open(f"{self.repository}/errors.json", "w") as f:
            f.write(
                json.dumps(
                    {
                        "date": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
                        "errors": self.errors,
                    }
                )
            )
        with open(f"{self.repository}/gambay-additions.json", "w") as f:
            f.write(
                json.dumps(
                    {
                        "date": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
                        "additions": self.gambay_additions,
                    }
                )
            )


if __name__ == "__main__":
    d = DataExtractor()
    d.extract()
