import sys
import json
import csv
from datetime import datetime


class Parser:

    def to_string(self, string):
        try:
            return str(string)
        except:
            return string.encode('utf-8')

    def reduce_nest(self, key, value, reduced_nest):

        #Reduction Condition 1
        if type(value) is list:
            i = 0
            for sub_item in value:
                self.reduce_nest(key + '_' + self.to_string(i), sub_item)
                i = i + 1

        #Reduction Condition 2
        elif type(value) is dict:
            sub_keys = value.keys()
            for sub_key in sub_keys:
                self.reduce_nest(key + '_' + self.to_string(sub_key), value[sub_key], reduced_nest)

        #Base Condition
        else:
            if "timestamp" in key:
                reduced_nest[self.to_string(key)] = self.to_string(datetime.fromtimestamp(value))
            else:
                reduced_nest[self.to_string(key)] = self.to_string(value)

        return reduced_nest

    def json_to_csv(self, node, json_file_path, csv_file_path):
        fp = open(json_file_path, 'r')
        json_value = fp.read()
        file_data = json.loads(json_value)
        fp.close()
        try:
            data_to_be_processed = file_data[node]
        except:
            data_to_be_processed = file_data

        processed_data = []
        header = []
        for item in data_to_be_processed:
            print(item)
            reduced_nest = {}
            self.reduce_nest(node, item, reduced_nest)

            header += reduced_nest.keys()
            processed_data.append(reduced_nest)

        header = list(set(header))
        header.sort()

        with open(csv_file_path, 'w', newline='') as file:
            writer = csv.DictWriter(file, header, quoting=csv.QUOTE_ALL)
            writer.writeheader()
            for row in processed_data:
                writer.writerow(row)

        print("Yay! {0} is ready with {1} columns.".format(csv_file_path, len(header)))


if __name__ == "__main__":

    if len(sys.argv) != 5:
        print("Usage: python parser.py <node_name> <json_in_file_path> <output format: type csv for now> <csv_out_file_path>")

    else:
        node = sys.argv[1]
        json_file_path = sys.argv[2]
        output_format = sys.argv[3]
        csv_file_path = sys.argv[4]
        new_parser = Parser()

        if output_format == "csv":
            new_parser.json_to_csv(node, json_file_path, csv_file_path)
