import json
import pandas as pd
import numpy as np
import datetime as dt
from abc import ABCMeta, abstractmethod

# timestamp = 1545730073
# dt_object = datetime.fromtimestamp(timestamp)

# print("dt_object =", dt_object)
# print("type(dt_object) =", type(dt_object))


class Query_Analize:
    __metaclass__ = ABCMeta

    def __init__(self, query_file="", data_file=""):

        with open(query_file) as file:
            query = json.load(file)
        self.analysis = query["analysis"]
        self.metric_value = query["parameters"]["metric_value"]
        self.metric_range = query["parameters"]["metric_range"]
        self.start_time = query["parameters"]["start_time"]
        self.end_time = query["parameters"]["end_time"]
        self.start_date = query["parameters"]["start_date"]
        self.end_date = query["parameters"]["end_date"]
        self.start_timestamp = query["parameters"]["start_timestamp"]
        self.end_timestamp = query["parameters"]["end_timestamp"]
        self.agents = query["parameters"]["agents"]
        self.data = pd.read_csv(data_file)
        self.agents_data = []
        self.agents_result = []
        self.metrics = []

    def format_data(self):
        print(list(self.data.columns))
        self.data = self.data[self.metrics + ["serial_number", "timestamp"]]
        # print(self.data[self.metric].value_counts())
        self.data["date_time"] = pd.to_datetime(self.data["timestamp"], unit="s")
        # print(self.data)

    def select_period(self):
        if self.start_timestamp != "" and self.end_timestamp != "":
            self.data.set_index("timestamp", inplace=True)
            self.data = self.data.sort_values(["timestamp"])
            self.data = self.data.loc[int(self.start_timestamp) : int(self.end_timestamp)]
            self.data.set_index("date_time", inplace=True)
            self.data = self.data.sort_values(["date_time"])
            # print(self.data)
        else:
            self.data.set_index("date_time", inplace=True)
            self.data = self.data.sort_values(["date_time"])
            self.data = self.data.loc[self.start_time : self.end_time]
        # print(self.data)

    def select_time(self):
        start = dt.datetime.strptime(self.start_time, "%H:%M:%S").time()
        end = dt.datetime.strptime(self.end_time, "%H:%M:%S").time()
        self.data = self.data.between_time(start, end)
        # print(self.data)

    def get_agent_data(self):
        for i in self.agents:
            self.agents_data.append(self.data[self.data["serial_number"] == i])
            print(self.agents_data)
            # print(i)
            # self.agents_data.append((list(temp.index) , np.array(temp[self.metrics[0]])))
        # print(self.agents_data[0][1])

    @abstractmethod
    def make_analysis(self):
        pass

    @abstractmethod
    def get_query_results(self):
        pass


# timestamp = 1583713243
# print(timestamp)
# print(str(datetime.fromtimestamp(timestamp)))
# print(len(query['parameters']['agents']))


# print(data.head(50))


# print(query['analysis'])
# if query['parameters']['end_date'] == '':
# 	print('empty')
# print(query['parameters']['start_timestamp'])


# output = dict()
# output ['analysis'] = query['analysis']
# output ['agents'] = query['parameters']['agents']
# output [query['analysis']] = 6466
# print(output)
