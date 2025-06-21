# Oref

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Oref** is an unofficial Python wrapper for Israel’s Home Front Command alert system. It mimics the official website’s functionality, enabling Python-based access and alert monitoring.

## Features

- Live and one-time alert checks
- Area-specific filtering
- Multilingual support (`ar`, `he`, `ru`)
- Location and guideline retrieval

## Installation

```bash
pip install oref
````

## Requirements

* Python 3.11+
* `requests` 2.31+

## Usage

```python
import oref
from oref.types import Alert

# Initialise (default: English only)
oref.init()

# Add more languages (supported: "ar", "he", "ru")
oref.init(extra_languages=["ar", "he"])

# One-time alert check (default: all areas)
oref.check_alert()

# Check specific areas (by name or ID)
oref.check_alert(["Tel Aviv - South and Jaffa", 439, "Givatayim"])

# Live alert monitoring
def callback(alert: Alert):
    print(alert)

oref.listen(callback)  # Optional: areas=[...]

# Alternatively:
oref.alerts.listen(callback)

# Retrieve available locations
oref.get_locations()  # -> List[oref.types.Location]

# Retrieve guidelines
oref.get_guidelines()  # -> List[oref.types.Guideline]
```