import json
import pandas as pd
import numpy as np
import datetime as dt

from query_class import Query_Analize

class Ram_Analize (Query_Analize):
	def __init__(self, query_file= '', data_file= ''):
		Query_Analize.__init__(self, query_file, data_file)
		self.metrics = ['ram_memory_total', 'ram_memory_available', 'ram_memory_percent', 'ram_memory_used', 'ram_memory_free', 'ram_memory_shared', 'ram_memory_buffers', 'ram_memory_cached', 'ram_swap_total', 'ram_swap_used', 'ram_swap_free', 'ram_swap_percent', 'ram_insights_current', 'ram_insights_total', 'ram_insights_percent', 'ram_insights_status']


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
		#print("make analysis", self.agents_result)

	def get_query_results(self):
		self.format_data()
		self.select_period()
		self.select_time()
		self.get_agent_data()
		self.make_analysis()

		output = {}
		output ['analysis'] = self.analysis
		output ['agents'] = []
		for ag in range(len(self.agents)):
			ag_temp = {}
			#ag_temp = {key: None for key in self.metric_value} 
			ag_temp ['name'] = self.agents[ag]
			for res in self.agents_result:
				for tup in res:
					ag_temp[str(tup[0])] = tup[1]
			output['agents'].append(ag_temp)
		#print(output)
		return output
