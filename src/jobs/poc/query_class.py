import json
import pandas as pd
import numpy as np
import datetime as dt

# timestamp = 1545730073
# dt_object = datetime.fromtimestamp(timestamp)

# print("dt_object =", dt_object)
# print("type(dt_object) =", type(dt_object))


class query_analize():
	def __init__(self, query_file= '', data_file= ''):

		with open(query_file) as file:
			query = json.load(file)
		self.analysis = query['analysis']
		self.metric_value = query['parameters']['metric_value']
		self.metric_range = query['parameters']['metric_range']
		self.start_time = query['parameters']['start_time']
		self.end_time = query['parameters']['end_time']
		self.start_date = query['parameters']['start_date']
		self.end_date = query['parameters']['end_date']
		self.start_timestamp = query['parameters']['start_timestamp']
		self.end_timestamp = query['parameters']['end_timestamp']
		self.agents = query['parameters']['agents']
		self.data = pd.read_csv(data_file)
		self.agents_data = []
		self.agents_result = []
		self.metric = 'status'

	def format_data (self):
		self.data = self.data.drop(['__dt'], axis=1)
		#print(self.data[self.metric].value_counts())
		self.data['date_time'] = pd.to_datetime(self.data['timestamp'], unit="s")
		#print(self.data)

	def select_period(self):
		if(self.start_timestamp != "" and self.end_timestamp != ""):
			self.data.set_index('timestamp', inplace=True)
			self.data = self.data.sort_values(['timestamp'])
			self.data = self.data.loc[int(self.start_timestamp):int(self.end_timestamp)]
			self.data.set_index('date_time', inplace=True)
			self.data = self.data.sort_values(['date_time'])
			#print(self.data)
		else:
			self.data.set_index('date_time', inplace=True)
			self.data = self.data.sort_values(['date_time'])
			self.data = self.data.loc[self.start_time : self.end_time]
		#print(self.data)

	def select_time(self):
		start = dt.time(1,50,0)
		end = dt.time(6,0,0)
		self.data = self.data.between_time(start, end)
		print(self.data)
		
		#pandas.time_range("11:00", "21:30")


	def get_agent_data(self):
		for i in self.agents:
			temp = self.data[self.data['serial_number'] == i]
			self.agents_data.append((list(temp.index) , np.array(temp[self.metric])))
		print(self.agents_data[0][1])
	
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
		pass


query = query_analize('query.json','ElU.csv')
query.format_data()
query.select_period()
query.select_time()
query.get_agent_data()
query.make_analysis()

# timestamp = 1583713243
# print(timestamp)
# print(str(datetime.fromtimestamp(timestamp)))
#print(len(query['parameters']['agents']))



#print(data.head(50))


# print(query['analysis'])
# if query['parameters']['end_date'] == '':
# 	print('empty')
# print(query['parameters']['start_timestamp'])




# output = dict()
# output ['analysis'] = query['analysis']
# output ['agents'] = query['parameters']['agents']
# output [query['analysis']] = 6466
# print(output)