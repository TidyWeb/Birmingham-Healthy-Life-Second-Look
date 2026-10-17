#!/usr/bin/env python3
"""Build the Concept B v3 static data payload and self-contained page."""

from __future__ import annotations

import sys
sys.dont_write_bytecode = True

import base64
import csv
import json
import math
import re
from pathlib import Path
from typing import Any

from shapely.geometry import shape
from shapely import coverage_invalid_edges, coverage_is_valid


HERE = Path(__file__).resolve().parent
SITE_ROOT = HERE.parents[1]
PROJECT_ROOT = HERE.parents[2] / "Code-Institute-DA-with-AI-Unit-3-Assessment"
DATA_FILE = HERE / "web-data.json"
INDEX_FILE = HERE / "index.html"
TEMPLATE_FILE = HERE / "template.html"
QUESTION_URL = "https://github.com/TidyWeb/Birmingham-Healthy-Life-Second-Look/issues/new?template=question-this-work.yml"

WIDE_CSV = PROJECT_ROOT / "data/cleaned/Wide/msoa_wide_660.csv"
WIDE_DICTIONARY = PROJECT_ROOT / "data/cleaned/Wide/data_dictionary.csv"
NAMES_FILE = PROJECT_ROOT / "data/reference/Area Names/locality-names.json"
GEOMETRY_FILE = PROJECT_ROOT / "data/raw/2026-10-01/ons_msoa21_boundaries_exploratory_west_midlands.geojson"
PAIRS_FILE = PROJECT_ROOT / "data/cleaned/Neighbours/neighbour_pairs.csv"
BIG_GAPS_FILE = PROJECT_ROOT / "data/cleaned/Neighbours/big_gap_pairs.csv"
PAIR_DICTIONARY = PROJECT_ROOT / "data/cleaned/Neighbours/neighbour_data_dictionary.csv"
RANK_STABILITY_FILE = PROJECT_ROOT / "data/cleaned/Uncertainty/rank_stability.csv"
SMOKING_CONTEXT_FILE = HERE / "smoking-context.json"
AUTHORITY_LOOKUP = PROJECT_ROOT / "data/prepared/Geography/ons_lsoa21_to_msoa21_lad22_exploratory_west_midlands.csv"

# These are the measures exposed by the Concept B v3 metric switch. Other
# source fields remain in each area's values for traceability, but are not
# added as map layers.
DISPLAY_MEASURE_FIELDS = (
    "hle_average",
    "hle_male",
    "hle_female",
    "annual_equivalised_income_after_housing_costs_gbp",
    "no_qualifications_pct",
    "level4plus_pct",
    "employed_residents_16plus_pct",
    "unemployment_rate_active_pct",
    "fuel_poor_households_pct",
    "overcrowded_households_pct",
    "households_deprived_2plus_pct",
    "no2_area_mean_ug_m3",
    "pm25_area_mean_ug_m3",
    "crime_for_analysis",
    "asb_rows_per_1000_residents",
)
SHORT_LABELS = {'hle_average': 'HLE average', 'hle_male': 'Male HLE', 'hle_female': 'Female HLE', 'annual_equivalised_income_after_housing_costs_gbp': 'Income after housing costs', 'no_qualifications_pct': 'No qualifications', 'level4plus_pct': 'Level 4 and above', 'employed_residents_16plus_pct': 'Employed residents 16+', 'unemployment_rate_active_pct': 'Unemployment rate', 'fuel_poor_households_pct': 'Fuel-poor households', 'overcrowded_households_pct': 'Overcrowded households', 'households_deprived_2plus_pct': 'Households deprived in 2+ dimensions', 'no2_area_mean_ug_m3': 'Nitrogen dioxide (NO₂)', 'pm25_area_mean_ug_m3': 'Fine particles (PM2.5)', 'crime_for_analysis': 'Recorded crime', 'asb_rows_per_1000_residents': 'Antisocial behaviour'}

