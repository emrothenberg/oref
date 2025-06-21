from typing import List, Literal, Sequence
import logging


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
        from .loader import get_location
        self.id = id
        self.category = category
        self.title = title
        self.description = description
        self.unfiltered_locations = []
        self.locations = []

        for i in data:
            loc = get_location(i)
            if isinstance(loc, Location):
                self.unfiltered_locations.append(loc)

        if relevant:
            self.filter_locations(relevant)

    def filter_locations(self, relevant: Sequence[int | str] | Literal["all"]) -> List[Location]:
        from .loader import get_location, validate_location
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

        if not self.locations == "all":
            for i in list(set(relevant)):
                try:
                    validate_location(i)
                except AssertionError:
                    logger.warning(f"Warning: [!] Location {i} is invalid.")

                loc = get_location(i)
                if loc and loc in self.unfiltered_locations:
                    filtered.append(loc)

        self.locations = filtered
        return filtered

    def __str__(self):
        return f"[{self.id}] {self.title} ({len(self.locations)} locations)"

    def __repr__(self):
        return f"Alert(id={self.id!r}, category={self.category}, title={self.title!r}, description={self.description!r}, locations={self.locations!r})"
