import json
import os
import time

from handlers.data_analysis.lambda_functions import LambdaHandler
from handlers.utils import base_response
from settings.aws import ANALYTICS_LAMBDA_ROUTING_MAPPING
from settings.logs import Logger

logs_handler = Logger()
logger = logs_handler.get_logger()


def lambda_handler(event, context):
    activation_time = round(time.time())
    logger.info(activation_time)
    logger.info(event)

    return base_response(status_code=200)


if __name__ == "__main__":
    event = {
        "previous": {
            "state": {
                "reported": {
                    "ram_info": {
                        "raw": {
                            "memory": {
                                "total": 8269570048,
                                "available": 7674933248,
                                "percent": 7.2,
                                "used": 303083520,
                                "free": 6174826496,
                                "shared": 1515520,
                                "buffers": 294756352,
                                "cached": 1496903680,
                            },
                            "swap": {"total": 4294963200, "used": 0, "free": 4294963200, "percent": 0.0},
                        },
                        "insights": {"current": 594636800, "total": 1496903680, "percent": 1496903680, "status": False},
                    },
                    "cpu_dynamic_info": {
                        "raw": {
                            "percent_per_cpu": [2, 0, 0, 0],
                            "freq_per_cpu": [480, 480, 488, 480],
                            "avg_load_times": [1, 1, 0],
                            "avg_load_percent_times": [20, 16, 9],
                        },
                        "insights": {"percent": 1, "high": False},
                    },
                    "disk_dynamic_info": {
                        "current": 10013065216,
                        "total": 982899539968,
                        "percent": 1,
                        "high": False,
                        "general_io": {
                            "read_count": 82306,
                            "write_count": 4594,
                            "read_bytes": 725876736,
                            "write_bytes": 1272476160,
                            "read_time": 82306,
                            "write_time": 1626256,
                        },
                    },
                    "temp_info": {
                        "raw": {
                            "current": 106,
                            "total": 194,
                            "per_core": {
                                "acpitz": [{"label": "", "current": 80, "high": 203, "critical": 203}],
                                "coretemp": [
                                    {"label": "Core 0", "current": 106, "high": 194, "critical": 194},
                                    {"label": "Core 1", "current": 106, "high": 194, "critical": 194},
                                    {"label": "Core 2", "current": 106, "high": 194, "critical": 194},
                                    {"label": "Core 3", "current": 106, "high": 194, "critical": 194},
                                    {"label": "Core 0", "current": 106, "high": 194, "critical": 194},
                                    {"label": "Core 1", "current": 106, "high": 194, "critical": 194},
                                    {"label": "Core 2", "current": 106, "high": 194, "critical": 194},
                                    {"label": "Core 3", "current": 106, "high": 194, "critical": 194},
                                ],
                            },
                        },
                        "insights": {"percent": 55, "high": False},
                    },
                    "boot_time_info": {
                        "raw": {"last_boot_timestamp": 1591369599.0, "current_date": "2020-06-05 15:19:52.758383"},
                        "insights": {
                            "last_boot": "2020-06-05 15:06:39",
                            "days_since_boot": 0,
                            "seconds_since_boot": 794,
                            "high": False,
                        },
                    },
                    "battery_info": {},
                    "fans_info": {},
                    "bw_info": {"current": 0},
                    "hardware": {"machine": "x86_64", "processor": "", "name": 0},
                    "platform": {
                        "system": "Linux",
                        "node": "test_server_greengrass",
                        "release": "4.15.0-101-generic",
                        "version": "#102-Ubuntu SMP Mon May 11 10:07:26 UTC 2020",
                        "machine": "",
                        "processor": "",
                        "architecture": "64bit",
                        "libc_version": "glibc 2.2.5",
                    },
                    "cpu_static_info": {
                        "physical_cpu_count": 4,
                        "logical_cpu_count": 4,
                        "cpu_affinity": 4,
                        "min_cpu_freq": 480,
                        "max_cpu_freq": 2240,
                        "per_cpu_freq": [
                            {"min": 480, "max": 2240},
                            {"min": 480, "max": 2240},
                            {"min": 480, "max": 2240},
                            {"min": 480, "max": 2240},
                        ],
                    },
                    "disk_static_nfo": {
                        "partitions_info": {
                            "/device-data:/device": {
                                "device": "/dev/sda2",
                                "fstype": "ext4",
                                "opts": "rw,relatime,data=ordered",
                            },
                            "/device": {"device": "/dev/sda2", "fstype": "ext4", "opts": "rw,relatime,data=ordered"},
                            "/proc:/prochost:ro": {
                                "device": "/dev/sda2",
                                "fstype": "ext4",
                                "opts": "rw,relatime,data=ordered",
                            },
                            "/sys:/sys:ro": {
                                "device": "/dev/sda2",
                                "fstype": "ext4",
                                "opts": "rw,relatime,data=ordered",
                            },
                            "/:/rootfs:ro": {
                                "device": "/dev/sda2",
                                "fstype": "ext4",
                                "opts": "rw,relatime,data=ordered",
                            },
                            "/etc/resolv.conf": {
                                "device": "/dev/sda2",
                                "fstype": "ext4",
                                "opts": "rw,relatime,data=ordered",
                            },
                            "/etc/hostname": {
                                "device": "/dev/sda2",
                                "fstype": "ext4",
                                "opts": "rw,relatime,data=ordered",
                            },
                            "/etc/hosts": {"device": "/dev/sda2", "fstype": "ext4", "opts": "rw,relatime,data=ordered"},
                            "/var/run:/var/run:rw": {
                                "device": "/dev/sda2",
                                "fstype": "ext4",
                                "opts": "rw,relatime,data=ordered",
                            },
                            "/run/docker.sock:/var/run/docker.sock": {
                                "device": "/dev/sda2",
                                "fstype": "ext4",
                                "opts": "rw,relatime,data=ordered",
                            },
                            "/var/lib/docker/:/var/lib/docker:ro": {
                                "device": "/dev/sda2",
                                "fstype": "ext4",
                                "opts": "rw,relatime,data=ordered",
                            },
                        }
                    },
                }
            }
        },
        "current": {
            "state": {
                "reported": {
                    "ram_info": {
                        "raw": {
                            "memory": {
                                "total": 8269570048,
                                "available": 7674933248,
                                "percent": 7.2,
                                "used": 303083520,
                                "free": 6174826496,
                                "shared": 1515520,
                                "buffers": 294756352,
                                "cached": 1496903680,
                            },
                            "swap": {"total": 4294963200, "used": 0, "free": 4294963200, "percent": 0.0},
                        },
                        "insights": {"current": 594636800, "total": 1496903680, "percent": 1496903680, "status": False},
                    },
                    "cpu_dynamic_info": {
                        "raw": {
                            "percent_per_cpu": [2, 0, 0, 0],
                            "freq_per_cpu": [480, 480, 488, 480],
                            "avg_load_times": [1, 1, 0],
                            "avg_load_percent_times": [20, 16, 9],
                        },
                        "insights": {"percent": 1, "high": False},
                    },
                    "disk_dynamic_info": {
                        "current": 10013065216,
                        "total": 982899539968,
                        "percent": 1,
                        "high": False,
                        "general_io": {
                            "read_count": 82306,
                            "write_count": 4594,
                            "read_bytes": 725876736,
                            "write_bytes": 1272476160,
                            "read_time": 82306,
                            "write_time": 1626256,
                        },
                    },
                    "temp_info": {
                        "raw": {
                            "current": 106,
                            "total": 194,
                            "per_core": {
                                "acpitz": [{"label": "", "current": 80, "high": 203, "critical": 203}],
                                "coretemp": [
                                    {"label": "Core 0", "current": 106, "high": 194, "critical": 194},
                                    {"label": "Core 1", "current": 106, "high": 194, "critical": 194},
                                    {"label": "Core 2", "current": 106, "high": 194, "critical": 194},
                                    {"label": "Core 3", "current": 106, "high": 194, "critical": 194},
                                    {"label": "Core 0", "current": 106, "high": 194, "critical": 194},
                                    {"label": "Core 1", "current": 106, "high": 194, "critical": 194},
                                    {"label": "Core 2", "current": 106, "high": 194, "critical": 194},
                                    {"label": "Core 3", "current": 106, "high": 194, "critical": 194},
                                ],
                            },
                        },
                        "insights": {"percent": 55, "high": False},
                    },
                    "boot_time_info": {
                        "raw": {"last_boot_timestamp": 1591369599.0, "current_date": "2020-06-05 15:19:52.758383"},
                        "insights": {
                            "last_boot": "2020-06-05 15:06:39",
                            "days_since_boot": 0,
                            "seconds_since_boot": 794,
                            "high": False,
                        },
                    },
                    "battery_info": {},
                    "fans_info": {},
                    "bw_info": {"current": 0},
                    "hardware": {"machine": "x86_64", "processor": "", "name": 0},
                    "platform": {
                        "system": "Linux",
                        "node": "test_server_greengrass",
                        "release": "4.15.0-101-generic",
                        "version": "#102-Ubuntu SMP Mon May 11 10:07:26 UTC 2020",
                        "machine": "",
                        "processor": "",
                        "architecture": "64bit",
                        "libc_version": "glibc 2.2.5",
                    },
                    "cpu_static_info": {
                        "physical_cpu_count": 4,
                        "logical_cpu_count": 4,
                        "cpu_affinity": 4,
                        "min_cpu_freq": 480,
                        "max_cpu_freq": 2240,
                        "per_cpu_freq": [
                            {"min": 480, "max": 2240},
                            {"min": 480, "max": 2240},
                            {"min": 480, "max": 2240},
                            {"min": 480, "max": 2240},
                        ],
                    },
                    "disk_static_nfo": {
                        "partitions_info": {
                            "/device-data:/device": {
                                "device": "/dev/sda2",
                                "fstype": "ext4",
                                "opts": "rw,relatime,data=ordered",
                            },
                            "/device": {"device": "/dev/sda2", "fstype": "ext4", "opts": "rw,relatime,data=ordered"},
                            "/proc:/prochost:ro": {
                                "device": "/dev/sda2",
                                "fstype": "ext4",
                                "opts": "rw,relatime,data=ordered",
                            },
                            "/sys:/sys:ro": {
                                "device": "/dev/sda2",
                                "fstype": "ext4",
                                "opts": "rw,relatime,data=ordered",
                            },
                            "/:/rootfs:ro": {
                                "device": "/dev/sda2",
                                "fstype": "ext4",
                                "opts": "rw,relatime,data=ordered",
                            },
                            "/etc/resolv.conf": {
                                "device": "/dev/sda2",
                                "fstype": "ext4",
                                "opts": "rw,relatime,data=ordered",
                            },
                            "/etc/hostname": {
                                "device": "/dev/sda2",
                                "fstype": "ext4",
                                "opts": "rw,relatime,data=ordered",
                            },
                            "/etc/hosts": {"device": "/dev/sda2", "fstype": "ext4", "opts": "rw,relatime,data=ordered"},
                            "/var/run:/var/run:rw": {
                                "device": "/dev/sda2",
                                "fstype": "ext4",
                                "opts": "rw,relatime,data=ordered",
                            },
                            "/run/docker.sock:/var/run/docker.sock": {
                                "device": "/dev/sda2",
                                "fstype": "ext4",
                                "opts": "rw,relatime,data=ordered",
                            },
                            "/var/lib/docker/:/var/lib/docker:ro": {
                                "device": "/dev/sda2",
                                "fstype": "ext4",
                                "opts": "rw,relatime,data=ordered",
                            },
                        }
                    },
                }
            }
        },
    }
    lambda_handler(event=event, context={})