POOR_END_BY_FIELD = {
    "hle_average": "low",
    "hle_male": "low",
    "hle_female": "low",
    "annual_equivalised_income_after_housing_costs_gbp": "low",
    "no_qualifications_pct": "high",
    "level4plus_pct": "low",
    "employed_residents_16plus_pct": "low",
    "unemployment_rate_active_pct": "high",
    "fuel_poor_households_pct": "high",
    "overcrowded_households_pct": "high",
    "households_deprived_2plus_pct": "high",
    "no2_area_mean_ug_m3": "high",
    "pm25_area_mean_ug_m3": "high",
    "crime_for_analysis": "high",
    "asb_rows_per_1000_residents": "high",
}
HLE_BAND_COLORS = ("#46327e", "#365c8d", "#21918c", "#5ec962", "#d7e75b")
SEQUENTIAL_BAND_COLORS = ("#fff7bc", "#fec44f", "#fe9929", "#ec7014", "#cc4c02")
PROBABILITY_BAND_COLORS = (
    SEQUENTIAL_BAND_COLORS[0], SEQUENTIAL_BAND_COLORS[1],
    SEQUENTIAL_BAND_COLORS[3], SEQUENTIAL_BAND_COLORS[4],
)
PROBABILITY_BAND_LABELS = (
    "not · <5%", "possibly · 5–<50%", "likely · 50–<95%",
    "confidently in the lowest tenth · ≥95%",
)
ETHNICITY_CAVEAT = "Area shares describe who lives in an area. They are not explanations of anyone's health."
CRIME_CAVEAT = (
    "Recorded crime counts what is reported and recorded, which varies with policing, reporting and footfall. "
    "Removing it from the model barely changes accuracy (Notebook 07)."
)
BOTTOM_TENTH_NOTE = (
    "Colour shows the simulated probability of an area ranking in the bottom tenth; "
    "it is not a map of certain outcomes."
)
ETHNICITY_GROUP_SOURCES = {
    "white_british_pct": ("white_british_pct",),
    "other_white_pct": ("white_irish_pct", "white_gypsy_irish_traveller_pct", "white_roma_pct", "white_other_pct"),
    "asian_pct": ("asian_bangladeshi_pct", "asian_chinese_pct", "asian_indian_pct", "asian_pakistani_pct", "asian_other_pct"),
    "black_pct": ("black_african_pct", "black_caribbean_pct", "black_other_pct"),
    "mixed_pct": ("mixed_white_asian_pct", "mixed_white_black_african_pct", "mixed_white_black_caribbean_pct", "mixed_other_pct"),
    "other_pct": ("other_arab_pct", "other_ethnic_group_pct"),
}
ETHNICITY_GROUP_LABELS = {
    "white_british_pct": "White British",
    "other_white_pct": "Other White",
    "asian_pct": "Asian",
    "black_pct": "Black",
    "mixed_pct": "Mixed",
    "other_pct": "Other",
}
RANK_STABILITY_FIELDS = (
    "median_simulated_rank", "rank_5th_percentile", "rank_95th_percentile",
    "rank_interval_width_places", "p_bottom_10_percent", "bottom_10_confidence",
    "p_top_10_percent", "top_10_confidence",
)
RANK_NUMERIC_FIELDS = {
    "median_simulated_rank", "rank_5th_percentile", "rank_95th_percentile",
    "rank_interval_width_places", "p_bottom_10_percent", "p_top_10_percent",
}
WEB_AREA_FIELDS = (
    "area_code", "local_area_name",
    "hle_male", "hle_male_lci", "hle_male_uci", "hle_male_le_imputed",
    "hle_male_health_prevalence_imputed", "hle_male_imputed",
    "hle_female", "hle_female_lci", "hle_female_uci", "hle_female_le_imputed",
    "hle_female_health_prevalence_imputed", "hle_female_imputed",
    "hle_average", "hle_average_lci", "hle_average_uci", "hle_period",
    "households_deprived_2plus_pct", "overcrowded_households_pct",
    "fuel_poor_households_pct", "no2_area_mean_ug_m3", "pm25_area_mean_ug_m3",
    "employed_residents_16plus_pct", "unemployment_rate_active_pct",
    "no_qualifications_pct", "level4plus_pct",
    "annual_equivalised_income_after_housing_costs_gbp",
    "asb_rows_per_1000_residents", "student_dominated", "visitor_hub",
    "exclude_from_crime_analysis", "city_centre_caveat", "crime_for_analysis",
)

