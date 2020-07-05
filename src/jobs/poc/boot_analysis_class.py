import json
import pandas as pd
import numpy as np
import datetime as dt

from query_class import Query_Analize


class Boot_Analize(Query_Analize):
    def __init__(self, query_file="", data_file=""):
        Query_Analize.__init__(self, query_file, data_file)
        self.metrics = [
            "boot_time_insights_seconds_since_boot",
            "boot_time_insights_days_since_boot",
            "boot_time_insights_status",
        ]

    def make_analysis(self):
        for ag_data in self.agents_data:
            ag_temp = []
            for metric_v in self.metric_value:
                if self.analysis == "average":
                    ag_temp.append((metric_v, np.array(ag_data[metric_v].values).mean()))
                elif self.analysis == "maximun":
                    ag_temp.append((metric_v, np.array(ag_data[metric_v].values).max()))
                elif self.analysis == "minimun":
                    ag_temp.append((metric_v, np.array(ag_data[metric_v].values).min()))
                else:
                    print("Metric no valid")
            self.agents_result.append(ag_temp)
        # print("make analysis", self.agents_result)

    def get_query_results(self):
        self.format_data()
        self.select_period()
        self.select_time()
        self.get_agent_data()
        self.make_analysis()

        output = {}
        output["analysis"] = self.analysis
        output["agents"] = []
        for ag in range(len(self.agents)):
            ag_temp = {}
            # ag_temp = {key: None for key in self.metric_value}
            ag_temp["name"] = self.agents[ag]
            for res in self.agents_result:
                for tup in res:
                    # print("tup0", tup[0])
                    # print("tup1", tup[1])
                    ag_temp[str(tup[0])] = tup[1]
            output["agents"].append(ag_temp)
        # print(output)
        return output
