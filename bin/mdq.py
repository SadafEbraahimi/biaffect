#Code for scoring MDQ
#2019

import csv


class MDQ:

    def calculating_mdq(self):
        read_csv = csv.DictReader(open("MDQv1.csv", "r"), delimiter=",")
        analysisData = []
        included_cols = ['hyper', 'irritable', 'confidence', 'sleep', 'talkative', 'thoughts',
                         'distracted', 'energy', 'active', 'social', 'sex', 'unusual', 'money']
        for row in read_csv:
            symptom_severity = 0
            flag = True
            bipolar = "false"
            for col in included_cols:
                if row[col] in ("true", "false"):
                    symptom_severity += self.mdq_scoring(row[col])
                else:
                    flag = False
                    break
            if flag:
                if symptom_severity > 7 and row['multiple'] == "true" and row['problem'] in ("Serious Problem", "Moderate Problem"):
                    bipolar = "true"
                analysisData.append({"healthCode": row['healthCode'], "uploadDate": row['uploadDate'], "MDQ_Symptom_Severity": symptom_severity, "MDQ_Bipolar_Bin": bipolar})
        return analysisData

    def mdq_scoring(self, string):
        if string == "true":
            return 1
        elif string == "false":
            return 0


