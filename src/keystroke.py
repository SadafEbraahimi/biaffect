#    Created by Sadaf Ebrahimi
#    sadafebraahimi@gmail.com


class Keystroke:

    def __init__(self, analysis_data):
        self.all_rows_of_patient, self.backspace_rate, self.autocorrection_rate = self.keystoke_rates(analysis_data)
        self.avg_interkey_delay = self.avg_interkey_delay(analysis_data)

    def keystoke_rates(self, analysis_data):
        backspace_count = 0
        autocorrection_count = 0
        if len(analysis_data) == 0:
            return '', '', ''
        else:
            for row in analysis_data:
                if row[6] == 'backspace':                   #keypress_type col
                    backspace_count += 1
                if row[6] == 'autocorrection':
                    autocorrection_count += 1
            return len(analysis_data), backspace_count*100/len(analysis_data), autocorrection_count*100/len(analysis_data)

    def avg_interkey_delay(self, analysis_data):
        sum_of_delays = 0
        if len(analysis_data) == 0:
            return ''
        else:
            for row, next_row in zip(analysis_data, analysis_data[1:]):
                if row[0] == next_row[0]:
                    sum_of_delays += abs(float(row[5]) - float(next_row[5]))        #keypres_timestamp col
                else:
                    continue
            return sum_of_delays/len(analysis_data)
