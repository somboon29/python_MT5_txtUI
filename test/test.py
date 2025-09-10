import os
import time
import math
import json
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional


def load_config(config_path: str = "test/config.json") -> Dict[str, Any]:
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Config file {config_path} not found")
    with open(config_path, "r") as f:
        return json.load(f)
df= load_config()
print(df)