BOOLEAN_FIELDS = {
    "hle_male_imputed",
    "hle_female_imputed",
    "student_dominated",
    "visitor_hub",
    "exclude_from_crime_analysis",
    "city_centre_caveat",
}
PAIR_FLAG_FIELDS = [
    "student_dominated_a", "visitor_hub_a", "city_centre_caveat_a",
    "hle_male_imputed_a", "hle_female_imputed_a",
    "student_dominated_b", "visitor_hub_b", "city_centre_caveat_b",
    "hle_male_imputed_b", "hle_female_imputed_b",
]
PAIR_FIELDS = [
    "area_code_a", "area_code_b", "name_a", "name_b", "hle_a", "hle_b",
    "gap", "se_gap", "z", "big_gap", "flags",
]


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)
        if reader.fieldnames is None:
            raise ValueError(f"CSV has no header: {path}")
        return reader.fieldnames, rows


def parse_by_dtype(value: str | None, dtype: str) -> Any:
    if value is None or value == "":
        return None
    if dtype == "bool":
        if value not in {"True", "False"}:
            raise ValueError(f"Expected boolean, received {value!r}")
        return value == "True"
    if dtype.startswith("int"):
        return int(value)
    if dtype.startswith("float"):
        return float(value)
    return value


def parse_pair_value(key: str, value: str | None) -> Any:
    if value is None or value == "":
        return None
    if key in PAIR_FLAG_FIELDS:
        if value not in {"True", "False"}:
            raise ValueError(f"Expected pair boolean for {key}, received {value!r}")
        return value == "True"
    if key in {"area_a", "area_b", "name_a", "name_b"}:
        return value
    return float(value)


def round_coordinates(value: Any) -> Any:
    if isinstance(value, (list, tuple)):
        return [round_coordinates(item) for item in value]
    if isinstance(value, (float, int)) and not isinstance(value, bool):
        return round(float(value), 5)
    return value


def collect_vertices(value: Any, output: set[tuple[float, ...]]) -> None:
    if isinstance(value, (list, tuple)):
        if len(value) >= 2 and isinstance(value[0], (int, float)) and isinstance(value[1], (int, float)):
            output.add(tuple(float(part) for part in value))
        else:
            for item in value:
                collect_vertices(item, output)


def apply_coordinate_precision(value: Any, protected: set[tuple[float, ...]]) -> Any:
    if isinstance(value, (list, tuple)):
        if len(value) >= 2 and isinstance(value[0], (int, float)) and isinstance(value[1], (int, float)):
            original = tuple(float(part) for part in value)
            if original in protected:
                return list(original)
            return [round(float(part), 5) for part in value]
        return [apply_coordinate_precision(item, protected) for item in value]
    return value


def prepare_geometry(source_features: list[dict[str, Any]]) -> tuple[dict[str, Any], int]:
    """Round coordinates globally, protecting source vertices if rounding invalidates a polygon."""
    protected: set[tuple[float, ...]] = set()
    for _ in range(len(source_features) + 1):
        by_code: dict[str, Any] = {}
        geometries: dict[str, Any] = {}
        invalid_codes: list[str] = []
        for feature in source_features:
            code = feature["properties"]["MSOA21CD"]
            coordinates = apply_coordinate_precision(feature["geometry"]["coordinates"], protected)
            by_code[code] = coordinates
            geometry = shape({"type": feature["geometry"]["type"], "coordinates": coordinates})
            geometries[code] = geometry
            if not geometry.is_valid:
                invalid_codes.append(code)
        if invalid_codes:
            prior_count = len(protected)
            for feature in source_features:
                if feature["properties"]["MSOA21CD"] in invalid_codes:
                    collect_vertices(feature["geometry"]["coordinates"], protected)
            if len(protected) == prior_count:
                raise ValueError(f"Coordinate precision loop could not repair invalid geometries: {invalid_codes}")
            continue
        collection = list(geometries.values())
        invalid_edges = coverage_invalid_edges(collection)
        if not coverage_is_valid(collection) or any(not edge.is_empty for edge in invalid_edges):
            raise ValueError("Rounded geometry is valid per polygon but fails shared-coverage validation")
        return {code: coords for code, coords in by_code.items()}, len(protected)
    raise ValueError("Coordinate precision exception process exceeded its iteration limit")


