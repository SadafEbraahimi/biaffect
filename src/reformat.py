#    Created by Sadaf Ebrahimi
#    sadafebraahimi@gmail.com

import os
import csv
import glob
import numpy as np


class Reformat:

    def rename(self, folder_path, new_dir):
        old_new = []
        health_codes = []
        if "keystroke" in folder_path:
            col = 1
            prefix = 'keystroke'
        elif "trailmaking" in folder_path:
            col = 1
            prefix = 'trailmaking'
        elif "acceleration" in folder_path:
            col = 1
            prefix = 'acceleration'
        elif "gonogo" in folder_path:
            col = 3
            prefix = 'gonogo'
        #saving all file names in dir with their healthcodes in a list
        for filename in glob.glob(os.path.join(folder_path, '*.csv')):
            with open(filename, 'r') as csvfile:
                reader = csv.reader(csvfile, delimiter=',')
                header = next(reader)
                try:
                    health_code = np.array(next(reader))[col]
                except:
                    continue
                health_codes.append([os.path.basename(filename), health_code[1:-1]])
                old_new = np.array(health_codes)
        #renaming all files in dir with their healthcodes
        for row in old_new:
            old = folder_path+"/"+row[0]
            new = new_dir+"/"+prefix+"-"+row[1]+".csv"
            try:
                os.rename(old, new)
            except:
                new = new_dir + "/" + prefix + "-" + row[1] + "(1)" + ".csv"
                os.rename(old, new)

    def apply_dir_change(self):
        #change these direcotries to your local directories
        acc_dir = "data/acceleration"
        gonogo_dir = "data/gonogo"
        keystroke_dir = "data/keystroke"
        trailmaking_dir = "data/trailmaking"
        # creating new directories for renamed data
        new_dir = ["renamed_data", "renamed_data/acceleration", "renamed_data/gonogo",
                           "renamed_data/keystroke", "renamed_data/trailmaking"]
        for dir in new_dir:
            os.mkdir(dir)
        #renaming all files with their healthcode in new directory: /renamed_data
        self.rename(acc_dir, new_dir[1])
        self.rename(gonogo_dir, new_dir[2])
        self.rename(keystroke_dir, new_dir[3])
        self.rename(trailmaking_dir, new_dir[4])
