#Code for calculating BiAffect Sensor Modalities from Raw Data
#2019

import math


class calc_modalities:

    def motion(self, array, health_code):
        square = 0
        motion_count = 0
        for row in array:
            if health_code in row["healthCode"]:
                square += math.sqrt(float(row["x"])**2 + float(row['y'])**2 + float(row['z'])**2)
                motion_count += 1
        if motion_count == 0:
            return None, None
        else:
            return motion_count, square/motion_count

    def keystoke_rates(self, array, health_code):
        all_rows_of_patient = 0
        backspace_count = 0
        autocorrection_count = 0
        for row in array:
            if health_code in row["healthCode"]:
                if row['keypress_type'] == 'backspace':
                    backspace_count += 1
                if row['keypress_type'] == 'autocorrection':
                    autocorrection_count += 1
                all_rows_of_patient += 1
        if all_rows_of_patient == 0:
            return None, None, None
        else:
            return all_rows_of_patient, backspace_count*100/all_rows_of_patient, autocorrection_count*100/all_rows_of_patient

    def average_interkey_delay(self, array, health_code):
        all_rows_of_patient = 0
        sum_of_delays = 0
        for row, next_row in zip(array, array[1:]):
            if health_code in row["healthCode"]:
                sum_of_delays += float(row['keypress_timestamp']) - float(next_row['keypress_timestamp'])
                all_rows_of_patient += 1
        if all_rows_of_patient == 0:
            return None
        else:
            return sum_of_delays/all_rows_of_patient

    def gonogo_error_rate(self, array, health_code):
        all_rows_of_patient = 0
        error_count = 0
        for row in array:
            if health_code in row["healthCode"]:
                if row['incorrect'] == 'True':
                    error_count += 1
                all_rows_of_patient += 1
        if all_rows_of_patient == 0:
            return None
        else:
            return error_count*100/all_rows_of_patient

