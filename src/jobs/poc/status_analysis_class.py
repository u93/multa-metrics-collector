import json
import pandas as pd
import numpy as np
import datetime as dt

from query_class import Query_Analize


class Status_Analize(Query_Analize):
    def __init__(self, query_file="", data_file=""):
        Query_Analize.__init__(self, query_file, data_file)
        self.metrics = ["status"]

    def format_data(self):
        self.data = self.data.drop(["__dt"], axis=1)
        # print(self.data[self.metric].value_counts())
        self.data["date_time"] = pd.to_datetime(self.data["timestamp"], unit="s")
        # print(self.data)

    def make_analysis(self):
        if self.analysis == "average":
            for ang_data in self.agents_data:
                self.agents_result.append(ang_data[1].mean())
        elif self.analysis == "maximun":
            for ang_data in self.agents_data:
                self.agents_result.append(ang_data[1].max())
        elif self.analysis == "minimun":
            for ang_data in self.agents_data:
                self.agents_result.append(ang_data[1].min())
        print(self.agents_result)

    def get_query_results(self):
        self.format_data()
        self.select_period()
        self.select_time()
        self.get_agent_data()
        self.make_analysis()

        output = dict()
        output["metric"] = self.metrics[0]
        output["analysis"] = self.analysis
        output["agents"] = self.agents
        output["agents"] = self.agents
        output["agents_result"] = self.agents_result
        return output
