import json
import pandas as pd
import numpy as np
import datetime as dt
import streamlit as st

from status_analysis_class import Status_Analize
from ram_analysis_class import Ram_Analize
from disk_analysis_class import Disk_Analize
from cpu_analysis_class import CPU_Analize
from temp_analysis_class import Temp_Analize

query = Ram_Analize("query.json", "NewFormat.csv")
results = query.get_query_results()
print(results)
# query.format_data()
# query.select_period()
# query.select_time()
# query.get_agent_data()

# data = query.agents_data[0]
# print(data['ram_memory_used'])
print(query.get_query_results())


# query = Status_Analize('query.json','ElU.csv')
# output = query.get_query_results()
# print(output)