def read_dictionary() -> tuple[list[str], dict[str, dict[str, str]]]:
    fields, rows = read_csv(WIDE_DICTIONARY)
    del fields
    entries = {row["column"]: row for row in rows}
    return list(entries), entries


def smoking_context(areas: list[dict[str, Any]]) -> dict[str, Any]:
    codes = {a["code"] for a in areas}
    _, lookup = read_csv(AUTHORITY_LOOKUP)
    authorities = {row["LAD22CD"]: row["LAD22NM"] for row in lookup if row["MSOA21CD"] in codes}
    area_authorities = {a["local_authority"] for a in areas}
    if set(authorities.values()) != area_authorities:
        raise ValueError("Authority lookup does not cover the dashboard exactly")
    context = json.loads(SMOKING_CONTEXT_FILE.read_text(encoding="utf-8"))
    smoking = context["smoking"]
    if set(smoking["authority_index"]) != set(authorities):
        raise ValueError("Retained smoking context does not match the Unit 3 authority lookup")
    if smoking["authority_index"] != authorities:
        raise ValueError("Retained smoking authority names do not match the Unit 3 authority lookup")
    return smoking


def metric_metadata(dictionary: dict[str, dict[str, str]]) -> dict[str, dict[str, Any]]:
    metrics: dict[str, dict[str, Any]] = {}
    ordered_fields = (*DISPLAY_MEASURE_FIELDS[:3], "p_bottom_10_percent", *DISPLAY_MEASURE_FIELDS[3:])
    for field in ordered_fields:
        if field == "p_bottom_10_percent":
            metrics[field] = {
                "label": "Chance of being in the lowest tenth (HLE)",
                "short_label": "Chance of being in the lowest tenth (HLE)",
                "family": "uncertainty",
                "format": "probability",
                "display_decimals": 1,
                "unit": "%",
                "period": "Notebook 08 · 10,000 simulated draws",
                "definition": "Share of simulated draws in which an area's average HLE ranks in the lowest tenth; the stored probability is between 0 and 1.",
                "poor_end": "low",
                "band_colors": list(PROBABILITY_BAND_COLORS),
                "band_breaks": [0.05, 0.50, 0.95],
                "band_labels": list(PROBABILITY_BAND_LABELS),
                "note": BOTTOM_TENTH_NOTE,
            }
            continue
        if field not in dictionary:
            raise KeyError(f"Metric missing from wide data dictionary: {field}")
        if field not in POOR_END_BY_FIELD:
            raise KeyError(f"Metric missing poor-end direction: {field}")
        record = dictionary[field]
        is_hle = field in {"hle_average", "hle_male", "hle_female"}
        band_colors = HLE_BAND_COLORS if is_hle else SEQUENTIAL_BAND_COLORS
        if not is_hle and POOR_END_BY_FIELD[field] == "low":
            band_colors = tuple(reversed(band_colors))
        metrics[field] = {
            "label": SHORT_LABELS[field] if field in {"no2_area_mean_ug_m3", "pm25_area_mean_ug_m3"} else record["definition"],
            "short_label": SHORT_LABELS.get(field, record["definition"]),
            "family": "hle" if is_hle else "context",
            "sex": {"hle_average": "avg", "hle_male": "male", "hle_female": "female"}.get(field),
            "format": ("years" if is_hle else "percentage" if field.endswith("_pct")
                       else "currency" if record["unit"].startswith("£")
                       else "rate" if "1,000" in record["unit"] else "quantity"),
            "display_decimals": 0 if record["unit"].startswith("£") or "1,000" in record["unit"] else 1,
            "unit": record["unit"],
            "period": record["period"],
            "definition": record["definition"],
            "poor_end": POOR_END_BY_FIELD[field],
            "band_colors": list(band_colors),
        }
    for field, label in ETHNICITY_GROUP_LABELS.items():
        metrics[field] = {
            "label": label,
            "short_label": label,
            "family": "ethnicity",
            "format": "percentage",
            "display_decimals": 1,
            "unit": "%",
            "period": "2021",
            "definition": "Share of all usual residents in the 2021 Census broad ethnic group.",
            "poor_end": "high",
            "band_colors": list(SEQUENTIAL_BAND_COLORS),
            "note": ETHNICITY_CAVEAT,
        }
    metrics["crime_for_analysis"]["note"] = CRIME_CAVEAT
    return metrics


