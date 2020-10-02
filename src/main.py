#    Created by Sadaf Ebrahimi
#    sadafebraahimi@gmail.com

import os
import csv
import sys
import glob
import numpy as np
import pandas as pd
from mdq import MDQ
from phq9 import PHQ9
from user import User
from gonogo import Gonogo
import datetime as datetime
from reformat import Reformat
from datetime import timezone
from keystroke import Keystroke
from trailmaking import Trailmaking
from datetime import datetime as dt
from acceleration import Acceleration

class Main:


    def fuse(self, time_span):

        #reformat = Reformat()
        #reformat.apply_dir_change()
        phq9_results = self.all_phq9()
        mdq_results = self.all_mdq()

        all_users = []
        header = ['Health Code', 'Start', 'End', 'Accelerometer Readings', 'Average Motion', 'Keystroke Count',
                  'Backspace Rate', 'Autocorrection Rate',
                  'Average Interkey Delay', 'Gonogo Error Rate', 'Trailmaking Error Rate', 'PHQ9 Score',
                  'Symptom Severity', 'Bipolar']
        all_users.append(header)

        start_periods = [datetime.time(0, 0, 0), datetime.time(6, 0, 0), datetime.time(12, 0, 0), datetime.time(18, 0, 0)]
        end_periods = [datetime.time(5, 59, 59), datetime.time(11, 59, 59), datetime.time(17, 59, 59), datetime.time(23, 59, 59)]

        file_count = 0
        empty = np.empty(shape=(0, 0))
        for ks_file in glob.glob(os.path.join("renamed_data/keystroke", '*.csv')):
            file_count += 1
            print("Starting calculation for {} {}/278".format(ks_file, file_count))
            health_code = (os.path.basename(ks_file).split('.')[0])[10:]  # just healthcode
            start, end, ks_df, acc_df, gng_df, tm_df, found_acc, found_gonogo, found_trailmaking =\
                self.load_data(ks_file, health_code, time_span)
            if time_span == '4rows':
                temp_start = 0
                end = 3
            if time_span == '6hours':
                temp_start = start
                temp_end = temp_start + 21599  # 6 hours
            elif time_span == '24hours':
                temp_start = start
                temp_end = temp_start + 86399  # 24 hours

            while temp_start <= end:

                results1 = results2 = results3 = results4 = pd.DataFrame([])

                if time_span == '6hours' or time_span == '24hours':
                    temp_df = ks_df.loc[(ks_df.keypress_timestamp >= temp_start) & (ks_df.keypress_timestamp <= temp_end)]
                elif time_span == '4rows':
                    temp_df = ks_df.loc[(ks_df.time >= start_periods[temp_start]) & (ks_df.time <= end_periods[temp_start])]

                results2 = results2.append(temp_df)
                results2 = results2.applymap(str)
                ks_data = np.array(results2)

                if found_acc == 1:
                    if time_span == '6hours' or time_span == '24hours':
                        temp_df = acc_df.loc[(acc_df.timestamp >= temp_start) & (acc_df.timestamp <= temp_end)]
                    elif time_span == '4rows':
                        temp_df = acc_df.loc[(acc_df.time >= start_periods[temp_start]) & (acc_df.time <= end_periods[temp_start])]
                    results1 = results1.append(temp_df)
                    results1 = results1.applymap(str)
                    acc_data = np.array(results1)
                else:
                    acc_data = empty
                if found_gonogo == 1:
                    if time_span == '6hours' or time_span == '24hours':
                        temp_df = gng_df.loc[(gng_df.startDate >= temp_start) & (gng_df.startDate <= temp_end)]
                    elif time_span == '4rows':
                        temp_df = gng_df.loc[(gng_df.time >= start_periods[temp_start]) & (gng_df.time <= end_periods[temp_start])]
                    results3 = results3.append(temp_df)
                    results3 = results3.applymap(str)
                    gng_data = np.array(results3)
                else:
                    gng_data = empty

                if found_trailmaking == 1:
                    if time_span == '6hours' or time_span == '24hours':
                        temp_df = tm_df.loc[(tm_df.startTime >= temp_start) & (tm_df.startTime <= temp_end)]
                    elif time_span == '4rows':
                        temp_df = tm_df.loc[(tm_df.time >= start_periods[temp_start]) & (tm_df.time <= end_periods[temp_start])]
                    results4 = results4.append(temp_df)
                    results4 = results4.applymap(str)
                    tm_data = np.array(results4)
                else:
                    tm_data = empty

                if time_span == '6hours' or time_span == '24hours':
                    user_start = dt.utcfromtimestamp(temp_start)
                    user_end = dt.utcfromtimestamp(temp_end)
                    phq9_score = PHQ9.most_recent_score(health_code, dt.utcfromtimestamp(temp_end).date(), phq9_results)
                    symptom_severity, bipolar = MDQ.most_recent_score(health_code, dt.utcfromtimestamp(temp_end).date(), mdq_results)
                elif time_span == '4rows':
                    user_start = start_periods[temp_start]
                    user_end = end_periods[temp_start]
                    np_phq9 = np.array(phq9_results)
                    try:
                        itemindex = np.where(np_phq9 == health_code)
                        phq9_score = np_phq9[itemindex[0][0], 3]
                    except:
                        phq9_score = ''

                    np_mdq = np.array(mdq_results)
                    try:
                        itemindex = np.where(np_mdq == health_code)
                        symptom_severity = np_mdq[itemindex[0][0], 3]
                        bipolar = np_mdq[itemindex[0][0], 4]
                    except:
                        symptom_severity = bipolar = ''

                acceleration = Acceleration(acc_data)
                keystroke = Keystroke(ks_data)
                gonogo = Gonogo(gng_data)
                trailmaking = Trailmaking(tm_data)
                phq9 = PHQ9(phq9_score)
                mdq = MDQ(symptom_severity, bipolar)

                user = User(health_code, user_start, user_end, keystroke, acceleration, gonogo, trailmaking, phq9, mdq)

                list = [user.health_code, user.start, user.end, user.acceleration.motion_count, user.acceleration.avg_motion,
                         user.keystroke.all_rows_of_patient, user.keystroke.backspace_rate, user.keystroke.autocorrection_rate,
                         user.keystroke.avg_interkey_delay, user.gonogo.gonogo_error_rate, user.trailmaking.trailmaking_error_rate,
                        user.phq9.score, user.mdq.symptom_severity, user.mdq.bipolar]

                if time_span == '4rows':
                    temp_start += 1
                elif time_span == '6hours':
                    temp_start = temp_end + 1
                    if temp_start == 1552176000:  # March 10, Daylight saving
                        temp_end = temp_start + 17999  # ToDo: Yadet raft payane dore ro dar nazar begiri
                    else:
                        temp_start = temp_end + 1
                        temp_end = temp_start + 21599
                elif time_span == '24hours':
                    temp_start = temp_end + 1
                    if temp_start == 1552176000:  # March 10, Daylight saving
                        temp_end = temp_start + 86399  # ToDo: Yadet raft payane dore ro dar nazar begiri
                    else:
                        temp_start = temp_end + 1
                        temp_end = temp_start + 86399

                all_users.append(list)

        # writing final results in csv file: look for final.csv in your root directory
        with open('outcome/' + time_span + '.csv', 'w', newline='') as writeFile:
            writer = csv.writer(writeFile)
            writer.writerows(all_users)



    def all_phq9(self):
        phq9_results = []
        with open('data/PHQ9V1.csv', 'r') as file:
            header = next(file)
            reader = csv.reader(file, delimiter=',')
            for row in reader:
                np_row = np.array(row)
                if np_row[19] != "":               #discouragement col
                    discouragement = np_row[19]
                elif row[23] != "":
                    discouragement = np_row[23]
                else:
                    continue
                try:
                    # anhedonia, depression, sleep, energy, appetite, concentration and speed cols
                    score = PHQ9.calculating_phq9(np_row[24], discouragement, np_row[14], np_row[15], np_row[16], np_row[17], np_row[18], np_row[20], np_row[21])
                except:
                    continue
                list = [row[6], row[5], row[0], score]  # healthCode, #uploadeDate, #ROW_ID and score cols
                phq9_results.append(list)
            print("phq9 calculated")

        return phq9_results

    def all_mdq(self):
        mdq_results = []
        with open('data/MDQv1.csv', 'r') as file:
            header = next(file)
            reader = csv.reader(file, delimiter=',')
            for row in reader:
                np_row = np.array(row)
                try:
                    # hyper, irritable, confidence, sleep, talkative, thoughts, distracted, energy, active, social, sex, unusual, money
                    symptom_severity, bipolar = MDQ.calculating_mdq(np_row[27], np_row[28], np_row[14], np_row[15], np_row[16],
                                                                    np_row[17], np_row[18], np_row[19], np_row[20], np_row[21],
                                                                    np_row[22], np_row[23], np_row[24], np_row[25], np_row[26])
                except:
                    continue
                list = [row[6], row[5], row[0], symptom_severity, bipolar]  #healthCode, uploadeDate, ROW_ID cols severity and bipolar
                mdq_results.append(list)
            print("mdq calculated")
        return mdq_results


    def load_data(self, ks_file, health_code, time_span):
        file_count = 0
        ks_df = acc_df = gng_df = tm_df = pd.DataFrame([])

        ks_df = pd.read_csv(ks_file, delimiter=',', error_bad_lines=False)
        timezone_diff = ks_df.iloc[0, 4] / 100 * 3600
        ks_df.keypress_timestamp = ks_df.keypress_timestamp + timezone_diff
        ks_df['time'] = ks_df.apply(lambda row: self.extract_time(row.keypress_timestamp), axis=1)

        start, end = self.calc_periods(ks_file, time_span)
        start = np.int64(start)
        end = np.int64(end)

        found_acc = 0
        found_gonogo = 0
        found_trailmaking = 0

        for filename in glob.glob(os.path.join("renamed_data/acceleration/", '*.csv')):
            if health_code in filename:
                found_acc = 1
                with open(filename, 'r') as file:
                    acc_df = pd.read_csv(file, delimiter=',', error_bad_lines=False)
                acc_df = acc_df.groupby('sessionDuration', as_index=False).nth(-1)
                timezone_diff = acc_df.iloc[0, 3] / 100 * 3600
                acc_df = acc_df.dropna(subset=['timestamp'])
                acc_df.timestamp = acc_df.timestamp + timezone_diff
                acc_df['time'] = acc_df.apply(lambda row: self.extract_time(row.timestamp), axis=1)
                break

        for filename in glob.glob(os.path.join("renamed_data/gonogo/", '*.csv')):
            if health_code in filename:
                found_gonogo = 1
                with open(filename, 'r') as file:
                    gng_df = pd.read_csv(file, delimiter=',', error_bad_lines=False)
                timezone_diff = gng_df.iloc[0, 2] / 100 * 3600
                gng_df['startDate'] = gng_df['startDate'].apply(
                    lambda x: (dt.strptime(x.split('.')[0], "%Y-%m-%dT%H:%M:%S")).replace(
                        tzinfo=timezone.utc).timestamp() + timezone_diff)
                gng_df['time'] = gng_df.apply(lambda row: self.extract_time(row.startDate), axis=1)
                break

        for filename in glob.glob(os.path.join("renamed_data/trailmaking/", '*.csv')):
            if health_code in filename:
                found_trailmaking = 1
                with open(filename, 'r') as file:
                    tm_df = pd.read_csv(file, delimiter=',', error_bad_lines=False)
                timezone_diff = tm_df.iloc[0, 4] / 100 * 3600
                tm_df.startTime = tm_df.startTime / 1000 + timezone_diff
                tm_df['time'] = tm_df.apply(lambda row: self.extract_time(row.startTime), axis=1)
                break

        return start, end, ks_df, acc_df, gng_df, tm_df, found_acc, found_gonogo, found_trailmaking

    def extract_time(self, x):
        return dt.utcfromtimestamp(x).time()

    def calc_periods(self, filename, string):
        results = pd.DataFrame([])
        sadaf = []
        with open(filename, 'r') as file:
            namedf = pd.read_csv(file, delimiter=',', error_bad_lines=False)
            results = results.append(namedf)
            results = results.applymap(str)
            analysis_data = np.array(results)

        timestamp_column = analysis_data[:, [5]]
        differ = int(int(analysis_data[0][4])/100) * 3600

        min_timestamp = int(float(np.amin(timestamp_column))) + differ
        max_timestamp = int(float(np.amax(timestamp_column))) + differ

        min_date_time = dt.utcfromtimestamp(min_timestamp)
        max_date_time = dt.utcfromtimestamp(max_timestamp)

        min_date = min_date_time.date()
        min_time = min_date_time.time()
        max_date = max_date_time.date()
        max_time = max_date_time.time()

        if string == "24hours":
            start = str(min_date) + " " + str(datetime.time(0, 0, 0))
            end = str(max_date) + " " + str(datetime.time(23, 59, 59))
            start_datetime_object = dt.strptime(start, '%Y-%m-%d %H:%M:%S')
            end_datetime_object = dt.strptime(end, '%Y-%m-%d %H:%M:%S')
            start_timestamp = start_datetime_object.replace(tzinfo=timezone.utc).timestamp()
            end_timestamp = end_datetime_object.replace(tzinfo=timezone.utc).timestamp()
            return start_timestamp, end_timestamp

        start_period1 = datetime.time(0, 0, 0)
        start_period2 = datetime.time(6, 0, 0)
        start_period3 = datetime.time(12, 0, 0)
        start_period4 = datetime.time(18, 0, 0)

        end_period1 = datetime.time(5, 59, 59)
        end_period2 = datetime.time(11, 59, 59)
        end_period3 = datetime.time(17, 59, 59)
        end_period4 = datetime.time(23, 59, 59)

        if min_time >= start_period1 and min_time <= end_period1:
            start = str(min_date) + " " + str(start_period1)
        elif min_time >= start_period2 and min_time <= end_period2:
            start = str(min_date) + " " + str(start_period2)
        elif min_time >= start_period3 and min_time <= end_period3:
            start = str(min_date) + " " + str(start_period3)
        elif min_time >= start_period4 and min_time <= end_period4:
            start = str(min_date) + " " + str(start_period4)

        if max_time >= start_period1 and max_time <= end_period1:
            end = str(max_date) + " " + str(end_period1)
        elif max_time >= start_period2 and max_time <= end_period2:
            end = str(max_date) + " " + str(end_period2)
        elif max_time >= start_period3 and max_time <= end_period3:
            end = str(max_date) + " " + str(end_period3)
        elif max_time >= start_period4 and max_time <= end_period4:
            end = str(max_date) + " " + str(end_period4)

        start_datetime_object = dt.strptime(start, '%Y-%m-%d %H:%M:%S')
        end_datetime_object = dt.strptime(end, '%Y-%m-%d %H:%M:%S')

        start_timestamp = start_datetime_object.replace(tzinfo=timezone.utc).timestamp()
        end_timestamp = end_datetime_object.replace(tzinfo=timezone.utc).timestamp()

        return start_timestamp, end_timestamp

if __name__ == "__main__":

    if len(sys.argv) != 2 or (sys.argv[1] != '6hours' and sys.argv[1] != '24hours' and sys.argv[1] != '4rows'):
        print("Please copy all the files into root directory, 'data' folder.\n"
              "Usage: python main.py <time span: 6hours, 24hours, 4rows>")
    else:
        time_span = sys.argv[1]
        main = Main()
        main.fuse(time_span)
