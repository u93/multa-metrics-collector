
DATE_FORMAT = '%m-%d-%Y'

analysis_list = {"RAM" : [
            "average",
            "maximun",
            "minimun"
        ],
        "TEMP" : [
            "average",
            "maximun",
            "minimun"
        ],
        "DISK" : [
            "average",
            "maximun",
            "minimun"
        ],
        "STATUS" : [
            "average",
            "maximun",
            "minimun"
        ],
        "BOOT" : [
            "average",
            "maximun",
            "minimun"
        ],
        "CPU" : [
            "average",
            "maximun",
            "minimun"
        ]}

agent_list = ["multa-agent-compose-i386-243"]

metric_list = {"RAM": [
            "ram_memory_total",
            "ram_memory_available",
            "ram_memory_percent",
            "ram_memory_used",
            "ram_memory_free",
            "ram_memory_shared",
            "ram_memory_buffers",
            "ram_memory_cached",
            "ram_swap_total",
            "ram_swap_used",
            "ram_swap_free",
            "ram_swap_percent",
            "ram_insights_current",
            "ram_insights_total",
            "ram_insights_percent",
            "ram_insights_status",
        ],
        "TEMP": [
            "temperature_current",
            "temperature_total",
            "temperature_insights_percent",
            "temperature_insights_status",
        ],
        "DISK": [
            "disk_dynamic_current",
            "disk_dynamic_total",
            "disk_dynamic_percent",
            "disk_dynamic_insights_status",
            "disk_dynamic_io_read_count",
            "disk_dynamic_io_write_count",
            "disk_dynamic_io_read_bytes",
            "disk_dynamic_io_write_bytes",
            "disk_dynamic_io_read_time",
            "disk_dynamic_io_write_time",
        ],
        "STATUS" : [
        "status"
        ],
        "CPU": [
        "cpu_dynamic_insights_percent", 
        "cpu_dynamic_insights_status"
        ],
        "BOOT" : [
            "boot_time_insights_seconds_since_boot",
            "boot_time_insights_days_since_boot",
            "boot_time_insights_status",
        ]}