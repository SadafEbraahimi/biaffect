import os
import glob
import json
import arrow

folder_path = 'biaffect-survey-weekly-PHQ-9-v1'

NotAtAll = SeveralDays = MoreThanHalfTheDays = VeryDifficult = 0

with open(folder_path+'/metadata.json', 'r') as metadataFile:
    metadata = json.load(metadataFile)
    start = arrow.get(metadata["startDate"]).datetime.timestamp()
    end = arrow.get(metadata["endDate"]).datetime.timestamp()

for filename in glob.glob(os.path.join(folder_path, '*.json')):
    if filename == 'biaffect-survey-weekly-PHQ-9-v1\metadata.json' or filename == 'biaffect-survey-weekly-PHQ-9-v1\info.json':
        continue
    else:
        with open(filename, 'r') as f:
            data = json.load(f)
            fileStart = arrow.get(data["startDate"]).datetime.timestamp()
            fileEnd = arrow.get(data["endDate"]).datetime.timestamp()
            if fileStart >= start and fileEnd <= end:
                if data["answer"] == "Not at all":
                    NotAtAll += 1
                elif data["answer"] == "Several days":
                    SeveralDays += 1
                elif data["answer"] == "More than half the days":
                    MoreThanHalfTheDays += 1
                elif data["answer"] == "Very difficult":
                    VeryDifficult += 1
score = SeveralDays + MoreThanHalfTheDays*2 + VeryDifficult*3
print(score)