def build_pair(record: dict[str, str], name_by_code: dict[str, str]) -> list[Any]:
    flags = [parse_pair_value(field, record[field]) for field in PAIR_FLAG_FIELDS]
    return [
        record["area_a"],
        record["area_b"],
        name_by_code[record["area_a"]],
        name_by_code[record["area_b"]],
        float(record["hle_average_a"]),
        float(record["hle_average_b"]),
        float(record["gap_years"]),
        float(record["se_gap_years"]),
        float(record["z"]),
        record["big_gap_pair"] == "True",
        flags,
    ]


BIG_GAP_PALETTE = ("#00c9dc", "#b49aff", "#ff9065", "#f4dc88", "#efabd1", "#8acfa8", "#8fb6ff")


def assign_big_gap_colors(big_pairs, pairs, areas):
    """Stable DSATUR colouring of pair conflicts, with code-key tie breaks."""
    members = [set(row) for row in big_pairs]
    borders = {tuple(sorted(row[:2])) for row in pairs}
    conflicts = [set() for _ in members]
    for i, left in enumerate(members):
        for j, right in enumerate(members[:i]):
            if left & right or any(tuple(sorted((a, b))) in borders for a in left for b in right):
                conflicts[i].add(j)
                conflicts[j].add(i)
    keys = ["|".join(sorted(row)) for row in big_pairs]
    hues = {}
    while len(hues) < len(members):
        i = min((i for i in range(len(members)) if i not in hues),
                key=lambda i: (-len({hues[j] for j in conflicts[i] if j in hues}), -len(conflicts[i]), keys[i]))
        used = {hues[j] for j in conflicts[i] if j in hues}
        available = [h for h in range(len(BIG_GAP_PALETTE)) if h not in used]
        if not available:
            raise ValueError("Big-gap conflict graph exceeds the approved palette")
        hues[i] = available[0]
    gaps = {tuple(sorted(row[:2])): abs(row[6]) for row in pairs}
    for area in areas:
        candidates = [i for i, codes in enumerate(members) if area["code"] in codes]
        if candidates:
            area["big_gap_pair"] = min(candidates, key=lambda i: (-gaps[tuple(sorted(big_pairs[i]))], keys[i]))
    return [hues[i] for i in range(len(members))]


