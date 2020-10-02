#    Created by Sadaf Ebrahimi
#    sadafebraahimi@gmail.com

import numpy as np
import pandas as pd


class PHQ9:

    def __init__(self, score):
        self.score = score

    @staticmethod
    def calculating_phq9(suicidality, *args):
        score = 0
        for arg in args:
            try:
                score += PHQ9.phq9_scoring(arg)
            except:
                raise ValueError()
        if suicidality != "":
            score += PHQ9.phq9_scoring(suicidality)
        else:
            score = score*9/8
        return score

    @staticmethod
    def phq9_scoring(string):
        if string == "Not at all" or string == "Not difficult at all":
            return 0
        elif string == "Several days":
            return 1
        elif string == "More than half the days":
            return 2
        elif string == "Nearly every day":
            return 3
        else:
            raise ValueError()

    @staticmethod
    def most_recent_score(health_code, date, analysis_data):
        scores_df = pd.DataFrame(analysis_data, columns=['healthCode', 'uploadeDate', 'ROW_ID', 'score cols'])
        scores_df = scores_df[scores_df.healthCode == health_code]
        scores_df = scores_df.loc[(scores_df.uploadeDate <= str(date))]
        if len(scores_df) == 0:
            return ''
        scores_df = scores_df.tail(1)
        sadaf = scores_df.applymap(str)
        goal_row = np.array(sadaf)
        return goal_row[0][3]

