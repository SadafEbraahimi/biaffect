#Code for scoring PHQ9
#2019

import csv


class PHQ9:

    def calculating_phq9(self):
        read_csv = csv.DictReader(open("PHQ9V1.csv", "r"), delimiter=",")
        analysisData = []
        included_cols = ['anhedonia', 'depression', 'sleep', 'energy', 'appetite', 'concentration', 'speed']
        for row in read_csv:
            score = 0
            if row['discouragement'] != "":
                score += self.phq9_scoring(row['discouragement'])
            elif row['discouraged'] != "":
                score += self.phq9_scoring(row['discouraged'])
            else:
                continue
            for col in included_cols:
                score += self.phq9_scoring(row[col])
            if score < 0:
                continue
            else:
                if row['suicidality'] != "":
                    score += self.phq9_scoring(row['suicidality'])
                else:
                    score = score*9/8
                analysisData.append({"healthCode": row['healthCode'], "uploadDate": row['uploadDate'], "phq9Score": score})
        return analysisData

    def phq9_scoring(self, string):
        if string == "Not at all" or string == "Not difficult at all":
            return 0
        elif string == "Several days":
            return 1
        elif string == "More than half the days":
            return 2
        elif string == "Nearly every day":
            return 3
        else:
            return -10000


