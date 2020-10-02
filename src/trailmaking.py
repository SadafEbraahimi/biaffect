#    Created by Sadaf Ebrahimi
#    sadafebraahimi@gmail.com


class Trailmaking:

    def __init__(self, analysis_data):
        self.trailmaking_error_rate = self.error_rate(analysis_data)

    def error_rate(self, analysis_data):
        error_count = 0
        column = 8
        if len(analysis_data) == 0:
            return ''
        else:
            for row in analysis_data:
                if row[column] == 'True':
                    error_count += 1
            return error_count*100/len(analysis_data)
