from typing import List, Literal, Sequence
import logging

from typing import Optional, List


class AlertTranslation:
    he: str
    en: str
    ru: str
    ar: str
    all_descs: List[str]
    cat_id: int
    matrix_cat_id: int
    he_title: Optional[str]
    en_title: Optional[str]
    ru_title: Optional[str]
    ar_title: Optional[str]
    all_titles: List[Optional[str]]
    update_type: int

    def __init__(
        self,
        heb: str,
        eng: str,
        rus: str,
        arb: str,
        cat_id: int,
        matrix_cat_id: int,
        heb_title: Optional[str],
        eng_title: Optional[str],
        rus_title: Optional[str],
        arb_title: Optional[str],
        update_type: int
    ):
        self.he = heb
        self.en = eng
        self.ru = rus
        self.ar = arb
        self.all_descs = [heb, eng, rus, arb]
        self.cat_id = cat_id
        self.matrix_cat_id = matrix_cat_id
        self.he_title = heb_title
        self.en_title = eng_title
        self.ru_title = rus_title
        self.ar_title = arb_title
        self.all_titles = [heb_title, eng_title, rus_title, arb_title]
        self.update_type = update_type
        
    def __getitem__(self, key):
        return getattr(self, f"{key}")

    def __repr__(self):
        return f"<Alert eng_title='{self.en_title}' cat_id={self.cat_id}>"


def parse_alerts(data: List[dict]) -> List[AlertTranslation]:
    return [
        AlertTranslation(
            heb=item["heb"],
            eng=item["eng"],
            rus=item["rus"],
            arb=item["arb"],
            cat_id=item["catId"],
            matrix_cat_id=item["matrixCatId"],
            heb_title=item.get("hebTitle"),
            eng_title=item.get("engTitle"),
            rus_title=item.get("rusTitle"),
            arb_title=item.get("arbTitle"),
            update_type=0 if item["updateType"] == "-" else int(
                item["updateType"])
        )
        for item in data
    ]


class Placename:
    en: str
    he: str | None
    ar: str | None
    ru: str | None

    def __init__(self, en: str, he: str | None = None, ar: str | None = None, ru: str | None = None):
        self.en = en
        self.he = he
        self.ar = ar
        self.ru = ru

    def __getitem__(self, key):
        return getattr(self, key)

    def __str__(self):
        return f'[{" | ".join(filter(None, (self.en, self.he, self.ar, self.ru)))}]'

    def __repr__(self):
        return (f"Placename(en={self.en!r}, he={self.he!r}, "
                f"ar={self.ar!r}, ru={self.ru!r})")


class Guideline:
    code: int
    area_id: int
    zone_name: str
    label: Placename
    time_notes: int
    mode: str
    color_code: str

    def __init__(self, code: int | str, area_id: int, zone_name: str, label: Placename | dict, time_notes: int | str, mode: str, color_code: str, **kwargs):
        self.code = int(code)
        self.area_id = area_id
        self.zone_name = zone_name
        self.label = Placename(**label) if isinstance(label, dict) else label
        self.time_notes = int(
            "".join([d for d in str(time_notes) if d.isdigit()] or ["0"]))
        self.mode = mode
        self.color_code = color_code


class Location:
    id: int
    area_id: int
    name: Placename
    region: Placename
    shelter_time: int

    def __init__(self, id: int | str, area_id: int | str, name: Placename | dict, region: Placename | dict, shelter_time: int, **args):
        self.id = int(id)
        self.area_id = int(area_id)
        self.name = Placename(**name) if isinstance(name, dict) else name
        self.region = Placename(
            **region) if isinstance(region, dict) else region
        self.shelter_time = shelter_time

    def __str__(self):
        return f"{str(self.name)} ({str(self.region)}) - Shelter time: {self.shelter_time}s"

    def __repr__(self):
        return (f"Location(id={self.id}, area_id={self.area_id}, "
                f"name={self.name}, region={self.region}, shelter_time={self.shelter_time})")


class Alert():
    id: str
    category: int
    title: str
    description: str
    locations: List[Location]
    unfiltered_locations: List[Location]

    def __init__(self, id: str, category: int, title: str, description: str, data: List[str], relevant: Sequence[str | int] | None = None, **kwargs):
        from .loader import location
        self.id = id
        self.category = category
        self.title = title
        self.description = description
        self.unfiltered_locations = []
        self.locations = []

        for i in data:
            loc = location(i)
            if isinstance(loc, Location):
                self.unfiltered_locations.append(loc)

        if relevant:
            self.filter_locations(relevant)

    def filter_locations(self, relevant: Sequence[int | str] | Literal["all"]) -> List[Location]:
        from .loader import location, validate_location
        """
        Filters and returns a list of valid locations from the given identifiers.

        Parameters:
            relevant (Sequence[int | str]): A list of location identifiers (integers or strings) to filter.

        Returns:
            List[Location]: A list of validated and existing locations present in self.locations.

        Logs:
            Emits a warning for invalid location identifiers.

        Side Effects:
            Updates self.filtered_locations with the filtered results.
        """

        logger = logging.getLogger(__name__)

        filtered = self.locations if relevant == "all" else []

        if not relevant == "all":
            for i in list(set(relevant)):
                try:
                    validate_location(i)
                except AssertionError:
                    logger.warning(f"Warning: [!] Location {i} is invalid.")

                loc = location(i)
                if loc and loc in self.unfiltered_locations:
                    filtered.append(loc)

        self.locations = filtered
        return filtered

    def __str__(self):
        return f"[{self.id}] {self.title} ({len(self.locations)} locations)"

    def __repr__(self):
        return f"Alert(id={self.id!r}, category={self.category}, title={self.title!r}, description={self.description!r}, locations={self.locations!r})"
