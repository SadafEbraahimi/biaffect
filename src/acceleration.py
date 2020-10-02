#    Created by Sadaf Ebrahimi
#    sadafebraahimi@gmail.com

import decimal


class Acceleration:

    def __init__(self, analisys_data):
        self.motion_count, self.avg_motion = self.motion(analisys_data)

    def motion(self, analysis_data):
        decimal.getcontext().prec = 100
        square = decimal.Decimal(0)
        length = decimal.Decimal(0)
        if len(analysis_data) == 0:
            return '', ''
        else:
            for row in analysis_data:
                # x, y, z cols
                square += (decimal.Decimal(row[5])**2 + decimal.Decimal(row[6])**2 + decimal.Decimal(row[7])**2).sqrt()
                length += 1
            return length, square/length