def data_payload() -> tuple[dict[str, Any], int, int]:
    source_fields, source_rows = read_csv(WIDE_CSV)
    dict_fields, dictionary = read_dictionary()
    if source_fields != dict_fields:
        raise ValueError("Wide CSV columns do not exactly match data_dictionary.csv order")

    rank_fields, rank_rows = read_csv(RANK_STABILITY_FILE)
    required_rank_fields = {"area_code", "published_hle", *RANK_STABILITY_FIELDS}
    if not required_rank_fields.issubset(rank_fields):
        raise ValueError(f"Rank-stability CSV is missing fields: {sorted(required_rank_fields - set(rank_fields))}")
    rank_by_code: dict[str, dict[str, str]] = {}
    for rank_row in rank_rows:
        code = rank_row["area_code"]
        if code in rank_by_code:
            raise ValueError(f"Rank-stability CSV has duplicate area code: {code}")
        rank_by_code[code] = rank_row
    source_codes = {row["area_code"] for row in source_rows}
    if set(rank_by_code) != source_codes:
        raise ValueError("Rank-stability CSV does not cover exactly the 660 dashboard areas")

    names = json.loads(NAMES_FILE.read_text(encoding="utf-8"))
    geojson = json.loads(GEOMETRY_FILE.read_text(encoding="utf-8"))
    rounded_coordinates_by_code, geometry_precision_exception_count = prepare_geometry(geojson["features"])
    geometry_by_code = {
        feature["properties"]["MSOA21CD"]: feature
        for feature in geojson["features"]
    }

    areas: list[dict[str, Any]] = []
    name_by_code: dict[str, str] = {}
    for row in source_rows:
        code = row["area_code"]
        name_record = names[code]
        display_name = name_record["display_name"].strip()
        qualifier = name_record.get("qualifier", "").strip()
        composed_name = f"{display_name} {qualifier}".strip()
        aliases = []
        for alias in name_record.get("aliases", []):
            cleaned = str(alias).strip()
            if cleaned and cleaned not in aliases:
                aliases.append(cleaned)
        geography = geometry_by_code[code]["properties"]["MSOA21NM"].strip()
        local_authority = geography[:-4].strip()
        geom = shape(geometry_by_code[code]["geometry"])
        representative = geom.representative_point()
        centre = [round(representative.x, 5), round(representative.y, 5)]

        values = {
            field: parse_by_dtype(row[field], dictionary[field]["dtype"])
            for field in WEB_AREA_FIELDS
        }
        for group, source_columns in ETHNICITY_GROUP_SOURCES.items():
            components = [parse_by_dtype(row[column], dictionary[column]["dtype"]) for column in source_columns]
            if any(value is None for value in components):
                raise ValueError(f"Ethnicity group {group} has a missing source value for {code}")
            values[group] = sum(components)
        if not math.isclose(sum(values[group] for group in ETHNICITY_GROUP_SOURCES), 100.0, rel_tol=0, abs_tol=0.1):
            raise ValueError(f"Six broad ethnicity groups do not sum to 100% for {code}")

        rank_record = rank_by_code[code]
        if not math.isclose(float(rank_record["published_hle"]), float(values["hle_average"]), rel_tol=0, abs_tol=1e-8):
            raise ValueError(f"Rank-stability HLE value does not match the wide table for {code}")
        for field in RANK_STABILITY_FIELDS:
            if field in RANK_NUMERIC_FIELDS:
                values[field] = float(rank_record[field])
            else:
                values[field] = rank_record[field]
        if not 0 <= values["p_bottom_10_percent"] <= 1 or not 0 <= values["p_top_10_percent"] <= 1:
            raise ValueError(f"Rank-stability probability is outside 0–1 for {code}")
        if not (1 <= values["rank_5th_percentile"] <= values["rank_95th_percentile"] <= len(source_rows)):
            raise ValueError(f"Rank-stability interval is invalid for {code}")
        # The composed display name comes only from the shared locality-name file.
        values["local_area_name"] = composed_name
        areas.append({
            "code": code,
            "name": composed_name,
            "aliases": aliases,
            "local_authority": local_authority,
            "centre": centre,
            "values": values,
        })
        name_by_code[code] = composed_name

    features: list[dict[str, Any]] = []
    for code, source_feature in geometry_by_code.items():
        rep = shape(source_feature["geometry"]).representative_point()
        features.append({
            "type": "Feature",
            "properties": {
                "area_code": code,
                "centre": [round(rep.x, 5), round(rep.y, 5)],
            },
            "geometry": {
                "type": source_feature["geometry"]["type"],
                "coordinates": rounded_coordinates_by_code[code],
            },
        })

    pair_fields, pair_rows = read_csv(PAIRS_FILE)
    big_gap_fields, big_gap_rows = read_csv(BIG_GAPS_FILE)
    if pair_fields != big_gap_fields:
        raise ValueError("Pair CSV columns do not match")
    pairs = [build_pair(row, name_by_code) for row in pair_rows]
    big_gap_pairs = [[row["area_a"], row["area_b"]] for row in big_gap_rows]

    pair_hues = assign_big_gap_colors(big_gap_pairs, pairs, areas)

    payload = {
        "meta": {
            "big_gap_palette": list(BIG_GAP_PALETTE),
            "big_gap_hues": pair_hues,
            "area_count": len(areas),
            "median_hle_average": 64.1,
            "source_fields": source_fields,
            "mapped_fields": list(WEB_AREA_FIELDS) + list(ETHNICITY_GROUP_SOURCES) + list(RANK_STABILITY_FIELDS),
            "pair_source_fields": pair_fields,
            "pair_fields": PAIR_FIELDS,
            "pair_flag_fields": PAIR_FLAG_FIELDS,
            "geometry_coordinate_precision": 5,
            "geometry_precision_exception_vertices": geometry_precision_exception_count,
            "study_area": "Birmingham and surrounding areas",
        },
        "authority_context": {"smoking": smoking_context(areas)},
        "metrics": metric_metadata(dictionary),
        "areas": areas,
        "geometry": {
            "type": "FeatureCollection",
            "features": features,
        },
        "pairs": pairs,
        "big_gap_pairs": big_gap_pairs,
    }

    original_geometry_bytes = GEOMETRY_FILE.stat().st_size
    rounded_geometry_bytes = len(json.dumps(payload["geometry"], separators=(",", ":"), ensure_ascii=False).encode("utf-8"))
    return payload, original_geometry_bytes, rounded_geometry_bytes


