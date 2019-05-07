#Code for mergin files
#2019

import os
import glob
import csv

class merge:

    def merge_files(self, folder_path):
        analysisData = []
        for filename in glob.glob(os.path.join(folder_path, '*.csv')):
            opened_csv = csv.DictReader(open(filename, "r"), delimiter=",")
            for row in opened_csv:
                dict = {}
                for col in row:
                    #if col in redundant_cols:
                        #continue
                    dict.update({col: row[col]})
                analysisData.append(dict)
        return analysisData

