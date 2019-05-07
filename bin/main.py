import csv
from bin.calc_modalities import calc_modalities
from bin.mdq import MDQ
from bin.phq9 import PHQ9
from bin.merge import merge

phq9 = PHQ9()
mdq = MDQ()
merge = merge()
calc_modalities = calc_modalities()

acceleration = merge.merge_files("acceleration")
keystrokes = merge.merge_files("keystroke")
gonogo = merge.merge_files("gonogo")

phq9_results = phq9.calculating_phq9()
mdq_results = mdq.calculating_mdq()

final_list = []
for mdq_row in mdq_results:
    for phq_row in phq9_results:
        dict = {}
        if mdq_row['healthCode'] == phq_row['healthCode'] and mdq_row['uploadDate'] == phq_row['uploadDate']:
            motion_count, avg_motion = calc_modalities.motion(acceleration, mdq_row['healthCode'])
            all_rows_of_patient, backspace_rate, autocorrection_rate = calc_modalities.keystoke_rates(keystrokes, mdq_row['healthCode'])
            average_interkey_delay = calc_modalities.average_interkey_delay(keystrokes, mdq_row['healthCode'])
            gonogo_error_rate = calc_modalities.gonogo_error_rate(gonogo, mdq_row['healthCode'])

            if avg_motion != None and all_rows_of_patient != None and gonogo_error_rate != None:
                dict.update({'healthCode': mdq_row['healthCode'], 'MDQ_Symptom_Severity': mdq_row['MDQ_Symptom_Severity'],
                             'phq9Score': phq_row['phq9Score'], 'MDQ_Bipolar_Bin': mdq_row['MDQ_Bipolar_Bin'],
                             'motion_count': motion_count, 'avg_motion': avg_motion, 'keystroke_count': all_rows_of_patient,
                             'backspace_rate': backspace_rate, 'autocorrection_rate': autocorrection_rate,
                             'average_interkey_delay': average_interkey_delay, 'gonogo_error_rate': gonogo_error_rate})
                final_list.append(dict)
            else:
                continue
for row in final_list:
    print(row)
with open('final.csv', 'w', newline='') as csvfile:
    header = final_list[0].keys()
    writer = csv.DictWriter(csvfile, fieldnames=header)
    writer.writeheader()
    writer.writerows(final_list)