def inline_css_assets(css: str) -> str:
    asset_dir = HERE / "vendor"
    pattern = re.compile(r"url\((['\"]?)([^)'\"]+)\1\)")

    def replace(match: re.Match[str]) -> str:
        url = match.group(2)
        if url.startswith(("data:", "http:", "https:", "//")):
            return match.group(0)
        asset = (asset_dir / url).resolve()
        if not asset.is_relative_to(asset_dir.resolve()) or not asset.is_file():
            return match.group(0)
        mime = "image/png" if asset.suffix.lower() == ".png" else "image/gif"
        encoded = base64.b64encode(asset.read_bytes()).decode("ascii")
        return f"url(data:{mime};base64,{encoded})"

    css = pattern.sub(replace, css)
    return re.sub(r"/\*# sourceMappingURL=.*?\*/", "", css, flags=re.DOTALL)


def write_page(payload_text: str) -> bool:
    if not TEMPLATE_FILE.is_file():
        return False
    js_path = HERE / "vendor/leaflet.js"
    css_path = HERE / "vendor/leaflet.css"
    if not js_path.is_file() or not css_path.is_file():
        raise FileNotFoundError("Expected vendor/leaflet.js and vendor/leaflet.css")
    js = js_path.read_text(encoding="utf-8")
    js = re.sub(r"\n?//# sourceMappingURL=.*?$", "", js, flags=re.MULTILINE)
    css = inline_css_assets(css_path.read_text(encoding="utf-8"))
    template = TEMPLATE_FILE.read_text(encoding="utf-8")
    replacements = {
        "__WEB_DATA__": payload_text,
        "__LEAFLET_JS__": js,
        "__LEAFLET_CSS__": css,
    }
    for placeholder, content in replacements.items():
        if placeholder not in template:
            raise ValueError(f"Template is missing required placeholder {placeholder}")
        template = template.replace(placeholder, content)
    marker = "<span>Exploratory area comparisons</span>"
    if template.count(marker) != 1:
        raise ValueError("Expected one dashboard attribution footer marker")
    question_link = (
        f'<span><a href="{QUESTION_URL}" target="_blank" '
        'rel="noopener noreferrer">Question this work</a></span>'
    )
    template = template.replace(marker, marker + question_link, 1)
    INDEX_FILE.write_text(template, encoding="utf-8")
    return True


def main() -> None:
    payload, original_geometry_bytes, rounded_geometry_bytes = data_payload()
    serialized = json.dumps(payload, separators=(",", ":"), ensure_ascii=False, allow_nan=False)
    DATA_FILE.write_text(serialized + "\n", encoding="utf-8")
    page_built = write_page(serialized)
    print(f"Wrote {DATA_FILE} ({DATA_FILE.stat().st_size:,} bytes)")
    print(f"Source geometry: {original_geometry_bytes:,} bytes; rounded FeatureCollection: {rounded_geometry_bytes:,} bytes")
    print(f"Embedded web data: {len(serialized.encode('utf-8')):,} bytes")
    print(
        "Topology decision: retained all original polygons; rounded to 5 decimals except "
        f"{payload['meta']['geometry_precision_exception_vertices']} source vertices protected globally after rounding invalidated a polygon; no simplification."
    )
    print(f"Self-contained index.html: {'built' if page_built else 'not built; template.html is not present yet'}")


if __name__ == "__main__":
    main()
