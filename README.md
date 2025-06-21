# Oref

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Oref** – Python interface to Israel’s Home Front Command (Pikud HaOref) emergrncy alert network.

---

## Installation

```bash
pip install oref
```

*Python 3.11 + required.*

---

## Quick‑start

```python
import oref
from oref.types import Alert

# Load baseline (English) metadata
oref.init()

# Optional – preload extra languages
oref.init(extra_languages=["he", "ar", "ru"])

# One‑off check (all areas)
alert = oref.check_alert()
if alert:
    print(alert)

# Continuous listener (filter to specific areas if desired)

def on_alert(a: Alert):
    print("\n>>> INCOMING:", a)

oref.listen(on_alert, areas=["Jerusalem", 158])
```

---

## API Synopsis

### Initialise

| Function   | Signature                                                     | Purpose                                                                                       |
| ---------- | ------------------------------------------------------------- | --------------------------------------------------------------------------------------------- |
| **`init`** | `init(extra_languages: List[Literal["ar", "he", "ru"]] = [])` | Downloads location, guideline & translation datasets. Must be called before any other helper. |

### Alerts
Alert functions can be invoked from both `oref` and `oref.alerts`.

| Function          | Signature                                     | Notes                                                  |                                                                                                |                                                 |
| ----------------- | --------------------------------------------- | ------------------------------------------------------ | ---------------------------------------------------------------------------------------------- | ----------------------------------------------- |
| **`check_alert`** | \`check\_alert(areas: List\[str \| int] \| Literal\["all"] = "all") -> Alert \ bool\`                                                                                         | Returns latest alert object or `False` if none. |
| **`listen`**      | \`listen(callback: Callable, areas: List\[str \| int] \| Literal\["all"] = "all", args=(), kwargs={})\` | Polls every second; invokes `callback` once per unique alert (15‑minute deduplication window). |                                                 |

### Data Helpers
Data helpers can be invoked from both `oref` and `oref.loader`

| Function                 | Returns                  | Description                                                             |                                            |
| ------------------------ | ------------------------ | ----------------------------------------------------------------------- | ------------------------------------------ |
| **`locations`**          | `List[Location]`         | All known locations with multilingual labels & shelter times.           |                                            |
| **`location`**           | \`Location \| bool\`                                                                  | Single lookup by ID or any language label. |
| **`guidelines`**         | `List[Guideline]`        | Civil‑defence instructions per alert zone.                              |                                            |
| **`alert_translations`** | `List[AlertTranslation]` | Full mapping of alert categories/titles/desc in four languages.         |                                            |
| **`translate`**          | `(title, desc)`          | Convenience wrapper translating an `Alert` into the requested language. |                                            |

### Data Structures (`oref.types`)

* **`Alert`** – `id`, `category`, `title`, `description`, `locations`, `unfiltered_locations`; `filter_locations(relevant)`
* **`Location`** – `id`, `area_id`, `name` (*Placename*), `region` (*Placename*), `shelter_time`
* **`Guideline`** – `code`, `area_id`, `zone_name`, `label` (*Placename*), `time_notes`, `mode`, `color_code`
* **`Placename`** – multilingual string container (`en / he / ar / ru`)
* **`AlertTranslation`** – four‑language mapping plus category metadata

---

## Example – Translate & Filter

```python
from oref import check_alert, translate

alert = check_alert()
if alert:
    # Limit to Be’er Sheva & area‑id 165
    alert.filter_locations(["Be'er Sheva", 165])
    # Convert title/description to Russian
    title_ru, desc_ru = translate(alert, "ru")
    print(title_ru, "::", desc_ru)
```

---

## Configuration

`oref.config` exposes endpoint constants (`ALERTS_URL`, `LOCATIONS_URL`, `GUIDELINES_URL`, `ALERT_TRANSLATIONS_URL`). Override them **before** calling `init()` to point at mirrors, proxies, or test fixtures.

---

## Logging

The package emits informative messages via the standard `logging` module. Example:

```python
import logging, oref
logging.basicConfig(level=logging.INFO)
oref.init()
```

---

## Caveats

* Unofficial – not endorsed by Pikud HaOref.
* Upstream JSON schemas may change without notice.
* Network polling every second like the official website; adjust in fork if lower bandwidth is essential.

---

## Licence

MIT © 2025
