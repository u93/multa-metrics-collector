from ram_validation import RamSchema
from boot_validation import BootSchema
from cpu_validation import CPUSchema
from temp_validation import TempSchema
from status_validation import StatusSchema
from disk_validation import DiskSchema

query = {
    "analysis": "average",
    "parameters": {
        "metric_value": ["disk_dynamic_current"],
        "metric_range": "",
        "start_time": "01:20:00",
        "end_time": "07:30:00",
        "start_date": None,
        "end_date": None,
        "start_timestamp": "1591585506",
        "end_timestamp": "1591643030",
        "agents": ["multa-agent-compose-i386-243"],
        "metadata": {}
    }
}

try:
    schema = DiskSchema()
    results = schema.validate(query)
    print(results)
except ValidationError as err:
    print(err)
