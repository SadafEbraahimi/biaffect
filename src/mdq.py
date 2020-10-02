#    Created by Sadaf Ebrahimi
#    sadafebraahimi@gmail.com

import numpy as np
import pandas as pd


class MDQ:

    def __init__(self, symptom_severity, bipolar):
        self.symptom_severity = symptom_severity
        self.bipolar = bipolar

    @staticmethod
    def calculating_mdq(multiple, problem, *args):
        symptom_severity = 0
        bipolar = "false"
        for arg in args:
            if arg in ("true", "false"):
                symptom_severity += MDQ.mdq_scoring(arg)
            else:
                raise ValueError()
        if symptom_severity > 7 and multiple == "true" and problem in ("Serious Problem", "Moderate Problem"):
            bipolar = "true"
        return symptom_severity, bipolar

    @staticmethod
    def mdq_scoring(string):
        if string == "true":
            return 1
        elif string == "false":
            return 0

    @staticmethod
    def most_recent_score(health_code, date, analysis_data):
        scores_df = pd.DataFrame(analysis_data, columns=['healthCode', 'uploadeDate', 'ROW_ID', 'symptom_severity', 'bipolar'])
        scores_df = scores_df[scores_df.healthCode == health_code]
        scores_df = scores_df.loc[(scores_df.uploadeDate <= str(date))]
        if len(scores_df) == 0:
            return '', ''
        scores_df = scores_df.tail(1)
        sadaf = scores_df.applymap(str)
        goal_row = np.array(sadaf)
        return goal_row[0][3], goal_row[0][4]

